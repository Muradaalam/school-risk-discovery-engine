
import argparse
import csv
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

GENERIC = {
    "govt", "government", "gov", "school", "primary", "upper", "senior",
    "secondary", "sr", "sec", "gsss", "ggsss", "gups", "gps", "sss",
    "ups", "ps", "ss", "pm", "shri"
}

REQUIRED = {
    "report_id", "publisher", "published_date", "event_date", "school_name",
    "district", "block", "event_type", "claim_summary", "source_url", "incident_group"
}


def words(value: str) -> list[str]:
    value = re.sub(r"\([0-9]+\)", " ", value.casefold())
    return re.findall(r"[a-z0-9]+", value)


def school_key(name: str) -> str:
    tokens = ["girls" if word in {"ggsss", "ggups", "ggps"} else word for word in words(name)]
    return " ".join(word for word in tokens if word not in GENERIC)


def location_key(value: str) -> str:
    return " ".join(words(value))


def read_reports(path: Path) -> list[dict]:
    reports = []
    seen = set()

    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if not REQUIRED.issubset(reader.fieldnames or []):
            raise ValueError("Missing required public-report CSV headers")

        for report in reader:
            report_id = report["report_id"].strip()
            url = urlparse(report["source_url"].strip())

            if not report_id or report_id in seen:
                raise ValueError("Report IDs must be present and unique")
            if url.scheme not in ("http", "https") or not url.netloc:
                raise ValueError(f"Invalid source URL for {report_id}")
            if not report["district"].strip() or not report["incident_group"].strip():
                raise ValueError(f"Missing location or incident group for {report_id}")
            if not report["publisher"].strip() or not report["event_type"].strip() or not report["claim_summary"].strip():
                raise ValueError(f"Missing evidence fields for {report_id}")

            date.fromisoformat(report["published_date"])
            date.fromisoformat(report["event_date"])

            seen.add(report_id)
            reports.append(report)

    return reports


def link_public_reports(schools_csv: str | Path, reports_csv: str | Path, output_jsonl: str | Path) -> dict:
    output_jsonl = Path(output_jsonl)

    if output_jsonl.exists():
        raise FileExistsError(output_jsonl)

    school_index = defaultdict(list)

    with Path(schools_csv).open(newline="", encoding="utf-8") as file:
        for school in csv.DictReader(file):
            key = school_key(school["school_name"])

            if len(key) < 3:
                continue

            school_index[(location_key(school["district"]), key)].append(school)

    reports = read_reports(Path(reports_csv))
    records = []
    counts = {"POSSIBLE": 0, "AMBIGUOUS": 0, "PROVISIONAL": 0, "UNRESOLVED": 0}

    for report in reports:
        name = report["school_name"].strip()
        district = report["district"].strip()
        block = report["block"].strip()
        key = school_key(name)

        candidates = school_index.get((location_key(district), key), []) if len(key) >= 3 else []

        if block:
            candidates = [s for s in candidates if location_key(s["block"]) == location_key(block)]

        if not name or len(key) < 3:
            status = "UNRESOLVED"
            reason = "No sufficiently distinctive school name in the report"
        elif len(candidates) == 1:
            status = "POSSIBLE"
            reason = "Exact distinctive-name and district match; identity unverified"
        elif len(candidates) > 1:
            status = "AMBIGUOUS"
            reason = "Multiple repair-list schools share the reported name and location"
        else:
            status = "PROVISIONAL"
            reason = "Reported school retained without a matching repair-list record"

        counts[status] += 1

        records.append({
            "report_id": report["report_id"],
            "publisher": report["publisher"],
            "published_date": report["published_date"],
            "event_date": report["event_date"],
            "event_type": report["event_type"],
            "incident_group": report["incident_group"],
            "claim_summary": report["claim_summary"],
            "source_url": report["source_url"],
            "school_name_reported": name,
            "district_reported": district,
            "block_reported": block,
            "match_status": status,
            "match_reason": reason,
            "provisional_id": f"REPORT:{report['report_id']}" if status == "PROVISIONAL" else None,
            "candidates": [{
                "serial": s["serial"],
                "school_name": s["school_name"],
                "district": s["district"],
                "block": s["block"],
                "udise_raw": s["udise_raw"],
                "page_number": s["page_number"],
                "pdf_sha256": s["pdf_sha256"],
                "repair_source_url": s["source_url"]
            } for s in candidates]
        })

    records.sort(key=lambda r: (r["event_date"], r["published_date"], r["report_id"]))

    output_jsonl.parent.mkdir(parents=True, exist_ok=True)

    with output_jsonl.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    return {
        "reports_processed": len(reports),
        **{key.lower(): value for key, value in counts.items()},
        "incident_groups": len({r["incident_group"] for r in records}),
        "output": str(output_jsonl)
    }


def main():
    parser = argparse.ArgumentParser(description="Link public reports to candidate schools")
    parser.add_argument("schools_csv")
    parser.add_argument("reports_csv")
    parser.add_argument("output_jsonl")

    args = parser.parse_args()
    print(json.dumps(link_public_reports(args.schools_csv, args.reports_csv, args.output_jsonl), indent=2))


if __name__ == "__main__":
    main()
