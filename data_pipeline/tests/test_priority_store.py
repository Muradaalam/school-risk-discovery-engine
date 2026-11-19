import csv
import json
import tempfile
import unittest
from pathlib import Path

from data_pipeline.integration.priority_store import load_candidates, pick_school_match


class TestPriorityStore(unittest.TestCase):
    def test_valid_records_and_duplicate_detection(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "priority.csv"
            row = {
                "entity_id": "REPORT:abc", "school_name": "Government Primary School Sonapura",
                "district": "Ajmer", "block": "", "identity_status": "AUTO_EXTRACTED_NAME_UNVERIFIED",
                "issue_state": "CURRENT_CONDITION_UNKNOWN", "priority_score": "70",
                "priority_level": "HIGH", "rank": "1", "incident_groups": "1",
                "evidence_events": "1", "latest_evidence_date": "2026-11-13",
                "evidence_references": json.dumps(["https://newsonair.gov.in/example"]),
                "explanation": "One reported incident", "generated_at": "2026-11-13T20:00:00+00:00",
                "eligible": "True"
            }
            with path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=list(row))
                writer.writeheader()
                writer.writerow(row)
            candidates = load_candidates(path)
            self.assertEqual(len(candidates), 1)
            self.assertEqual(candidates[0]["evidence_references"], ["https://newsonair.gov.in/example"])
            with path.open("a", newline="", encoding="utf-8") as file:
                csv.DictWriter(file, fieldnames=list(row)).writerow(row)
            with self.assertRaisesRegex(ValueError, "duplicate entity_id"):
                load_candidates(path)

    def test_school_matching_requires_unique_identity(self):
        self.assertEqual(pick_school_match([(12, "Ajmer"), (34, "Kekri")], "Kekri"), 34)
        self.assertIsNone(pick_school_match([(12, "Ajmer")], "Kekri"))
        with self.assertRaisesRegex(ValueError, "Ambiguous"):
            pick_school_match([(12, "Ajmer"), (34, "Kekri")])

    def test_rejects_bad_evidence_urls(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "priority.csv"
            path.write_text(
                'entity_id,school_name,district,identity_status,issue_state,priority_score,priority_level,rank,incident_groups,evidence_events,evidence_references,explanation\n'
                'REPORT:1,School A,Ajmer,PROVISIONAL,UNKNOWN,55,MEDIUM,1,1,1,"[""http://bad.example""]",Reported incident\n',
                encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "Evidence URLs"):
                load_candidates(path)


if __name__ == "__main__":
    unittest.main()
