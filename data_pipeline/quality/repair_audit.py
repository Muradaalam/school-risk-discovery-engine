
"""Audit structured school records against the extracted PDF pages."""

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROW_START = re.compile(r"^\s*(\d+)\s{2,}")


def page_rows(text: str) -> list[int]:
    numbers = []

    for line in text.splitlines():
        match = ROW_START.match(line)
        if not match:
            continue

        parts = re.split(r"\s{2,}", line.strip())
        if parts == [str(i) for i in range(1, 11)]:
            continue

        numbers.append(int(match.group(1)))

    return numbers


def audit_repair_rows(pages_path: str | Path, csv_path: str | Path, review_path: str | Path,
                      output_path: str | Path, expected_pages: int | None = None) -> dict:
    pages_path, csv_path = Path(pages_path), Path(csv_path)
    review_path, output_path = Path(review_path), Path(output_path)

    if output_path.exists():
        raise FileExistsError(output_path)
    if expected_pages is not None and expected_pages < 1:
        raise ValueError("expected_pages must be positive")

    raw_rows = Counter()
    page_numbers = []
    page_hashes = set()
    empty_pages = []

    with pages_path.open(encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            page = json.loads(line)
            number = int(page["page_number"])
            page_numbers.append(number)
            page_hashes.add(page["pdf_sha256"])

            if not page["text"].strip():
                empty_pages.append(number)

            for serial in page_rows(page["text"]):
                raw_rows[(number, serial)] += 1

    parsed_rows = Counter()
    unverified_udise = 0
    record_hashes = set()

    with csv_path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            key = (int(row["page_number"]), int(row["serial"]))
            parsed_rows[key] += 1
            record_hashes.add(row["pdf_sha256"])
            unverified_udise += row["udise_note"] != "VALID"

    reviewed_rows = Counter()
    review_count = 0
    unnumbered_reviews = 0

    with review_path.open(encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            issue = json.loads(line)
            review_count += 1
            matches = page_rows(issue["raw_text"])

            if len(matches) == 1:
                reviewed_rows[(int(issue["page_number"]), matches[0])] += 1
            else:
                unnumbered_reviews += 1

    accounted = parsed_rows + reviewed_rows
    missing_rows = sorted((raw_rows - accounted).elements())
    unexpected_rows = sorted((accounted - raw_rows).elements())
    duplicate_rows = sorted(key for key, count in parsed_rows.items() if count > 1)
    duplicate_pages = sorted(number for number, count in Counter(page_numbers).items() if count > 1)

    if page_numbers:
        upper = expected_pages if expected_pages is not None else max(page_numbers)
        lower = 1 if expected_pages is not None else min(page_numbers)
        missing_pages = sorted(set(range(lower, upper + 1)) - set(page_numbers))
    else:
        missing_pages = list(range(1, expected_pages + 1)) if expected_pages is not None else []

    raw_serials = {serial for _, serial in raw_rows}
    serial_gaps = []
    serial_gap_count = 0
    serials = sorted(raw_serials)

    for previous, current in zip(serials, serials[1:]):
        gap = max(0, current - previous - 1)
        serial_gap_count += gap

        if len(serial_gaps) < 30:
            serial_gaps.extend(range(previous + 1, previous + 1 + min(gap, 30 - len(serial_gaps))))

    errors = []

    if missing_rows:
        errors.append("PDF row starts are missing from parsed or review outputs")
    if unexpected_rows:
        errors.append("Output rows have no matching PDF row start")
    if duplicate_rows:
        errors.append("Duplicate parsed page/serial pairs")
    if duplicate_pages or missing_pages:
        errors.append("PDF page coverage is incomplete or duplicated")
    if len(page_hashes) != 1 or (record_hashes and record_hashes != page_hashes):
        errors.append("Inconsistent or missing source PDF hashes")

    warnings = []

    if review_count:
        warnings.append("Some school rows require manual review")
    if unnumbered_reviews:
        warnings.append("Some review entries have no unambiguous serial")
    if unverified_udise:
        warnings.append("Some UDISE values are not verified")
    if serial_gap_count:
        warnings.append("Gaps appear in source serial numbers")
    if empty_pages:
        warnings.append("Some pages have no extracted text")

    report = {
        "status": "FAILED" if errors else "REVIEW" if warnings else "CONSISTENT",
        "pages_processed": len(page_numbers),
        "expected_pages": expected_pages,
        "pdf_row_starts": sum(raw_rows.values()),
        "parsed_records": sum(parsed_rows.values()),
        "review_rows": review_count,
        "unverified_udise": unverified_udise,
        "missing_row_count": len(missing_rows),
        "missing_rows": [{"page": p, "serial": s} for p, s in missing_rows[:30]],
        "unexpected_row_count": len(unexpected_rows),
        "unexpected_rows": [{"page": p, "serial": s} for p, s in unexpected_rows[:30]],
        "duplicate_parsed_rows": [{"page": p, "serial": s} for p, s in duplicate_rows[:30]],
        "missing_page_count": len(missing_pages),
        "missing_pages": missing_pages[:30],
        "duplicate_pages": duplicate_pages[:30],
        "serial_gap_count": serial_gap_count,
        "serial_gaps": serial_gaps,
        "empty_pages": empty_pages[:30],
        "errors": errors,
        "warnings": warnings,
        "note": "Structural consistency is not proof that PDF columns were parsed correctly. Manually compare sample rows."
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description="Audit school rows against the extracted PDF pages")
    parser.add_argument("pages")
    parser.add_argument("schools_csv")
    parser.add_argument("review_jsonl")
    parser.add_argument("report_json")
    parser.add_argument("--expected-pages", type=int)

    args = parser.parse_args()
    result = audit_repair_rows(args.pages, args.schools_csv, args.review_jsonl,
                               args.report_json, args.expected_pages)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
