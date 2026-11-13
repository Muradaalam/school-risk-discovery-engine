#this code is AI generated

import csv
import json
import tempfile
import unittest
from pathlib import Path

from data_pipeline.prioritization.report_queue import build_report_queue


class TestReportQueue(unittest.TestCase):
    def test_auto_links_known_urls_and_incident_groups(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            curated = root / "curated.csv"
            scraped = root / "scraped.jsonl"
            review = root / "review.csv"
            all_csv = root / "all.csv"
            top_csv = root / "top.csv"

            url_akash = "https://newsonair.gov.in/school-tragedy-in-rajasthan-building-collapse-in-jhalawar-leaves-5-dead-20-injured/"
            url_pib = "https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2148897&lang=2&reg=48"
            rows = [
                {"report_id": "1", "school_name": "Government Upper Primary School Piplodi", "district": "Jhalawar", "incident_group": "PIPLODI_2025", "source_url": url_akash, "event_type": "BUILDING_COLLAPSE", "claim_summary": "Roof collapsed", "event_date": "2025-07-25"},
                {"report_id": "2", "school_name": "", "district": "Jhalawar", "incident_group": "PIPLODI_2025", "source_url": url_pib, "event_type": "NHRC_NOTICE", "claim_summary": "School collapse", "event_date": "2025-07-25"},
                {"report_id": "3", "school_name": "Government Primary School Narda", "district": "Udaipur", "incident_group": "NARDA_2026", "source_url": "https://example.com/narda", "event_type": "INCIDENT_REPORT", "claim_summary": "Roof collapsed", "event_date": "2026-10-06"},
                {"report_id": "4", "school_name": "", "district": "Udaipur", "incident_group": "NARDA_2026", "source_url": "https://example.com/nhrc-udaipur", "event_type": "NHRC_NOTICE", "claim_summary": "Reported collapse", "event_date": "2026-10-07"},
                {"report_id": "5", "school_name": "Government Primary School Rampura Kanwarpura", "district": "Jaipur", "incident_group": "RAMPURA_2026", "source_url": "https://example.com/jaipur", "event_type": "BUILDING_DAMAGE", "claim_summary": "Damaged wall", "event_date": "2026-10-01"},
                {"report_id": "6", "school_name": "Government Girls Senior Secondary School Poonamnagar", "district": "Jaisalmer", "incident_group": "POONAMNAGAR_2026", "source_url": "https://example.com/jaisalmer", "event_type": "BUILDING_COLLAPSE", "claim_summary": "Roof collapse", "event_date": "2026-11-01"}
            ]
            with curated.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["report_id", "school_name", "district", "block", "incident_group", "source_url", "event_type", "claim_summary", "event_date"])
                writer.writeheader()
                writer.writerows(rows)

            articles = [
                {"url": url_akash, "source": "AKASHVANI", "title": "", "excerpt": "In Rajasthan, students died after a school building collapsed", "published_date": "2025-07-25"},
                {"url": url_pib, "source": "PIB", "title": "NHRC takes cognizance of government school building collapse", "excerpt": "School building collapsed in Jhalawar", "published_date": ""}
            ]
            scraped.write_text("\n".join(json.dumps(a) for a in articles) + "\n", encoding="utf-8")

            first = build_report_queue(curated, scraped, review, all_csv, top_csv)
            second = build_report_queue(curated, scraped, review, all_csv, top_csv)

            self.assertEqual(first["ranked_school_candidates"], 4)
            self.assertEqual(first["scraped_linked_by_url_or_group"], 2)
            self.assertEqual(first["scraped_unresolved"], 0)
            self.assertEqual(second["ranked_school_candidates"], 4)

            with top_csv.open(newline="", encoding="utf-8") as file:
                schools = list(csv.DictReader(file))
            piplodi = next(r for r in schools if "Piplodi" in r["school_name"])
            self.assertEqual(piplodi["incident_groups"], "1")
            self.assertEqual(piplodi["evidence_events"], "2")
            self.assertEqual(len(json.loads(piplodi["evidence_references"])), 2)

    def test_new_explicitly_named_school_needs_no_manual_approval(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            curated = root / "curated.csv"
            curated.write_text("school_name,district,source_url,incident_group\n", encoding="utf-8")
            scraped = root / "scraped.jsonl"
            articles = [
                {"url": "https://newsonair.gov.in/new-school/", "source": "AKASHVANI", "title": "Government Primary School Sonapura in Ajmer", "excerpt": "The building roof was damaged in Ajmer.", "published_date": "2026-11-13"},
                {"url": "https://pib.gov.in/unnamed/", "source": "PIB", "title": "School roof damaged in Rajasthan", "excerpt": "Authorities visited the school.", "published_date": "2026-11-13"}
            ]
            scraped.write_text("\n".join(json.dumps(a) for a in articles) + "\n", encoding="utf-8")

            result = build_report_queue(curated, scraped, root / "review.csv", root / "all.csv", root / "top.csv")
            self.assertEqual(result["ranked_school_candidates"], 1)
            self.assertEqual(result["scraped_linked_by_name"], 1)
            self.assertEqual(result["scraped_unresolved"], 1)
            with (root / "top.csv").open(newline="", encoding="utf-8") as file:
                row = next(csv.DictReader(file))
            self.assertEqual(row["school_name"], "Government Primary School Sonapura")
            self.assertEqual(row["identity_status"], "AUTO_EXTRACTED_NAME_UNVERIFIED")


if __name__ == "__main__":
    unittest.main()
