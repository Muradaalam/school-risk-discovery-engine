
import csv
import json
import tempfile
import unittest
from pathlib import Path

from data_pipeline.quality.repair_audit import audit_repair_rows, page_rows


class TestRepairAudit(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        root = Path(self.folder.name)
        self.pages = root / "pages.jsonl"
        self.schools = root / "schools.csv"
        self.review = root / "review.jsonl"
        self.report = root / "report.json"

        self.write_pages([(1, [1, 2])])
        self.write_schools([(1, 1), (1, 2)])
        self.review.write_text("")

    def write_pages(self, pages):
        with self.pages.open("w") as file:
            for number, serials in pages:
                text = "\n".join(f" {s}    AJMER    SCHOOL {s}" for s in serials)
                file.write(json.dumps({
                    "page_number": number,
                    "pdf_sha256": "hash",
                    "text": text
                }) + "\n")

    def write_schools(self, rows):
        with self.schools.open("w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=[
                "page_number", "serial", "udise_note", "pdf_sha256"
            ])
            writer.writeheader()

            for page, serial in rows:
                writer.writerow({
                    "page_number": page,
                    "serial": serial,
                    "udise_note": "VALID",
                    "pdf_sha256": "hash"
                })

    def test_skips_column_number_header(self):
        header = "1       2       3       4       5       6       7       8       9       10"
        self.assertEqual(page_rows(header + "\n 91    AJMER     SCHOOL"), [91])

    def test_consistent_records(self):
        result = audit_repair_rows(self.pages, self.schools, self.review, self.report, 1)
        self.assertEqual(result["status"], "CONSISTENT")
        self.assertEqual(result["pdf_row_starts"], 2)
        self.assertTrue(self.report.exists())

    def test_missing_record_detected(self):
        self.write_schools([(1, 1)])
        result = audit_repair_rows(self.pages, self.schools, self.review, self.report)
        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["missing_rows"], [{"page": 1, "serial": 2}])

    def test_review_row_is_accounted_for(self):
        self.write_schools([(1, 1)])
        self.review.write_text(json.dumps({
            "page_number": 1,
            "raw_text": " 2    AJMER    broken"
        }) + "\n")

        result = audit_repair_rows(self.pages, self.schools, self.review, self.report)
        self.assertEqual(result["status"], "REVIEW")
        self.assertEqual(result["missing_rows"], [])
        self.assertEqual(result["review_rows"], 1)

    def test_duplicate_records_detected(self):
        self.write_schools([(1, 1), (1, 1), (1, 2)])
        result = audit_repair_rows(self.pages, self.schools, self.review, self.report)
        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["duplicate_parsed_rows"], [{"page": 1, "serial": 1}])

    def test_missing_pages_detected(self):
        result = audit_repair_rows(self.pages, self.schools, self.review, self.report, 2)
        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["missing_pages"], [2])

    def test_mixed_pdf_hashes_detected(self):
        with self.schools.open("r+") as file:
            text = file.read().replace("hash", "different")
            file.seek(0)
            file.write(text)
            file.truncate()

        result = audit_repair_rows(self.pages, self.schools, self.review, self.report)
        self.assertEqual(result["status"], "FAILED")

    def test_existing_report_not_overwritten(self):
        self.report.write_text("existing")

        with self.assertRaises(FileExistsError):
            audit_repair_rows(self.pages, self.schools, self.review, self.report)

        self.assertEqual(self.report.read_text(), "existing")


if __name__ == "__main__":
    unittest.main()
