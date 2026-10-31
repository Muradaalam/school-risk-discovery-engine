
import csv
import json
import tempfile
import unittest
from pathlib import Path

from data_pipeline.evidence.timeline import build_timelines


class TestTimeline(unittest.TestCase):

    def test_links_candidates_but_keeps_repair_status_unverified(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            schools = root / "schools.csv"
            tenders = root / "tenders.csv"
            reports = root / "reports.jsonl"
            output = root / "timeline.jsonl"

            with schools.open("w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=[
                    "pdf_sha256", "page_number", "serial", "school_name",
                    "district", "block", "udise_raw", "repair_classrooms",
                    "repair_amount_raw", "source_url"
                ])
                writer.writeheader()
                writer.writerow({
                    "pdf_sha256": "hash",
                    "page_number": "3",
                    "serial": "10",
                    "school_name": "GSSS DONDA",
                    "district": "JHALAWAR",
                    "block": "JHALRAPATAN",
                    "udise_raw": "123",
                    "repair_classrooms": "3",
                    "repair_amount_raw": "5.00",
                    "source_url": "https://example.org/repair.pdf"
                })

            with tenders.open("w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=[
                    "tender_id", "tender_title", "published_date",
                    "tender_source_url", "match_status", "school_serial",
                    "school_page", "repair_pdf_sha256", "school_district",
                    "school_block"
                ])
                writer.writeheader()

                writer.writerow({
                    "tender_id": "T1",
                    "tender_title": "Repair Donda",
                    "published_date": "2026-10-02",
                    "tender_source_url": "https://example.org/tender",
                    "match_status": "POSSIBLE",
                    "school_serial": "10",
                    "school_page": "3",
                    "repair_pdf_sha256": "hash"
                })

                writer.writerow({
                    "tender_id": "T2",
                    "tender_title": "Another school",
                    "published_date": "2026-10-03",
                    "tender_source_url": "https://example.org/tender2",
                    "match_status": "NO_MATCH"
                })

            report = {
                "report_id": "R1",
                "event_type": "INCIDENT_REPORT",
                "event_date": "2026-10-01",
                "published_date": "2026-10-02",
                "publisher": "News",
                "source_url": "https://example.org/news",
                "match_status": "POSSIBLE",
                "incident_group": "INCIDENT_1",
                "claim_summary": "Damage reported",
                "school_name_reported": "Donda",
                "candidates": [{
                    "pdf_sha256": "hash",
                    "page_number": "3",
                    "serial": "10"
                }]
            }

            reports.write_text(json.dumps(report) + "\n")

            result = build_timelines(schools, tenders, reports, output)
            rows = [json.loads(line) for line in output.read_text().splitlines()]

            self.assertEqual(result["repair_schools"], 1)
            self.assertEqual(result["timelines_written"], 2)
            self.assertEqual(len(rows[0]["events"]), 3)
            self.assertEqual(rows[0]["issue_state"], "REPAIR_STATUS_UNVERIFIED")
            self.assertEqual(rows[0]["events"][1]["match_status"], "POSSIBLE")
            self.assertEqual(rows[1]["identity_status"], "UNLINKED_TENDER")


if __name__ == "__main__":
    unittest.main()
