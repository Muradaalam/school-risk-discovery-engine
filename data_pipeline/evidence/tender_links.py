
"""Find reviewable links between repair-list schools and public tenders."""

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

GENERIC_WORDS = {
    "government", "govt", "gov", "school", "gsss", "ggsss", "gups", "gps",
    "senior", "secondary", "sr", "sec", "sss", "ss", "ups", "ps",
    "upper", "primary", "primery", "higher", "highersecondary"
}

OUTPUT_FIELDS = [
    "tender_id", "tender_title", "published_date", "tender_source_url",
    "match_status", "match_reason", "school_serial", "school_name",
    "school_district", "school_block", "school_udise_raw", "school_page",
    "repair_pdf_sha256", "repair_source_url"
]


def clean_words(text: str) -> list[str]:
    text = re.sub(r"\([0-9]+\)", " ", text.casefold())
    return re.findall(r"[a-z0-9]+", text)


def place_key(text: str) -> str:
    return " ".join(clean_words(text))


def name_key(text: str) -> str:
    words = clean_words(text)

    if "ggsss" in words:
        words = ["girls" if word == "ggsss" else word for word in words]

    words = [word for word in words if word not in GENERIC_WORDS]
    return " ".join(words)


def school_type_key(text: str) -> str:
    aliases = {
        "GPS": "PS",
        "GUPS": "UPS",
        "GSSS": "SSS",
        "GGSSS": "SSS"
    }
    return aliases.get(text.upper(), text.upper())


def link_tenders(schools_csv: str | Path, tenders_csv: str | Path, output_csv: str | Path) -> dict:
    output_csv = Path(output_csv)

    if output_csv.exists():
        raise FileExistsError(output_csv)

    index = defaultdict(list)

    with Path(schools_csv).open(newline="", encoding="utf-8") as file:
        for school in csv.DictReader(file):
            identity = name_key(school["school_name"])

            if not identity:
                continue

            key = (
                place_key(school["district"]),
                place_key(school["block"]),
                identity,
                school_type_key(school["school_type"])
            )
            index[key].append(school)

    output = []
    statuses = {"POSSIBLE": 0, "AMBIGUOUS": 0, "NO_MATCH": 0}
    seen = set()

    with Path(tenders_csv).open(newline="", encoding="utf-8") as file:
        for tender in csv.DictReader(file):
            tender_id = tender["tender_id"].strip()

            if not tender_id or tender_id in seen:
                raise ValueError("Tender IDs must be present and unique")

            seen.add(tender_id)
            identity = name_key(tender["school_hint"])

            key = (
                place_key(tender["district"]),
                place_key(tender["block"]),
                identity,
                school_type_key(tender["school_type"])
            )

            matches = index.get(key, []) if identity else []

            if len(matches) == 1:
                status = "POSSIBLE"
            elif matches:
                status = "AMBIGUOUS"
            else:
                status = "NO_MATCH"

            statuses[status] += 1

            for school in matches or [None]:
                output.append({
                    "tender_id": tender_id,
                    "tender_title": tender["tender_title"],
                    "published_date": tender["published_date"],
                    "tender_source_url": tender["source_url"],
                    "match_status": status,
                    "match_reason": (
                        "Exact normalized district, block, school name and type; human verification required"
                        if matches else "No exact candidate in parsed repair list"
                    ),
                    "school_serial": school["serial"] if school else "",
                    "school_name": school["school_name"] if school else "",
                    "school_district": school["district"] if school else "",
                    "school_block": school["block"] if school else "",
                    "school_udise_raw": school["udise_raw"] if school else "",
                    "school_page": school["page_number"] if school else "",
                    "repair_pdf_sha256": school["pdf_sha256"] if school else "",
                    "repair_source_url": school["source_url"] if school else ""
                })

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    with output_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(output)

    return {
        "tenders_checked": len(seen),
        "possible": statuses["POSSIBLE"],
        "ambiguous": statuses["AMBIGUOUS"],
        "no_match": statuses["NO_MATCH"],
        "output": str(output_csv)
    }


def main():
    parser = argparse.ArgumentParser(description="Link curated tender evidence to repair-list schools")
    parser.add_argument("schools_csv")
    parser.add_argument("tenders_csv")
    parser.add_argument("output_csv")

    args = parser.parse_args()
    print(json.dumps(link_tenders(args.schools_csv, args.tenders_csv, args.output_csv), indent=2))


if __name__ == "__main__":
    main()
