# This part is AI written

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit

from data_pipeline.integration.priority_store import open_db

ISSUE_TYPES = {
    "BUILDING_DILAPIDATED": "BUILDING",
    "BUILDING_CONDITION_REPORTED": "BUILDING",
    "BUILDING_COLLAPSE": "BUILDING",
    "BUILDING_REQUIREMENT": "BUILDING",
    "MAJOR_REPAIR": "BUILDING",
}


def normalize(value):
    return re.sub(r"\s+", " ", str(value or "")).strip().casefold()


def read_jsonl(path):
    with Path(path).open(encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def valid_url(url):
    if not isinstance(url, str) or len(url) > 200:
        return False
    try:
        parsed = urlsplit(url)
        return parsed.scheme == "https" and bool(parsed.hostname)
    except ValueError:
        return False


def prepare_schools(records, evidence=()):
    attached = defaultdict(set)
    unlinked = 0
    for entry in evidence:
        record_id = str(entry.get("school_record_id") or "")
        if record_id and entry.get("evidence_type"):
            attached[record_id].add(entry["evidence_type"])
        else:
            unlinked += 1

    groups = defaultdict(list)
    reviews = []
    for row in records:
        name = str(row.get("school_name") or "").strip()
        district = str(row.get("district") or "").strip()
        block = str(row.get("block") or "").strip()
        code = str(row.get("school_code_raw") or row.get("udise_raw") or "").strip()
        url = row.get("source_url") or ""
        reason = ""
        if not all((name, district, block)):
            reason = "INCOMPLETE_SCHOOL_IDENTITY"
        elif any(len(v) > size for v, size in ((name, 100), (district, 50), (block, 50))):
            reason = "SCHOOL_FIELD_TOO_LONG"
        elif code and not re.fullmatch(r"[0-9]{10,11}", code):
            reason = "INVALID_PRINTED_SCHOOL_CODE"
        elif row.get("review_flag"):
            reason = "EXTRACTION_REVIEW_FLAG"
        elif not valid_url(url):
            reason = "MISSING_OR_INVALID_SOURCE_URL"
        if reason:
            reviews.append({"reason": reason, "record_id": row.get("record_id"), "school_name": name,
                            "district": district, "block": block, "school_code_raw": code, "source_url": url})
            continue
        key = (normalize(district), normalize(block), normalize(name))
        groups[key].append((row, code))

    codes_by_name = {}
    names_by_code = defaultdict(set)
    for key, items in groups.items():
        codes = {code for _, code in items if code}
        codes_by_name[key] = codes
        for code in codes:
            names_by_code[(key[0], code)].add(key)

    prepared = []
    for key, items in sorted(groups.items()):
        codes = codes_by_name[key]
        reason = ""
        if len(codes) > 1:
            reason = "CONFLICTING_PRINTED_CODES_FOR_SCHOOL"
        elif any(len(names_by_code[(key[0], code)]) > 1 for code in codes):
            reason = "PRINTED_CODE_USED_FOR_DIFFERENT_SCHOOLS"
        if reason:
            reviews.append({"reason": reason, "school_name": items[0][0]["school_name"],
                            "district": items[0][0]["district"], "block": items[0][0]["block"],
                            "school_code_raw": sorted(codes), "records_skipped": len(items)})
            continue
        code = next(iter(codes), "")
        school_id = "SRDE:" + hashlib.sha256("\x1f".join((*key, code)).encode()).hexdigest()[:24]
        urls = set()
        kinds = set()
        school_type = ""
        for row, _ in items:
            urls.add((row["source_url"], str(row.get("source") or "OTHER").strip().upper()))
            school_type = school_type or str(row.get("school_type") or "")
            if str(row.get("dilapidated_reported") or "").upper() == "NO":
                continue
            row_kinds = {row.get("evidence_type")} | attached.get(str(row.get("record_id") or ""), set())
            for kind in row_kinds:
                if kind in ISSUE_TYPES:
                    if kind == "MAJOR_REPAIR" and str(row.get("repair_classrooms_raw") or "").isdigit() and int(row["repair_classrooms_raw"]) > 0:
                        kinds.add("CLASSROOM")
                    else:
                        kinds.add(ISSUE_TYPES[kind])
        row = items[0][0]
        prepared.append({"school_id": school_id, "school_name": str(row["school_name"]).strip(),
                         "district": str(row["district"]).strip(), "block": str(row["block"]).strip(),
                         "school_type": school_type[:50], "school_code_raw": code, "issue_types": sorted(kinds),
                         "sources": sorted(urls), "record_count": len(items)})
    return prepared, reviews, unlinked


def lookup_dictionary(cursor, table, column):
    if (table, column) not in {("issue_type", "issue_type"), ("issue_status", "status"),
                              ("source_name", "source_name")}:
        raise ValueError("Unsupported lookup table")
    cursor.execute(f"SELECT id, {column} FROM {table}")
    return {str(value).upper(): row_id for row_id, value in cursor.fetchall()}


def resolve_school(cursor, school, *, create=True):
    lock = " FOR UPDATE" if create else ""
    cursor.execute("SELECT id FROM school WHERE school_id = %s" + lock, (school["school_id"],))
    exact = cursor.fetchall()
    if len(exact) == 1:
        return exact[0][0], False
    if len(exact) > 1:
        raise ValueError("Duplicate SRDE school identifier in database")

    cursor.execute("""SELECT id, block, udise_code FROM school
                   WHERE LOWER(TRIM(school_name)) = %s
                   AND LOWER(TRIM(district)) = %s""" + lock,
                   (normalize(school["school_name"]), normalize(school["district"])))
    same_name = cursor.fetchall()
    matched = [entry for entry in same_name if normalize(entry[1]) == normalize(school["block"])]
    if len(matched) > 1 or (not matched and any(not normalize(entry[1]) for entry in same_name)):
        raise ValueError("Ambiguous existing school identity")
    if matched:
        verified = str(matched[0][2] or "").strip()
        supplied = school.get("school_code_raw", "")
        if len(verified) == 11 and len(supplied) == 11 and verified != supplied:
            raise ValueError("Conflicting 11-digit identifier on existing school")
        return matched[0][0], False

    if not create:
        return None, True
    cursor.execute("""INSERT INTO school
                   (school_id, school_name, state, district, block, school_type)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                   (school["school_id"], school["school_name"], "Rajasthan",
                    school["district"], school["block"], school["school_type"] or None))
    return cursor.lastrowid, True


def import_schools(schools, *, dry_run=False, limit=None, batch_size=500, connection=None):
    if batch_size < 1 or (limit is not None and limit < 1):
        raise ValueError("limit and batch_size must be positive")
    if limit is not None:
        schools = schools[:limit]
    if not schools:
        raise ValueError("No validated schools available for synchronization")
    owned = connection is None
    conn = connection or open_db()
    counters = {"schools_selected": len(schools), "schools_created": 0, "schools_matched": 0,
                "issues_created": 0, "issues_existing": 0, "sources_created": 0,
                "sources_existing": 0, "schools_skipped_db": 0, "batches_committed": 0}
    reviews = []
    try:
        cursor = conn.cursor()
        types = lookup_dictionary(cursor, "issue_type", "issue_type")
        statuses = lookup_dictionary(cursor, "issue_status", "status")
        sources = lookup_dictionary(cursor, "source_name", "source_name")
        required_types = {kind for school in schools for kind in school["issue_types"]}
        missing = required_types - set(types)
        if missing or "UNKNOWN" not in statuses or "OTHER" not in sources:
            raise ValueError(f"Missing database lookup values: issue types={sorted(missing)}, "
                             f"UNKNOWN={'UNKNOWN' in statuses}, OTHER={'OTHER' in sources}")
        for start in range(0, len(schools), batch_size):
            batch = schools[start:start + batch_size]
            try:
                for school in batch:
                    try:
                        school_pk, created = resolve_school(cursor, school, create=not dry_run)
                    except ValueError as error:
                        counters["schools_skipped_db"] += 1
                        reviews.append({"reason": "AMBIGUOUS_DATABASE_MATCH", "school_id": school["school_id"],
                                        "school_name": school["school_name"], "detail": str(error)})
                        continue
                    counters["schools_created" if created else "schools_matched"] += 1
                    if dry_run and created:
                        counters["issues_created"] += len(school["issue_types"])
                        counters["sources_created"] += len(school["sources"])
                        continue
                    for kind in school["issue_types"]:
                        cursor.execute("SELECT id FROM issue WHERE school_id = %s AND issue_type_id = %s LIMIT 1",
                                       (school_pk, types[kind]))
                        if cursor.fetchone():
                            counters["issues_existing"] += 1
                            continue
                        if not dry_run:
                            cursor.execute("""INSERT INTO issue (school_id, issue_type_id, status_id)
                                           VALUES (%s, %s, %s)""",
                                           (school_pk, types[kind], statuses["UNKNOWN"]))
                        counters["issues_created"] += 1
                    for url, origin in school["sources"]:
                        source_type = origin if origin in sources else "OTHER"
                        cursor.execute("""SELECT id FROM source WHERE school_id = %s
                                       AND source_name_id = %s AND source_url = %s LIMIT 1""",
                                       (school_pk, sources[source_type], url))
                        if cursor.fetchone():
                            counters["sources_existing"] += 1
                            continue
                        if not dry_run:
                            cursor.execute("""INSERT INTO source (school_id, source_name_id, source_url)
                                           VALUES (%s, %s, %s)""",
                                           (school_pk, sources[source_type], url))
                        counters["sources_created"] += 1
                if dry_run:
                    conn.rollback()
                else:
                    conn.commit()
                    counters["batches_committed"] += 1
            except Exception:
                conn.rollback()
                raise
    finally:
        if owned:
            conn.close()
    return {**counters, "dry_run": dry_run, "database_review": reviews}


def sync_output(school_path, evidence_path=None, *, review_path=None, dry_run=False,
                limit=None, batch_size=500, connection=None):
    rows = read_jsonl(school_path)
    evidence = read_jsonl(evidence_path) if evidence_path and Path(evidence_path).exists() else []
    schools, reviews, unlinked = prepare_schools(rows, evidence)
    result = import_schools(schools, dry_run=dry_run, limit=limit,
                            batch_size=batch_size, connection=connection)
    all_reviews = reviews + result.pop("database_review")
    if review_path:
        path = Path(review_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            for row in all_reviews:
                file.write(json.dumps(row, ensure_ascii=False) + "\n")
    result.update({"structured_rows_seen": len(rows), "prepared_school_candidates": len(schools),
                   "review_items": len(all_reviews), "unlinked_evidence_ignored": unlinked,
                   "priority_snapshot_untouched": True,
                   "review_output": str(review_path) if review_path else ""})
    return result


def main():
    parser = argparse.ArgumentParser(description="Sync extracted schools to Deen's existing MySQL schema")
    parser.add_argument("--school-records", default="data_pipeline/processed/generalized/school_records.jsonl")
    parser.add_argument("--evidence", default="data_pipeline/processed/generalized/evidence.jsonl")
    parser.add_argument("--review", default="data_pipeline/processed/generalized/db_sync_review.jsonl")
    parser.add_argument("--db-dry-run", action="store_true")
    parser.add_argument("--db-limit", type=int)
    parser.add_argument("--db-batch-size", type=int, default=500)
    args = parser.parse_args()
    print(json.dumps(sync_output(args.school_records, args.evidence, review_path=args.review,
                                 dry_run=args.db_dry_run, limit=args.db_limit,
                                 batch_size=args.db_batch_size), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
