
import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from data_pipeline.prioritization.ranking import FIELDS
from data_pipeline.prioritization.report_queue import canonical_url, norm


PREFIXES = {
    "GPS": "Government Primary School",
    "GUPS": "Government Upper Primary School",
    "GGPS": "Government Girls Primary School",
    "GGUPS": "Government Girls Upper Primary School",
    "GSS": "Government Secondary School",
    "GGSS": "Government Girls Secondary School",
    "GSSS": "Government Senior Secondary School",
    "GGSSS": "Government Girls Senior Secondary School",
}
ALLOWED_EVIDENCE = {"MAJOR_REPAIR", "REPAIR_REQUIREMENT", "BUILDING_DILAPIDATED",
                    "BUILDING_COLLAPSE", "BUILDING_REQUIREMENT", "BUILDING_CONDITION_REPORTED"}
SERIOUS_TYPES = {"BUILDING_COLLAPSE"}


def school_alias(name):
    name = re.sub(r"\s+", " ", (name or "").strip())
    parts = name.split(" ", 1)
    if parts and parts[0].upper().rstrip(".") in PREFIXES:
        name = PREFIXES[parts[0].upper().rstrip(".")] + (" " + parts[1] if len(parts) > 1 else "")
    name = re.sub(r"^GOVT\.?\s+", "Government ", name, flags=re.I)
    return norm(name)


def key_for(row):
    district, block, name = norm(row.get("district")), norm(row.get("block")), school_alias(row.get("school_name"))
    return (district, block, name)


def read_jsonl(path):
    with Path(path).open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if line.strip():
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(f"Invalid JSONL at {path}:{line_no}") from error
                if not isinstance(row, dict):
                    raise ValueError(f"Expected object at {path}:{line_no}")
                yield row


def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        yield from csv.DictReader(f)


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def stable_id(key):
    return "SCHOOL:" + hashlib.sha256("|".join(key).encode("utf-8")).hexdigest()[:20]


def build_unified_queue(report_csv, school_jsonl, all_csv, top_csv, review_jsonl, limit=50):
    
    if limit < 1:
        raise ValueError("limit must be positive")
    paths = [Path(p).resolve() for p in (report_csv, school_jsonl, all_csv, top_csv, review_jsonl)]
    if len(set(paths)) != len(paths):
        raise ValueError("Input/output paths must be distinct")
    report_rows = list(read_csv(report_csv))
    required = {"entity_id", "school_name", "district", "priority_score", "incident_groups", "evidence_references"}
    if report_rows and not required.issubset(report_rows[0]):
        raise ValueError("Report priority CSV has missing required columns")

    reviews = []
    groups = {}
    by_name = defaultdict(set)
    stats = {"structured_rows_seen": 0, "structured_rows_with_evidence": 0, "structured_rows_rejected": 0,
             "document_links_added": 0, "document_duplicate_links": 0,
             "document_schools": 0, "report_schools": len(report_rows),
             "report_pdf_schools_linked": 0, "ambiguous_report_matches": 0}
    for row in read_jsonl(school_jsonl):
        stats["structured_rows_seen"] += 1
        kind = str(row.get("evidence_type") or "").upper().strip()
        if kind not in ALLOWED_EVIDENCE or str(row.get("dilapidated_reported") or "").upper() == "NO":
            continue
        stats["structured_rows_with_evidence"] += 1
        k = key_for(row)
        url = canonical_url(row.get("source_url"))
        if not k[0] or not k[2] or not url:
            stats["structured_rows_rejected"] += 1
            reviews.append({"reason": "SCHOOL_IDENTITY_OR_HTTPS_SOURCE_MISSING", "record_id": row.get("record_id", ""),
                            "source_url": row.get("source_url", "")})
            continue
        if k not in groups:
            groups[k] = {"school_name": str(row["school_name"]).strip(),
                         "district": str(row["district"]).strip(), "block": str(row["block"]).strip(),
                         "identity_status": str(row.get("identity_status") or "UNVERIFIED"),
                         "codes": set(), "links": {}, "types": set()}
        g = groups[k]
        code = str(row.get("school_code_raw") or "").strip()
        if code:
            g["codes"].add(code)
        if url not in g["links"]:
            g["links"][url] = {"kind": kind, "sha": row.get("source_sha256", ""),
                               "source": str(row.get("source", "")), "pages": set()}
            stats["document_links_added"] += 1
        else:
            stats["document_duplicate_links"] += 1
        page = row.get("page_number")
        if isinstance(page, int) and page >= 1:
            g["links"][url]["pages"].add(page)
        g["types"].add(kind)
        by_name[(k[0], k[2])].add(k)

    
    conflicts = {key for key, value in groups.items() if len(value["codes"]) > 1}
    for key, value in groups.items():
        if any(len(str(value[field])) > max_len for field, max_len in (("school_name", 100), ("district", 50), ("block", 50))):
            conflicts.add(key)
            reviews.append({"reason": "SCHOOL_IDENTITY_EXCEEDS_DB_COLUMN", "school_name": value["school_name"],
                            "district": value["district"], "block": value["block"]})
    for key in sorted(conflicts):
        if len(groups[key]["codes"]) <= 1:
            continue
        reviews.append({"reason": "CONFLICTING_RAW_SCHOOL_CODES", "school_name": groups[key]["school_name"],
                        "district": groups[key]["district"], "block": groups[key]["block"],
                        "codes": sorted(groups[key]["codes"])})

    assigned = {}
    used_keys = set()
    for report in report_rows:
        if str(report.get("eligible", "True")).strip().casefold() not in ("1", "true", "yes"):
            continue
        name, district = report.get("school_name", ""), report.get("district", "")
        block = norm(report.get("block"))
        options = by_name.get((norm(district), school_alias(name)), set()) - conflicts
        options = {k for k in options if not block or k[1] == block}
        if len(options) == 1:
            key = next(iter(options))
            if key in used_keys:
                reviews.append({"reason": "MULTIPLE_REPORT_IDENTITIES_FOR_ONE_DOCUMENT_SCHOOL",
                                "school_name": name, "district": district, "entity_id": report.get("entity_id")})
            else:
                assigned[report["entity_id"]] = key
                used_keys.add(key)
                stats["report_pdf_schools_linked"] += 1
        elif len(options) > 1:
            stats["ambiguous_report_matches"] += 1
            reviews.append({"reason": "AMBIGUOUS_REPORT_TO_DOCUMENT_SCHOOL", "school_name": name,
                            "district": district, "entity_id": report.get("entity_id"),
                            "blocks": sorted({k[1] for k in options})})

    now = datetime.now(timezone.utc).isoformat()
    result = []

    def combined_row(report=None, doc=None):
        
        old_groups, old_urls, old_events, old_severe = 0, [], 0, False
        if report:
            old_groups = int(report["incident_groups"])
            old_urls = json.loads(report["evidence_references"])
            old_events = int(report.get("evidence_events") or len(old_urls))
            old_score = int(report["priority_score"])
            old_severe = old_score > (40 + 15 * min(old_groups, 3))
        urls = list(old_urls)
        known_urls = {canonical_url(u) for u in urls}
        new_links = []
        if doc:
            hashes = set()
            for url, item in doc["links"].items():
                fingerprint = item.get("sha") or url
                if fingerprint in hashes:
                    continue
                hashes.add(fingerprint)
                if url not in known_urls:
                    new_links.append(url)
                    known_urls.add(url)
                    pages = item.get("pages", set())
                    urls.append(url + (f"#page={min(pages)}" if pages else ""))
        
        doc_sources = {doc["links"][url].get("source") or "UNKNOWN" for url in new_links} if doc else set()
        new_groups = len(doc_sources)
        groups_count = old_groups + new_groups
        severe = old_severe or bool(doc and doc["types"] & SERIOUS_TYPES)
        score = min(100, 40 + 15 * min(groups_count, 3) + (15 if severe else 0))
        if not report:
            key = key_for(doc)
            entity_id = stable_id(key)
            name, district, block = doc["school_name"], doc["district"], doc["block"]
            identity_status = doc["identity_status"]
            latest = ""
            base_explanation = ""
        else:
            entity_id = report["entity_id"]
            name, district, block = report["school_name"], report["district"], report.get("block") or (doc["block"] if doc else "")
            identity_status = report["identity_status"]
            latest = report.get("latest_evidence_date", "")
            base_explanation = report.get("explanation", "")
        detail = (f"{len(new_links)} additional infrastructure document(s) from {new_groups} source organization(s); "
                  if new_links else "")
        detail += "document publication does not prove current repair status; raw school identifiers may require verification"
        explanation = (base_explanation + "; " if base_explanation else "") + detail
        return {"rank": "", "entity_id": entity_id, "school_name": name, "district": district, "block": block,
                "identity_status": identity_status, "issue_state": "CURRENT_CONDITION_UNKNOWN", "eligible": True,
                "priority_score": score, "priority_level": "LOW" if score <=55 else "MEDIUM" if score <=85 else "HIGH",
                "repair_classrooms": int(report.get("repair_classrooms") or 0) if report else 0,
                "incident_groups": groups_count, "evidence_events": old_events + len(new_links),
                "latest_evidence_date": latest, "evidence_references": json.dumps(urls, ensure_ascii=False),
                "explanation": explanation, "generated_at": now}

    for report in report_rows:
        if str(report.get("eligible", "True")).strip().casefold() not in ("1", "true", "yes"):
            continue
        doc = groups.get(assigned.get(report["entity_id"]))
        result.append(combined_row(report, doc))
    for key, doc in groups.items():
        if key not in used_keys and key not in conflicts:
            result.append(combined_row(None, doc))
            stats["document_schools"] += 1

    
    result.sort(key=lambda r: r["entity_id"])
    result.sort(key=lambda r: r["latest_evidence_date"], reverse=True)
    result.sort(key=lambda r: r["priority_score"], reverse=True)
    for i, row in enumerate(result, 1):
        row["rank"] = i
    write_csv(all_csv, result)
    write_csv(top_csv, result[:limit])
    write_jsonl(review_jsonl, reviews)
    return {**stats, "ranked_candidates": len(result), "high_priority": sum(r["priority_level"] == "HIGH" for r in result),
            "medium_priority": sum(r["priority_level"] == "MEDIUM" for r in result),
            "low_priority": sum(r["priority_level"] == "LOW" for r in result),
            "review_items": len(reviews), "top_count": min(limit, len(result)),
            "all_output": str(all_csv), "top_output": str(top_csv), "review_output": str(review_jsonl)}


def main():
    parser = argparse.ArgumentParser(description="Combine SRDE existing report-based scores and generalized school evidence")
    parser.add_argument("--reports", default="data_pipeline/raw/report_school_priorities.csv")
    parser.add_argument("--schools", default="data_pipeline/processed/generalized/school_records.jsonl")
    parser.add_argument("--all", default="data_pipeline/raw/inspection_school_priorities.csv")
    parser.add_argument("--top", default="data_pipeline/raw/inspection_top50.csv")
    parser.add_argument("--review", default="data_pipeline/raw/inspection_priority_review.jsonl")
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    print(json.dumps(build_unified_queue(args.reports, args.schools, args.all, args.top, args.review, args.limit), indent=2))


if __name__ == "__main__":
    main()
