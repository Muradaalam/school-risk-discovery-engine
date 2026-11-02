import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path


FIELDS = [
    "rank", "entity_id", "school_name", "district", "block", "identity_status",
    "issue_state", "eligible", "priority_score", "priority_level", "repair_classrooms",
    "incident_groups", "evidence_events", "latest_evidence_date",
    "evidence_references", "explanation", "generated_at"
]

RESOLVED_STATES = {"VERIFIED_RESOLVED", "RESOLVED_VERIFIED"}


def rank_school(timeline: dict, generated_at: str) -> dict:
    events = timeline.get("events", [])
    school_name = timeline.get("school_name", "").strip()
    identity = timeline.get("identity_status", "")
    state = timeline.get("issue_state", "")

    repairs = [e for e in events if e.get("type") == "REPAIR_REQUIREMENT"]
    rooms = sum(int(e.get("details", {}).get("repair_classrooms") or 0) for e in repairs)

    incidents = {
        e.get("incident_group") or e.get("event_id")
        for e in events if e.get("type") == "INCIDENT_REPORT"
    }
    incidents.discard(None)

    dates = [e["event_date"] for e in events if e.get("event_date")]
    latest = max(dates, default="")

    references = []
    for event in events:
        url = event.get("source_url")
        if url and url not in references:
            references.append(url)

    eligible = (
        bool(school_name)
        and state not in RESOLVED_STATES
        and bool(repairs or incidents)
    )

    reasons = []

    if repairs:
        score = 20 + min(rooms, 20) * 4
        reasons.append(f"Historical repair list records {rooms} classrooms requiring repair")
    elif incidents:
        score = 35
    else:
        score = 0

    if incidents:
        score += min(len(incidents), 2) * 15
        reasons.append(
            f"{len(incidents)} distinct reported infrastructure incident(s); "
            "identity and claims require verification"
        )

    if any(e.get("type") == "TENDER_PUBLISHED" for e in events):
        reasons.append("Repair tender found; tender publication does not prove completion")

    if identity == "PROVISIONAL":
        reasons.append("Provisional school identity; verify before inspection assignment")

    if state in RESOLVED_STATES:
        reasons.append("Issue marked verified resolved; excluded pending new evidence")
    elif eligible:
        reasons.append("Current physical condition and repair completion not verified")
    else:
        reasons.append("Insufficient school-specific evidence for automatic inclusion")

    score = min(score, 100) if eligible else 0

    if not eligible:
        level = "NOT_RANKED"
    elif score >= 60:
        level = "HIGH"
    elif score >= 35:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "rank": "",
        "entity_id": timeline["entity_id"],
        "school_name": school_name,
        "district": timeline.get("district", ""),
        "block": timeline.get("block", ""),
        "identity_status": identity,
        "issue_state": state,
        "eligible": eligible,
        "priority_score": score,
        "priority_level": level,
        "repair_classrooms": rooms,
        "incident_groups": len(incidents),
        "evidence_events": len(events),
        "latest_evidence_date": latest,
        "evidence_references": json.dumps(references, ensure_ascii=False),
        "explanation": "; ".join(reasons),
        "generated_at": generated_at
    }


def build_priority_queue(timelines_jsonl: str | Path, all_csv: str | Path,
                         top_csv: str | Path, limit: int = 50) -> dict:
    if limit < 1:
        raise ValueError("limit must be positive")

    all_csv, top_csv = Path(all_csv), Path(top_csv)

    if all_csv == top_csv or all_csv.exists() or top_csv.exists():
        raise FileExistsError("Output files must be distinct and must not already exist")

    generated_at = datetime.now(timezone.utc).isoformat()
    candidates = []
    seen = set()

    with Path(timelines_jsonl).open(encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            timeline = json.loads(line)
            entity_id = timeline["entity_id"]

            if entity_id in seen:
                raise ValueError(f"Duplicate timeline entity: {entity_id}")

            seen.add(entity_id)
            candidates.append(rank_school(timeline, generated_at))

    eligible = [r for r in candidates if r["eligible"]]
    excluded = [r for r in candidates if not r["eligible"]]

    eligible.sort(key=lambda r: r["entity_id"])
    eligible.sort(key=lambda r: r["latest_evidence_date"], reverse=True)
    eligible.sort(key=lambda r: r["priority_score"], reverse=True)

    excluded.sort(key=lambda r: r["entity_id"])
    candidates = eligible + excluded

    for index, row in enumerate(eligible, 1):
        row["rank"] = index

    for path, rows in [(all_csv, candidates), (top_csv, eligible[:limit])]:
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)

    return {
        "timeline_entities": len(candidates),
        "eligible_candidates": len(eligible),
        "excluded_entities": len(candidates) - len(eligible),
        "top_count": min(limit, len(eligible)),
        "waiting_count": max(0, len(eligible) - limit),
        "all_output": str(all_csv),
        "top_output": str(top_csv)
    }


def main():
    parser = argparse.ArgumentParser(description="Rank inspection candidates from saved evidence")
    parser.add_argument("timelines_jsonl")
    parser.add_argument("all_csv")
    parser.add_argument("top_csv")
    parser.add_argument("--limit", type=int, default=50)

    args = parser.parse_args()

    result = build_priority_queue(
        args.timelines_jsonl, args.all_csv, args.top_csv, args.limit
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
