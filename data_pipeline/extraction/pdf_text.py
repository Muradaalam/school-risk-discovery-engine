
"""Extract page-level text from downloaded PDFs."""

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path

from pypdf import PdfReader


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        while chunk := file.read(64 * 1024):
            digest.update(chunk)

    return digest.hexdigest()


def extract_pdf_text(pdf_path: str | Path, output_path: str | Path, start_page: int = 1, limit: int = 3) -> dict:
    if start_page < 1 or limit < 1:
        raise ValueError("start_page and limit must be positive")

    pdf_path = Path(pdf_path)
    output_path = Path(output_path)

    if not pdf_path.is_file():
        raise FileNotFoundError(pdf_path)

    if output_path.exists():
        raise FileExistsError(output_path)

    metadata_path = pdf_path.with_suffix(pdf_path.suffix + ".json")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
    pdf_hash = file_sha256(pdf_path)

    if metadata.get("sha256") and metadata["sha256"] != pdf_hash:
        raise ValueError("PDF checksum does not match acquisition metadata")

    reader = PdfReader(str(pdf_path))
    total_pages = len(reader.pages)

    if start_page > total_pages:
        raise ValueError(f"start_page exceeds PDF page count ({total_pages})")

    end_page = min(total_pages, start_page + limit - 1)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = None
    pages_with_text = 0
    preview = ""

    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=output_path.parent, prefix=".pages_", delete=False) as file:
            temp_path = Path(file.name)

            for page_number in range(start_page, end_page + 1):
                page = reader.pages[page_number - 1]
                text = page.extract_text(extraction_mode="layout") if page.get("/Contents") is not None else ""
                text = text or ""
                has_text = bool(text.strip())
                pages_with_text += has_text

                if has_text and not preview:
                    preview = "\n".join(line.rstrip() for line in text.splitlines() if line.strip())[:1000]

                record = {
                    "source_id": metadata.get("source_id", "GYAN_SANKALP"),
                    "source_url": metadata.get("source_url"),
                    "pdf_sha256": pdf_hash,
                    "page_number": page_number,
                    "text": text,
                    "has_text": has_text
                }

                file.write(json.dumps(record, ensure_ascii=False) + "\n")

        os.replace(temp_path, output_path)
        temp_path = None

    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)

    return {
        "total_pages": total_pages,
        "pages_processed": end_page - start_page + 1,
        "pages_with_text": pages_with_text,
        "output_path": str(output_path),
        "preview": preview
    }


def main():
    parser = argparse.ArgumentParser(description="Inspect PDF text one page at a time")
    parser.add_argument("pdf")
    parser.add_argument("output")
    parser.add_argument("--start-page", type=int, default=1)
    parser.add_argument("--limit", type=int, default=3)

    args = parser.parse_args()
    result = extract_pdf_text(args.pdf, args.output, args.start_page, args.limit)

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result["pages_with_text"] == 0:
        print("No selectable text found in these pages. The PDF may be scanned.")


if __name__ == "__main__":
    main()
