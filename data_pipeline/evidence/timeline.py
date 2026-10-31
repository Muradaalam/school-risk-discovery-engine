
import argparse
import csv
import json
from pathlib import Path


def school_id(row: dict) -> str:
    return f"REPAIR:{row['pdf_sha256']}:{row['page_number']}:{row['serial']}"


def repair_event(row: dict) -> dict:
    return {
        "event_id": school_id(row),
        "type": "REPAIR_REQUIREMENT",
        "event_date": None,
        "source": "GYAN_SANKALP",
        "source_url": row.get("source_url", ""),
        "match_status": "SOURCE_RECORD",
        "incident_group": None,
        "details": {
            "repair_classrooms": row.get("repair_classrooms", ""),
            "repair_amount_raw": row.get("repair_amount_raw", ""),
            "page_number": row["page_number"],
            "pdf_sha256": row["pdf_sha256"]
        }
    }


def make_tender_event(row: dict) -> dict:
    return {
        "event_id": f"TENDER:{row['tender_id']}",
        "type": "TENDER_PUBLISHED",
        "event_date": row.get("published_date") or None,
        "source": "RAJASTHAN_EPROCUREMENT",
        "source_url": row.get("tender_source_url", ""),
        "match_status": row["match_status"],
        "incident_group": None,
        "details": {
            "title": row["tender_title"],
            "tender_id": row["tender_id"]
        }
    }


def make_report_event(row: dict) -> dict:
    return {
        "event_id": f"REPORT:{row['report_id']}",
        "type": row["event_type"],
        "event_date": row.get("event_date"),
        "published_date": row.get("published_date"),
        "source": row["publisher"],
        "source_url": row["source_url"],
        "match_status": row["match_status"],
        "incident_group": row["incident_group"],
        "details": {
            "summary": row["claim_summary"],
            "reported_school": row["school_name_reported"]
        }
    }


def build_timelines(schools_csv: str | Path, tender_links_csv: str | Path,
                    reports_jsonl: str | Path, output_jsonl: str | Path) -> dict:
    output_jsonl = Path(output_jsonl)

    if output_jsonl.exists():
        raise FileExistsError(output_jsonl)

    timelines = {}

    with Path(schools_csv).open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            sid = school_id(row)

            if sid in timelines:
                raise ValueError(f"Duplicate repair identity: {sid}")

            timelines[sid] = {
                "entity_id": sid,
                "identity_status": "REPAIR_LIST_RECORD",
                "school_name": row["school_name"],
                "district": row["district"],
                "block": row["block"],
                "udise_raw": row.get("udise_raw", ""),
                "issue_state": "REPAIR_STATUS_UNVERIFIED",
                "events": [repair_event(row)]
            }

    unlinked = []
    tender_groups = {}

    with Path(tender_links_csv).open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            tid = row["tender_id"]
            tender_groups.setdefault(tid, []).append(row)

    for tid, rows in tender_groups.items():
        row = rows[0]
        event = make_tender_event(row)
        candidates = []

        for match in rows:
            if match["school_serial"] and match["school_page"] and match["repair_pdf_sha256"]:
                sid = f"REPAIR:{match['repair_pdf_sha256']}:{match['school_page']}:{match['school_serial']}"

                if sid in timelines:
                    candidates.append(sid)

        if row["match_status"] == "POSSIBLE" and len(set(candidates)) == 1:
            timelines[candidates[0]]["events"].append(event)
            continue

        unlinked.append({
            "entity_id": f"TENDER:{tid}",
            "identity_status": "UNLINKED_TENDER",
            "school_name": "",
            "district": row.get("school_district", ""),
            "block": row.get("school_block", ""),
            "udise_raw": "",
            "issue_state": "NO_VERIFIED_REPAIR_STATUS",
            "candidate_repair_ids": list(dict.fromkeys(candidates)),
            "events": [event]
        })

    report_count = 0

    with Path(reports_jsonl).open(encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            row = json.loads(line)
            report_count += 1
            event = make_report_event(row)
            candidates = row.get("candidates", [])

            if row["match_status"] == "POSSIBLE" and len(candidates) == 1:
                sid = school_id(candidates[0])

                if sid in timelines:
                    timelines[sid]["events"].append(event)
                    continue

            unlinked.append({
                "entity_id": f"REPORT:{row['report_id']}",
                "identity_status": row["match_status"],
                "school_name": row.get("school_name_reported", ""),
                "district": row.get("district_reported", ""),
                "block": row.get("block_reported", ""),
                "udise_raw": "",
                "issue_state": "CURRENT_CONDITION_UNKNOWN",
                "candidate_repair_ids": [school_id(s) for s in candidates],
                "events": [event]
            })

    for timeline in list(timelines.values()) + unlinked:
        timeline["events"].sort(
            key=lambda e: (e["event_date"] is None, e["event_date"] or "", e["event_id"])
        )

    output_jsonl.parent.mkdir(parents=True, exist_ok=True)

    with output_jsonl.open("w", encoding="utf-8") as file:
        for item in list(timelines.values()) + unlinked:
            file.write(json.dumps(item, ensure_ascii=False) + "\n")

    return {
        "repair_schools": len(timelines),
        "tenders_checked": len(tender_groups),
        "reports_checked": report_count,
        "unlinked_evidence_entities": len(unlinked),
        "timelines_written": len(timelines) + len(unlinked),
        "output": str(output_jsonl)
    }


def main():
    parser = argparse.ArgumentParser(description="Build school evidence timelines")
    parser.add_argument("schools_csv")
    parser.add_argument("tender_links_csv")
    parser.add_argument("reports_jsonl")
    parser.add_argument("output_jsonl")

    args = parser.parse_args()
    result = build_timelines(
        args.schools_csv, args.tender_links_csv, args.reports_jsonl, args.output_jsonl
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
