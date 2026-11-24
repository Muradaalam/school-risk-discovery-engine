import copy
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from data_pipeline.integration.school_data_store import import_schools, prepare_schools, sync_output


class SQLiteCursor:
    def __init__(self, connection, owner):
        self.cursor = connection.cursor()
        self.owner = owner

    def execute(self, query, parameters=()):
        query = query.replace(" FOR UPDATE", "").replace("%s", "?")
        if query.lstrip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
            self.owner.writes += 1
        self.cursor.execute(query, parameters)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    @property
    def lastrowid(self):
        return self.cursor.lastrowid


class FakeMySQL:
    def __init__(self):
        self.writes = 0
        self.db = sqlite3.connect(":memory:")
        self.db.executescript("""
            CREATE TABLE school (id INTEGER PRIMARY KEY, school_id TEXT UNIQUE,
              udise_code TEXT, school_name TEXT, state TEXT, district TEXT, block TEXT, school_type TEXT);
            CREATE TABLE issue_type (id INTEGER PRIMARY KEY, issue_type TEXT);
            CREATE TABLE issue_status (id INTEGER PRIMARY KEY, status TEXT);
            CREATE TABLE source_name (id INTEGER PRIMARY KEY, source_name TEXT);
            CREATE TABLE issue (id INTEGER PRIMARY KEY, school_id INTEGER, issue_type_id INTEGER, status_id INTEGER);
            CREATE TABLE source (id INTEGER PRIMARY KEY, school_id INTEGER, source_name_id INTEGER, source_url TEXT);
            CREATE TABLE priority_snapshot (id INTEGER PRIMARY KEY, school_id INTEGER, priority_score INTEGER);
            INSERT INTO issue_type VALUES (1, 'BUILDING'), (2, 'CLASSROOM');
            INSERT INTO issue_status VALUES (5, 'UNKNOWN'), (4, 'VERIFIED');
            INSERT INTO source_name VALUES (5, 'OTHER'), (3, 'NEWSPAPER');
        """)

    def cursor(self):
        return SQLiteCursor(self.db, self)

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def count(self, table):
        return self.db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


class TestSchoolDataStore(unittest.TestCase):
    def setUp(self):
        self.url = "https://gyansankalp.rajasthan.gov.in/file.pdf"
        self.row = {"record_id": "r1", "school_name": "GPS TEST", "district": "AJMER",
                    "block": "AJMER URBAN", "school_code_raw": "8211500202",
                    "source": "GYAN_SANKALP", "source_url": self.url,
                    "identity_status": "REQUIRES_VERIFICATION_10_DIGIT", "school_type": "GPS",
                    "evidence_type": "BUILDING_DILAPIDATED", "dilapidated_reported": "YES"}

    def prep(self, records=None):
        return prepare_schools(records or [self.row])

    def test_raw_ten_digit_code_not_assigned_to_udise(self):
        schools, review, unlinked = self.prep()
        self.assertEqual((len(schools), len(review), unlinked), (1, 0, 0))
        database = FakeMySQL()
        result = import_schools(schools, connection=database)
        self.assertEqual(result["schools_created"], 1)
        self.assertEqual(database.db.execute("SELECT udise_code FROM school").fetchone()[0], None)
        self.assertEqual(database.db.execute("SELECT status_id FROM issue").fetchone()[0], 5)
        self.assertEqual(database.db.execute("SELECT source_name_id FROM source").fetchone()[0], 5)
        self.assertEqual(database.count("priority_snapshot"), 0)

    def test_idempotent_reimport(self):
        schools, _, _ = self.prep()
        db = FakeMySQL()
        import_schools(schools, connection=db)
        result = import_schools(schools, connection=db)
        self.assertEqual((db.count("school"), db.count("issue"), db.count("source")), (1, 1, 1))
        self.assertEqual((result["schools_matched"], result["issues_existing"], result["sources_existing"]), (1, 1, 1))

    def test_dry_run_rolls_back(self):
        schools, _, _ = self.prep()
        db = FakeMySQL()
        result = import_schools(schools, dry_run=True, connection=db)
        self.assertTrue(result["dry_run"])
        self.assertEqual(db.writes, 0)
        self.assertEqual((db.count("school"), db.count("issue"), db.count("source")), (0, 0, 0))

    def test_matching_existing_school_preserves_identity(self):
        schools, _, _ = self.prep()
        db = FakeMySQL()
        db.db.execute("INSERT INTO school (school_id, school_name, district, block) VALUES (?, ?, ?, ?)",
                      ("SCH-OLD", "GPS TEST", "AJMER", "AJMER URBAN"))
        db.db.commit()
        result = import_schools(schools, connection=db)
        self.assertEqual(result["schools_matched"], 1)
        self.assertEqual(db.db.execute("SELECT school_id FROM school").fetchone()[0], "SCH-OLD")
        self.assertEqual(db.count("school"), 1)

    def test_existing_issue_status_is_not_overwritten(self):
        schools, _, _ = self.prep()
        db = FakeMySQL()
        db.db.execute("INSERT INTO school (school_id, school_name, district, block) VALUES (?, ?, ?, ?)",
                      ("SCH-OLD", "GPS TEST", "AJMER", "AJMER URBAN"))
        db.db.execute("INSERT INTO issue (school_id, issue_type_id, status_id) VALUES (1, 1, 4)")
        db.db.commit()
        result = import_schools(schools, connection=db)
        self.assertEqual(result["issues_existing"], 1)
        self.assertEqual(db.db.execute("SELECT status_id FROM issue").fetchone()[0], 4)

    def test_same_school_from_two_pdfs_is_one(self):
        second = copy.deepcopy(self.row)
        second.update(record_id="r2", source_url="https://gyansankalp.rajasthan.gov.in/other.pdf")
        schools, review, _ = self.prep([self.row, second])
        self.assertEqual((len(schools), len(schools[0]["sources"]), len(review)), (1, 2, 0))
        db = FakeMySQL()
        import_schools(schools, connection=db)
        self.assertEqual((db.count("school"), db.count("issue"), db.count("source")), (1, 1, 2))

    def test_conflicting_codes_go_to_review(self):
        other = {**self.row, "record_id": "r2", "school_code_raw": "8211500203"}
        schools, review, _ = self.prep([self.row, other])
        self.assertEqual(schools, [])
        self.assertEqual(review[0]["reason"], "CONFLICTING_PRINTED_CODES_FOR_SCHOOL")

    def test_same_code_two_schools_goes_to_review(self):
        other = {**self.row, "record_id": "r2", "school_name": "GPS OTHER"}
        schools, review, _ = self.prep([self.row, other])
        self.assertEqual(schools, [])
        self.assertEqual(len(review), 2)

    def test_no_flag_does_not_create_issue(self):
        school = {**self.row, "dilapidated_reported": "NO", "evidence_type": ""}
        schools, _, _ = self.prep([school])
        db = FakeMySQL()
        import_schools(schools, connection=db)
        self.assertEqual(db.count("school"), 1)
        self.assertEqual(db.count("issue"), 0)

    def test_unlinked_evidence_does_not_create_issue(self):
        school = {**self.row, "evidence_type": ""}
        evidence = [{"evidence_id": "e1", "school_record_id": "", "evidence_type": "BUILDING_COLLAPSE"}]
        schools, _, unlinked = prepare_schools([school], evidence)
        self.assertEqual((schools[0]["issue_types"], unlinked), ([], 1))

    def test_ambiguous_existing_school_quarantined(self):
        schools, _, _ = self.prep()
        db = FakeMySQL()
        db.db.execute("INSERT INTO school (school_id, school_name, district, block) VALUES (?, ?, ?, ?)",
                      ("SCH-OLD", "GPS TEST", "AJMER", ""))
        db.db.commit()
        result = import_schools(schools, connection=db)
        self.assertEqual(result["schools_skipped_db"], 1)
        self.assertEqual(db.count("school"), 1)
        self.assertEqual(db.count("issue"), 0)

    def test_ambiguous_eleven_digit_match_is_reviewed(self):
        row = {**self.row, "school_code_raw": "12345678901"}
        schools, _, _ = self.prep([row])
        db = FakeMySQL()
        db.db.execute("INSERT INTO school (school_id, school_name, district, block, udise_code) VALUES (?, ?, ?, ?, ?)",
                      ("SCH-OLD", "GPS TEST", "AJMER", "AJMER URBAN", "12345678902"))
        db.db.commit()
        result = import_schools(schools, connection=db)
        self.assertEqual(result["schools_skipped_db"], 1)
        self.assertEqual(db.count("issue"), 0)

    def test_extraction_direct_sync_flag_is_opt_in(self):
        from data_pipeline.extraction.document_extractor import run
        fixture = Path(__file__).parent / "fixtures" / "sample_public_school_record.pdf"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            args = {"files": [fixture], "output_dir": root / "out",
                    "source": "GYAN_SANKALP", "source_url": self.url,
                    "title": "जर्जर विद्यालय भवनों की सूची"}
            with patch("data_pipeline.integration.school_data_store.sync_output", return_value={"dry_run": True}) as mocked:
                plain = run(**args)
                self.assertNotIn("db_sync", plain)
                self.assertEqual(mocked.call_count, 0)
                synced = run(**args, sync_db=True, db_dry_run=True, db_limit=10)
                self.assertEqual(synced["db_sync"], {"dry_run": True})
                self.assertEqual(mocked.call_count, 1)

    def test_sync_jsonl_outputs_review(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "school_records.jsonl").write_text(json.dumps(self.row) + "\n", encoding="utf-8")
            (root / "evidence.jsonl").write_text("", encoding="utf-8")
            db = FakeMySQL()
            result = sync_output(root / "school_records.jsonl", root / "evidence.jsonl",
                                 review_path=root / "db_sync_review.jsonl", connection=db, limit=1)
            self.assertEqual(result["schools_created"], 1)
            self.assertTrue((root / "db_sync_review.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
