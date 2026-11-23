
import argparse
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from data_pipeline.extraction.pdf_parser import parse_pdf
from data_pipeline.extraction.html_parser import parse_html
from data_pipeline.extraction.xml_parser import parse_xml
from data_pipeline.extraction.school_records import extract_school_evidence

DEFAULT_OUTPUT = Path("data_pipeline/processed/generalized")


def checksum(path):
    hash_value = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hash_value.update(chunk)
    return hash_value.hexdigest()


def detect_format(path):
    path = Path(path)
    with path.open("rb") as file:
        header = file.read(1024).lstrip(b"\xef\xbb\xbf\x00\x09\x0a\x0d\x20")
    if header.startswith(b"%PDF-"):
        return "pdf"
    extension = path.suffix.lower()
    text = header.lower()
    if extension in (".xml", ".rss", ".atom") or text.startswith(b"<?xml") or b"<rss" in text[:150] or b"<feed" in text[:150]:
        return "xml"
    if extension in (".html", ".htm") or any(tag in text for tag in (b"<!doctype html", b"<html", b"<body", b"<article")):
        return "html"
    raise ValueError(f"Unsupported document format (PDF/HTML/XML): {path}")


def _sections(path, format_type):
    if format_type == "pdf":
        return {"sections": parse_pdf(path), "title": "", "published_date": ""}
    raw = Path(path).read_bytes()
    if format_type == "html":
        return parse_html(raw)
    if format_type == "xml":
        return parse_xml(raw)
    raise ValueError("Unsupported format")


def _source_metadata(record):
    path = Path(record["saved_path"])
    if not path.is_file():
        raise FileNotFoundError(f"Missing acquired document: {path}")
    if path.stat().st_size > 100 * 1024 * 1024:
        raise ValueError("Document exceeds 100 MB extraction limit")
    actual_sha = checksum(path)
    expected_sha = record.get("sha256", "")
    if expected_sha and expected_sha.lower() != actual_sha:
        raise ValueError(f"SHA-256 mismatch for {path} (acquisition provenance invalid)")
    return {"path": str(path), "sha256": actual_sha,
            "format": detect_format(path), "source": record.get("source", "UNKNOWN"),
            "source_url": record.get("url") or record.get("source_url") or "",
            "title": record.get("title", ""), "retrieved_at": record.get("retrieved_at", "")}


def _parse_manifest(path):
    result, malformed = [], []
    with Path(path).open(encoding="utf-8") as f:
        for num, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise ValueError("Expected a JSON object")
                result.append(row)
            except (json.JSONDecodeError, ValueError) as error:
                malformed.append({"reason": "BAD_MANIFEST_ROW", "manifest": str(path),
                                  "line": num, "error": str(error)[:200]})
    return result, malformed


def _latest_per_url(records):
    chosen, unsourced = {}, []
    for record in records:
        key = record.get("url") or record.get("source_url")
        if not key:
            unsourced.append(record)
            continue
        if key not in chosen or record.get("retrieved_at", "") >= chosen[key].get("retrieved_at", ""):
            chosen[key] = record
    return list(chosen.values()) + unsourced


def _process_excerpt(record):
    title, excerpt = record.get("title", ""), record.get("excerpt") or record.get("summary") or ""
    if not excerpt:
        raise ValueError("Acquisition record has neither a local file nor an excerpt")
    sha = hashlib.sha256((title + "\n" + excerpt).encode("utf-8")).hexdigest()
    meta = {"sha256": sha, "format": "excerpt", "path": "",
            "source": record.get("source", "UNKNOWN"), "source_url": record.get("url", ""),
            "title": title, "retrieved_at": record.get("retrieved_at", "")}
    parsed = {"sections": [{"page_number": None, "kind": "excerpt", "text": title + "\n" + excerpt}]}
    return meta, parsed, ["EXCERPT_ONLY_NOT_FULL_ARTICLE"]


def extract(documents, *, max_documents=None):
    outputs = {"documents": [], "schools": [], "evidence": [], "review": []}
    summary = {"documents_input": len(documents), "documents_processed": 0,
               "documents_failed": 0, "duplicate_content_skipped": 0,
               "pdf_pages": 0, "table_row_candidates": 0, "unparsed_table_rows": 0,
               "school_records": 0, "evidence_records": 0,
               "review_items": 0, "ten_digit_codes": 0, "unsupported_formats": 0}
    seen_sha = set()
    items = documents[:max_documents] if max_documents else documents
    for record in items:
        try:
            if record.get("saved_path"):
                meta = _source_metadata(record)
                parsed = _sections(meta["path"], meta["format"])
                notes = []
                if not meta["title"]:
                    meta["title"] = parsed.get("title", "")
            else:
                meta, parsed, notes = _process_excerpt(record)
            if meta["sha256"] in seen_sha:
                summary["duplicate_content_skipped"] += 1
                continue
            seen_sha.add(meta["sha256"])
            sections = parsed["sections"]
            if meta["format"] == "pdf":
                summary["pdf_pages"] += len(sections)
                if not any(s["text"].strip() for s in sections):
                    notes.append("NO_EXTRACTABLE_PDF_TEXT_OCR_REQUIRED")
            result = extract_school_evidence(sections, meta)
            summary["table_row_candidates"] += result["audit"]["table_row_candidates"]
            summary["unparsed_table_rows"] += result["audit"]["unparsed_table_rows"]
            outputs["schools"].extend(result["schools"])
            outputs["evidence"].extend(result["evidence"])
            outputs["review"].extend(result["review"])
            for note in notes:
                outputs["review"].append({"reason": note, "source_url": meta["source_url"],
                                          "source_sha256": meta["sha256"]})
            summary["documents_processed"] += 1
            outputs["documents"].append({
                **meta, "sections": len(sections), "table_audit": result["audit"],
                "school_records": len(result["schools"]),
                "evidence_records": len(result["evidence"]), "status": "EXTRACTED_UNVERIFIED",
            })
        except (ValueError, OSError, RuntimeError, UnicodeError) as error:
            summary["documents_failed"] += 1
            summary["unsupported_formats"] += int("Unsupported" in str(error))
            outputs["review"].append({"reason": "DOCUMENT_PROCESSING_ERROR", "error": str(error)[:400],
                                      "source_url": record.get("url", ""),
                                      "saved_path": record.get("saved_path", "")})
    summary["school_records"] = len(outputs["schools"])
    summary["evidence_records"] = len(outputs["evidence"])
    summary["review_items"] = len(outputs["review"])
    summary["ten_digit_codes"] = sum(row["identity_status"] == "REQUIRES_VERIFICATION_10_DIGIT" for row in outputs["schools"])
    summary["status"] = "FAILED" if not summary["documents_processed"] else ("PARTIAL" if summary["documents_failed"] else "OK")
    return outputs, summary


def _write_jsonl(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".srde_", suffix=".part", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def run(manifests=(), files=(), *, output_dir=DEFAULT_OUTPUT, source="MANUAL", title="", source_url="", max_documents=None):
    documents, errors = [], []
    for manifest in manifests:
        rows, broken = _parse_manifest(manifest)
        documents.extend(rows)
        errors.extend(broken)
    for filename in files:
        documents.append({"saved_path": str(filename), "source": source,
                          "title": title, "url": source_url})
    if not documents and not errors:
        raise ValueError("Provide at least one --manifest or --file with content")
    documents = _latest_per_url(documents)
    outputs, summary = extract(documents, max_documents=max_documents)
    outputs["review"] = errors + outputs["review"]
    summary["review_items"] = len(outputs["review"])
    summary["generated_at"] = datetime.now(timezone.utc).isoformat()
    out = Path(output_dir)
    for name in ("documents", "schools", "evidence", "review"):
        filename = {"schools": "school_records.jsonl", "evidence": "evidence.jsonl",
                    "documents": "documents.jsonl", "review": "review.jsonl"}[name]
        _write_jsonl(out / filename, outputs[name])
    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser(description="Extract school evidence from acquired PDF, HTML and XML files")
    parser.add_argument("--manifest", action="append", type=Path, default=[], help="Acquisition JSONL manifest (repeatable)")
    parser.add_argument("--file", action="append", type=Path, default=[], help="Local PDF/HTML/XML file (repeatable)")
    parser.add_argument("--source", default="MANUAL", help="Source name for --file")
    parser.add_argument("--title", default="", help="Document title for --file")
    parser.add_argument("--source-url", default="", help="Original URL for --file")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-documents", type=int, default=None)
    args = parser.parse_args()
    if args.max_documents is not None and args.max_documents < 1:
        parser.error("--max-documents must be positive")
    print(json.dumps(run(args.manifest, args.file, output_dir=args.output_dir,
                         source=args.source, title=args.title, source_url=args.source_url,
                         max_documents=args.max_documents), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
