
"""Parse school-repair table rows from page-level PDF text."""

import argparse
import csv
import json
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path

from data_pipeline.normalization.udise_code import normalize_udise_code


HEADERS = [
    "serial", "district", "constituency", "block", "school_name",
    "udise_raw", "udise_code", "udise_note", "school_type",
    "enrollment", "repair_classrooms", "repair_amount_raw",
    "page_number", "source_url", "pdf_sha256"
]

ROW_START = re.compile(r"^\s*\d+\s{2,}")


def columns(line: str) -> list[str]:
    return re.split(r"\s{2,}", line.strip())


def get_row_groups(text: str):
    current = []

    for line in text.splitlines():
        if ROW_START.match(line):
            parts = columns(line)

            if parts == [str(i) for i in range(1, 11)]:
                if current:
                    yield current
                    current = []
                continue

            if current:
                yield current

            current = [line]

        elif current and line.strip() and len(columns(current[0])) != 10:
            current.append(line)

    if current:
        yield current


def parse_school_row(lines: list[str], page: dict) -> dict:
    parts = columns(lines[0])

    if len(parts) == 7 and len(lines) == 2:
        continuation = columns(lines[1])

        if len(continuation) == 4:
            parts = [parts[0], *continuation[:3], f"{parts[1]} {continuation[3]}", *parts[2:]]

    if len(parts) != 10:
        raise ValueError(f"Expected 10 columns, found {len(parts)}")

    serial, district, constituency, block, name, raw_udise, category, enrollment, rooms, amount = parts

    if not all([district, constituency, block, name]):
        raise ValueError("Missing school identity field")

    if category.upper() not in {"PS", "UPS", "SS", "SSS"}:
        raise ValueError(f"Unexpected school category: {category}")

    if not all(re.fullmatch(r"[0-9]+", value) for value in (serial, enrollment, rooms)):
        raise ValueError("Invalid numeric field")

    try:
        number = Decimal(amount)
        if not number.is_finite() or number < 0:
            raise ValueError("Invalid repair amount")
    except InvalidOperation:
        raise ValueError("Invalid repair amount") from None

    try:
        udise = normalize_udise_code(raw_udise)
        udise_note = "VALID"
    except (ValueError, TypeError):
        udise = ""
        udise_note = "REQUIRES_VERIFICATION"

    return {
        "serial": int(serial),
        "district": district,
        "constituency": constituency,
        "block": block,
        "school_name": name,
        "udise_raw": raw_udise,
        "udise_code": udise,
        "udise_note": udise_note,
        "school_type": category.upper(),
        "enrollment": int(enrollment),
        "repair_classrooms": int(rooms),
        "repair_amount_raw": amount,
        "page_number": page["page_number"],
        "source_url": page.get("source_url"),
        "pdf_sha256": page["pdf_sha256"]
    }


def extract_repair_rows(input_path: str | Path, csv_path: str | Path, review_path: str | Path) -> dict:
    input_path, csv_path, review_path = Path(input_path), Path(csv_path), Path(review_path)

    if csv_path == review_path or csv_path.exists() or review_path.exists():
        raise FileExistsError("Choose new output filenames; existing files will not be overwritten")

    records, review, seen = [], [], set()
    pages = 0

    with input_path.open(encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            page = json.loads(line)
            pages += 1

            for lines in get_row_groups(page["text"]):
                try:
                    row = parse_school_row(lines, page)

                    if row["serial"] in seen:
                        raise ValueError("Duplicate serial number")

                    seen.add(row["serial"])
                    records.append(row)

                except (ValueError, KeyError) as error:
                    review.append({
                        "page_number": page["page_number"],
                        "reason": str(error),
                        "raw_text": "\n".join(lines)
                    })

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    review_path.parent.mkdir(parents=True, exist_ok=True)

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(records)

    with review_path.open("w", encoding="utf-8") as file:
        for item in review:
            file.write(json.dumps(item, ensure_ascii=False) + "\n")

    return {
        "pages_processed": pages,
        "records_extracted": len(records),
        "rows_for_review": len(review),
        "udise_needing_verification": sum(row["udise_note"] != "VALID" for row in records)
    }


def main():
    parser = argparse.ArgumentParser(description="Extract school-repair rows from PDF page text")
    parser.add_argument("input")
    parser.add_argument("csv_output")
    parser.add_argument("review_output")

    args = parser.parse_args()
    print(json.dumps(extract_repair_rows(args.input, args.csv_output, args.review_output), indent=2))


if __name__ == "__main__":
    main()
