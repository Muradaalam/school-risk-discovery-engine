
import csv
import json
import tempfile
import unittest
from pathlib import Path

from data_pipeline.evidence.public_reports import link_public_reports


class TestPublicReports(unittest.TestCase):

    def test_possible_ambiguous_provisional_and_unresolved(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            schools = root / "schools.csv"
            reports = root / "reports.csv"
            output = root / "evidence.jsonl"

            with schools.open("w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=[
                    "serial", "district", "block", "school_name", "udise_raw",
                    "page_number", "pdf_sha256", "source_url"
                ])
                writer.writeheader()

                for serial, name in [
                    (1, "GUPS PIPLODI"),
                    (2, "GPS NARDA"),
                    (3, "GOVT PRIMARY SCHOOL NARDA")
                ]:
                    writer.writerow({
                        "serial": serial,
                        "district": "UDAIPUR" if serial > 1 else "JHALAWAR",
                        "block": "TEST",
                        "school_name": name,
                        "udise_raw": "8212345678",
                        "page_number": 5,
                        "pdf_sha256": "abc",
                        "source_url": "https://example.org/repair.pdf"
                    })

            with reports.open("w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=[
                    "report_id", "publisher", "published_date", "event_date",
                    "school_name", "district", "block", "event_type",
                    "claim_summary", "source_url", "incident_group"
                ])
                writer.writeheader()

                for report_id, name, district in [
                    ("A", "Government Upper Primary School Piplodi", "JHALAWAR"),
                    ("B", "Government Primary School Narda", "UDAIPUR"),
                    ("C", "Government Primary School Unlisted", "JAIPUR"),
                    ("D", "", "UDAIPUR")
                ]:
                    writer.writerow({
                        "report_id": report_id,
                        "publisher": "Test",
                        "published_date": "2026-10-01",
                        "event_date": "2026-09-30",
                        "school_name": name,
                        "district": district,
                        "block": "",
                        "event_type": "INCIDENT_REPORT",
                        "claim_summary": "Example",
                        "source_url": "https://example.org/report",
                        "incident_group": "INCIDENT_A"
                    })

            result = link_public_reports(schools, reports, output)

            self.assertEqual(
                [result[k] for k in ("possible", "ambiguous", "provisional", "unresolved")],
                [1, 1, 1, 1]
            )

            rows = {
                r["report_id"]: r
                for r in (json.loads(line) for line in output.read_text().splitlines())
            }

            self.assertEqual(rows["A"]["candidates"][0]["serial"], "1")
            self.assertEqual(len(rows["B"]["candidates"]), 2)
            self.assertEqual(rows["C"]["provisional_id"], "REPORT:C")
            self.assertEqual(rows["D"]["candidates"], [])


if __name__ == "__main__":
    unittest.main()
