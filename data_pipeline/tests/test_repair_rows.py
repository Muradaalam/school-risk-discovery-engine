
import csv
import json
import tempfile
import unittest
from pathlib import Path

from data_pipeline.extraction.repair_rows import extract_repair_rows, parse_school_row


LINE = "  1     AJMER                   PUSHKAR                 AJMER RURAL          MAHATMA GANDHI GOVT. SCHOOL GAGWANA (214250)                                 8210304401              SSS              332              5              20.00"

WRAP1 = "111                                                                         SHAHID DEEPENDRA SINGH RATHORE GOVT. SENIOR SECONDARY                        8210404901              SSS              179             11               15.00"
WRAP2 = "        AJMER                   PUSHKAR                AJMER RURAL          SCHOOL LESWA (214319)"

HEADER = " 1                 2                       3                     4                                               5                                             6                  7                 8              9                10"

PAGE = {
    "page_number": 2,
    "source_url": "https://example.org/schools.pdf",
    "pdf_sha256": "abcd"
}


class TestRepairRows(unittest.TestCase):

    def test_parse_actual_simple_row(self):
        result = parse_school_row([LINE], PAGE)

        self.assertEqual(result["school_name"], "MAHATMA GANDHI GOVT. SCHOOL GAGWANA (214250)")
        self.assertEqual(result["district"], "AJMER")
        self.assertEqual(result["enrollment"], 332)
        self.assertEqual(result["repair_classrooms"], 5)
        self.assertEqual(result["repair_amount_raw"], "20.00")
        self.assertEqual(result["page_number"], 2)

    def test_preserves_10_digit_udise(self):
        result = parse_school_row([LINE], PAGE)

        self.assertEqual(result["udise_raw"], "8210304401")
        self.assertEqual(result["udise_code"], "")
        self.assertEqual(result["udise_note"], "REQUIRES_VERIFICATION")

    def test_wrapped_school_name(self):
        result = parse_school_row([WRAP1, WRAP2], PAGE)

        self.assertEqual(result["school_name"], "SHAHID DEEPENDRA SINGH RATHORE GOVT. SENIOR SECONDARY SCHOOL LESWA (214319)")
        self.assertEqual(result["block"], "AJMER RURAL")
        self.assertEqual(result["serial"], 111)

    def test_bad_columns_rejected(self):
        with self.assertRaises(ValueError):
            parse_school_row([" 3     AJMER    missing"], PAGE)

    def test_extracts_csv_and_review(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            pages = root / "pages.jsonl"
            csv_output = root / "schools.csv"
            review_output = root / "review.jsonl"

            content = "\n".join([HEADER, LINE, "  2     AJMER    missing", WRAP1, WRAP2])
            pages.write_text(json.dumps({**PAGE, "text": content}) + "\n", encoding="utf-8")

            summary = extract_repair_rows(pages, csv_output, review_output)

            with csv_output.open(encoding="utf-8") as file:
                records = list(csv.DictReader(file))

            issues = [json.loads(line) for line in review_output.read_text().splitlines()]

            self.assertEqual(summary["records_extracted"], 2)
            self.assertEqual(summary["rows_for_review"], 1)
            self.assertEqual([r["serial"] for r in records], ["1", "111"])
            self.assertEqual(issues[0]["page_number"], 2)

    def test_does_not_overwrite_output(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            csv_output = root / "schools.csv"
            csv_output.write_text("existing")

            with self.assertRaises(FileExistsError):
                extract_repair_rows(root / "missing.jsonl", csv_output, root / "review.jsonl")

            self.assertEqual(csv_output.read_text(), "existing")


if __name__ == "__main__":
    unittest.main()
