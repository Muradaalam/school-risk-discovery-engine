

import argparse
import csv
import json
import os
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit


SCHEMA = Path(__file__).with_name("priority_schema.sql")

UPSERT = """
INSERT INTO srde_report_priorities (
    entity_id, school_fk, priority_rank, priority_score, priority_level,
    identity_status, issue_state, incident_groups, evidence_events,
    latest_evidence_date, evidence_references, explanation, calculated_at,
    active
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
ON DUPLICATE KEY UPDATE
    school_fk = VALUES(school_fk),
    priority_rank = VALUES(priority_rank),
    priority_score = VALUES(priority_score),
    priority_level = VALUES(priority_level),
    identity_status = VALUES(identity_status),
    issue_state = VALUES(issue_state),
    incident_groups = VALUES(incident_groups),
    evidence_events = VALUES(evidence_events),
    latest_evidence_date = VALUES(latest_evidence_date),
    evidence_references = VALUES(evidence_references),
    explanation = VALUES(explanation),
    calculated_at = VALUES(calculated_at),
    active = 1
"""


def to_int(row, field, minimum=0, maximum=None):
    try:
        value = int(row[field])
    except (KeyError, ValueError, TypeError) as error:
        raise ValueError(f"Invalid {field} for {row.get('entity_id')}") from error
    if value < minimum or (maximum is not None and value > maximum):
        raise ValueError(f"Out-of-range {field} for {row.get('entity_id')}")
    return value


def parse_date(value):
    return date.fromisoformat(value) if value else None


def parse_timestamp(value):
    if not value:
        return None
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("generated_at must include a timezone")
    return parsed.astimezone(timezone.utc).replace(tzinfo=None)


def load_candidates(path):
    
    candidates, seen, ranks = [], set(), set()
    required = {
        "entity_id", "school_name", "district", "identity_status", "issue_state",
        "priority_score", "priority_level", "rank", "incident_groups",
        "evidence_events", "evidence_references", "explanation"
    }
    with Path(path).open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing CSV columns: {sorted(missing)}")

        for row in reader:
            if row.get("eligible", "True").strip().casefold() not in ("true", "1", "yes"):
                continue

            entity_id = row["entity_id"].strip()
            name = row["school_name"].strip()
            district = row["district"].strip()
            block = (row.get("block") or "").strip()
            if not entity_id or entity_id in seen:
                raise ValueError(f"Missing or duplicate entity_id: {entity_id!r}")
            if not name or not district:
                raise ValueError(f"School name/district missing for {entity_id}")
            if any(len(text) > limit for text, limit in ((entity_id, 50), (name, 100), (district, 50), (block, 50))):
                raise ValueError(f"School identity exceeds database column length: {entity_id}")

            level = row["priority_level"].strip()
            if level not in ("HIGH", "MEDIUM", "LOW"):
                raise ValueError(f"Invalid priority_level for {entity_id}")

            try:
                urls = json.loads(row["evidence_references"])
            except json.JSONDecodeError as error:
                raise ValueError(f"Invalid evidence JSON for {entity_id}") from error
            if not isinstance(urls, list) or not urls or not all(
                isinstance(url, str) and urlsplit(url).scheme == "https"
                and urlsplit(url).hostname for url in urls
            ):
                raise ValueError(f"Evidence URLs missing or invalid for {entity_id}")

            rank = to_int(row, "rank", 1)
            if rank in ranks:
                raise ValueError(f"Duplicate rank: {rank}")
            seen.add(entity_id)
            ranks.add(rank)

            candidates.append({
                "entity_id": entity_id, "school_name": name, "district": district,
                "block": block, "identity_status": row["identity_status"].strip(),
                "issue_state": row["issue_state"].strip(),
                "priority_score": to_int(row, "priority_score", 0, 100),
                "priority_level": level, "priority_rank": rank,
                "incident_groups": to_int(row, "incident_groups"),
                "evidence_events": to_int(row, "evidence_events"),
                "latest_evidence_date": parse_date(row.get("latest_evidence_date", "")),
                "evidence_references": urls, "explanation": row["explanation"].strip(),
                "calculated_at": parse_timestamp(row.get("generated_at", ""))
            })

    if candidates and ranks != set(range(1, len(candidates) + 1)):
        raise ValueError("Candidate ranks must be consecutive from 1")
    return candidates


def pick_school_match(matches, block=""):
    
    block = (block or "").strip().casefold()
    if block:
        matches = [entry for entry in matches if (entry[1] or "").strip().casefold() == block]
    if len(matches) > 1:
        raise ValueError("Ambiguous existing school records: multiple name/location matches")
    return matches[0][0] if matches else None


def resolve_school(cursor, candidate):
    
    cursor.execute("SELECT id FROM school WHERE school_id = %s FOR UPDATE", (candidate["entity_id"],))
    row = cursor.fetchone()
    if row:
        return row[0], False

    cursor.execute("""SELECT id, block FROM school
        WHERE LOWER(TRIM(school_name)) = LOWER(%s)
          AND LOWER(TRIM(district)) = LOWER(%s) FOR UPDATE""",
        (candidate["school_name"], candidate["district"]))
    existing_id = pick_school_match(cursor.fetchall(), candidate["block"])
    if existing_id is not None:
        return existing_id, False

    cursor.execute("""INSERT INTO school (school_id, school_name, state, district, block)
        VALUES (%s, %s, %s, %s, %s)""", (
        candidate["entity_id"], candidate["school_name"], "Rajasthan",
        candidate["district"], candidate["block"] or None
    ))
    return cursor.lastrowid, True


def mysql_config():
    
    required = ("SRDE_MYSQL_USER", "SRDE_MYSQL_PASSWORD")
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise ValueError(f"Missing MySQL environment variables: {', '.join(missing)}")
    return {
        "host": os.getenv("SRDE_MYSQL_HOST", "localhost"),
        "port": int(os.getenv("SRDE_MYSQL_PORT", "3306")),
        "user": os.environ["SRDE_MYSQL_USER"],
        "password": os.environ["SRDE_MYSQL_PASSWORD"],
        "database": os.getenv("SRDE_MYSQL_DATABASE", "schoolRDE"),
        "autocommit": False
    }


def open_db():
    try:
        import mysql.connector
    except ImportError as error:
        raise RuntimeError("Install the connector with: pip install mysql-connector-python") from error
    return mysql.connector.connect(**mysql_config())


def initialize_schema():
    
    conn = open_db()
    try:
        cursor = conn.cursor()
        cursor.execute(SCHEMA.read_text(encoding="utf-8").strip().rstrip(";"))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return {"schema_ready": True, "table": "srde_report_priorities"}


def import_candidates(csv_path, replace=False):
    
    rows = load_candidates(csv_path)
    if not rows:
        raise ValueError("Refusing to import an empty candidate list")

    conn = open_db()
    matched, created = 0, 0
    try:
        cursor = conn.cursor()
        if replace:
            cursor.execute("UPDATE srde_report_priorities SET active = 0 WHERE active = 1")
        for row in rows:
            school_pk, new_school = resolve_school(cursor, row)
            created += int(new_school)
            matched += int(not new_school)
            cursor.execute(UPSERT, (
                row["entity_id"], school_pk, row["priority_rank"],
                row["priority_score"], row["priority_level"], row["identity_status"],
                row["issue_state"], row["incident_groups"], row["evidence_events"],
                row["latest_evidence_date"], json.dumps(row["evidence_references"]),
                row["explanation"], row["calculated_at"]
            ))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return {
        "imported": len(rows), "matched_existing_schools": matched,
        "new_provisional_schools": created, "full_snapshot": replace,
        "table": "srde_report_priorities"
    }


def main():
    parser = argparse.ArgumentParser(description="MySQL report priority import for SRDE")
    parser.add_argument("csv", nargs="?", default="data_pipeline/raw/report_school_priorities.csv")
    parser.add_argument("--check-only", action="store_true", help="Only validate CSV; no database access")
    parser.add_argument("--init-schema", action="store_true", help="Create the report priority table (requires approval)")
    parser.add_argument("--replace", action="store_true", help="Full ranking snapshot; deactivate absent candidates")
    args = parser.parse_args()

    if args.check_only:
        result = {"validated_candidates": len(load_candidates(args.csv))}
    elif args.init_schema:
        result = initialize_schema()
    else:
        result = import_candidates(args.csv, replace=args.replace)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
