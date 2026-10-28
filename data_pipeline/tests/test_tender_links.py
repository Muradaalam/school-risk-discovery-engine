
import csv
import tempfile
import unittest
from pathlib import Path

from data_pipeline.evidence.tender_links import link_tenders


class TestTenderLinks(unittest.TestCase):

    def test_possible_ambiguous_and_unmatched(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            schools = root / "schools.csv"
            tenders = root / "tenders.csv"
            output = root / "links.csv"

            with schools.open("w", newline="") as file:
                fields = [
                    "serial", "school_name", "district", "block", "school_type",
                    "udise_raw", "page_number", "pdf_sha256", "source_url"
                ]
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()

                records = [
                    (1, "GOVT SENIOR SECONDARY SCHOOL DONDA (123)", "JHALAWAR", "JHALRAPATAN"),
                    (2, "GSSS KHOD", "PALI", "RANI"),
                    (3, "GOVT SR SEC SCHOOL KHOD", "PALI", "RANI")
                ]

                for serial, name, district, block in records:
                    writer.writerow({
                        "serial": serial,
                        "school_name": name,
                        "district": district,
                        "block": block,
                        "school_type": "SSS",
                        "udise_raw": "8320211205",
                        "page_number": "42",
                        "pdf_sha256": "abc",
                        "source_url": "https://example.org/repair.pdf"
                    })

            with tenders.open("w", newline="") as file:
                fields = [
                    "tender_id", "tender_title", "school_hint", "district",
                    "block", "school_type", "published_date", "source_url"
                ]
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()

                records = [
                    ("A", "GSSS DONDA", "JHALAWAR", "JHALRAPATAN"),
                    ("B", "GSSS KHOD", "PALI", "RANI"),
                    ("C", "GSSS NONE", "PALI", "RANI")
                ]

                for tender_id, name, district, block in records:
                    writer.writerow({
                        "tender_id": tender_id,
                        "tender_title": "Test",
                        "school_hint": name,
                        "district": district,
                        "block": block,
                        "school_type": "SSS",
                        "published_date": "2026-10-02",
                        "source_url": "https://example.org"
                    })

            result = link_tenders(schools, tenders, output)

            self.assertEqual(result["possible"], 1)
            self.assertEqual(result["ambiguous"], 1)
            self.assertEqual(result["no_match"], 1)

            with output.open(newline="") as file:
                rows = list(csv.DictReader(file))

            self.assertEqual(len(rows), 4)
            self.assertEqual(rows[0]["school_serial"], "1")
            self.assertEqual(rows[-1]["match_status"], "NO_MATCH")


if __name__ == "__main__":
    unittest.main()
