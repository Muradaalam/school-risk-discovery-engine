
import csv
import json
import tempfile
import unittest
from pathlib import Path

from data_pipeline.prioritization.ranking import build_priority_queue


def timeline(sid, rooms=0, state="REPAIR_STATUS_UNVERIFIED",
             identity="REPAIR_LIST_RECORD", incidents=0):
    events = []

    if rooms:
        events.append({
            "event_id": f"REPAIR:{sid}",
            "type": "REPAIR_REQUIREMENT",
            "event_date": None,
            "details": {"repair_classrooms": str(rooms)}
        })

    for i in range(incidents):
        events.append({
            "event_id": f"REPORT:{sid}:{i}",
            "type": "INCIDENT_REPORT",
            "event_date": "2026-10-06",
            "incident_group": "SAME_INCIDENT"
        })

    return {
        "entity_id": sid,
        "school_name": sid,
        "district": "AJMER",
        "block": "TEST",
        "identity_status": identity,
        "issue_state": state,
        "events": events
    }


class TestRanking(unittest.TestCase):

    def test_queue_priorities_and_deduplication(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            data = root / "in.jsonl"
            all_csv = root / "all.csv"
            top = root / "top.csv"

            rows = [
                timeline("A", 12),
                timeline("B", 5),
                timeline("C", 1),
                timeline("D", 0, identity="PROVISIONAL", incidents=2),
                timeline("E", 20, state="VERIFIED_RESOLVED")
            ]

            data.write_text("\n".join(json.dumps(r) for r in rows) + "\n")

            result = build_priority_queue(data, all_csv, top, limit=3)

            with top.open(newline="") as file:
                chosen = list(csv.DictReader(file))

            with all_csv.open(newline="") as file:
                all_rows = list(csv.DictReader(file))

            self.assertEqual(result["top_count"], 3)
            self.assertEqual(result["waiting_count"], 1)
            self.assertEqual([r["entity_id"] for r in chosen], ["A", "D", "B"])

            provisional = next(r for r in all_rows if r["entity_id"] == "D")
            resolved = next(r for r in all_rows if r["entity_id"] == "E")

            self.assertEqual(provisional["incident_groups"], "1")
            self.assertEqual(resolved["eligible"], "False")

    def test_resolved_candidate_replaced_from_waiting_list(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            data = root / "input.jsonl"

            rows = [timeline("A", 12), timeline("B", 5)]
            data.write_text("\n".join(json.dumps(r) for r in rows) + "\n")

            build_priority_queue(data, root / "all1.csv", root / "top1.csv", limit=1)

            updated = [
                timeline("A", 12, state="VERIFIED_RESOLVED"),
                timeline("B", 5)
            ]

            data.write_text("\n".join(json.dumps(r) for r in updated) + "\n")

            build_priority_queue(data, root / "all2.csv", root / "top2.csv", limit=1)

            with (root / "top2.csv").open(newline="") as file:
                selected = next(csv.DictReader(file))

            self.assertEqual(selected["entity_id"], "B")


if __name__ == "__main__":
    unittest.main()
