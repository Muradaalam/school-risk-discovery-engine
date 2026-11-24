"""Offline regression tests for generalized PDF/HTML/XML school extraction."""
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from data_pipeline.extraction.document_extractor import detect_format, extract, run
from data_pipeline.extraction.html_parser import parse_html
from data_pipeline.extraction.pdf_parser import parse_pdf
from data_pipeline.extraction.school_records import extract_school_evidence, parse_school_table_row
from data_pipeline.extraction.xml_parser import parse_xml

FIXTURE = Path(__file__).parent / "fixtures" / "sample_public_school_record.pdf"
META = {"source": "GYAN_SANKALP", "source_url": "https://example.invalid/schools.pdf",
        "sha256": "1234abcd", "title": "जर्जर विद्यालय भवनों की सूची", "format": "pdf"}


class TestGenericSchoolExtraction(unittest.TestCase):
    def test_dilapidated_school_table_line(self):
        line = "88     BALOTRA      GIDA           GPS RAJPURA                                    8171103802 GPS     YES"
        row = parse_school_table_row(line, section={"page_number": 3}, meta=META)
        self.assertEqual((row["district"], row["block"], row["school_name"]),
                         ("BALOTRA", "GIDA", "GPS RAJPURA"))
        self.assertEqual(row["udise_raw"], "8171103802")
        self.assertEqual(row["udise_code"], "")
        self.assertEqual(row["dilapidated_reported"], "YES")
        self.assertEqual(row["evidence_type"], "BUILDING_DILAPIDATED")

    def test_major_repair_table_layout_without_pdf_specific_parser(self):
        line = "101    AJMER     KISHANGARH     KISHANGARH     GUPS KHEDA     8123456789     UPS    200    3    120000"
        meta = {**META, "title": "Major Repair Requirements"}
        row = parse_school_table_row(line, section={"page_number": 10}, meta=meta)
        self.assertEqual(row["school_name"], "GUPS KHEDA")
        self.assertEqual(row["block"], "KISHANGARH")
        self.assertEqual(row["repair_classrooms_raw"], "3")
        self.assertEqual(row["evidence_type"], "MAJOR_REPAIR")

    def test_11_digit_code_preserved_in_verified_format_field(self):
        line = "11    AJMER    AJMER URBAN    GOVT SCHOOL TEST    12345678901 GPS    YES"
        row = parse_school_table_row(line, section={}, meta=META)
        self.assertEqual(row["udise_code"], "12345678901")
        self.assertEqual(row["identity_status"], "VALID_FORMAT_UNVERIFIED_IDENTITY")

    def test_negative_condition_does_not_create_risk_event(self):
        line = "12    AJMER    AJMER URBAN    GPS TEST    8211500202 GPS    NO"
        row = parse_school_table_row(line, section={}, meta=META)
        self.assertEqual(row["evidence_type"], "")

    def test_mismatch_flag(self):
        line = "2415    UDAIPUR    KOTRA    GUPS DAMROLA    8260609203 GPS    YES"
        result = extract_school_evidence([{"page_number": 29, "text": line}], META)
        self.assertEqual(len(result["schools"]), 1)
        self.assertEqual(result["review"][0]["reason"], "SCHOOL_NAME_TYPE_MISMATCH")

    def test_unparsed_possible_table_row_flagged(self):
        line = "42    JAIPUR    JAMWARAMGARH    SCHOOL NAME WITH NO CODE"
        result = extract_school_evidence([{"page_number": 3, "text": line}], META)
        self.assertIn("UNPARSED_POSSIBLE_TABLE_ROW", [x["reason"] for x in result["review"]])

    def test_weather_false_positive_rejected(self):
        txt = "स्कूल शिक्षा निदेशालय ने समय बदला। तापमान में गिरावट हुई और मौसम ठंडा है।"
        result = extract_school_evidence([{"page_number": None, "text": txt}], META)
        self.assertEqual(result["evidence"], [])

    def test_school_roof_incident_preserved_but_unmatched(self):
        txt = "जिला विद्यालय की छत गिरने से तीन कमरे क्षतिग्रस्त हुए।"
        result = extract_school_evidence([{"page_number": None, "text": txt}], META)
        self.assertEqual(len(result["evidence"]), 1)
        self.assertEqual(result["evidence"][0]["identity_status"], "UNRESOLVED")

    def test_html_article_and_table(self):
        content = b'''<html><head><title>School report</title></head><body>
           <nav>noise</nav><article><p>Government school roof collapsed in Rajasthan district.</p>
           <table><tr><th>Sr</th><th>District</th></tr>
           <tr><td>22</td><td>AJMER</td><td>ARAIN</td><td>GPS RAJPURA</td><td>8211500202</td><td>GPS</td><td>YES</td></tr>
           </table></article></body></html>'''
        parsed = parse_html(content)
        result = extract_school_evidence(parsed["sections"], META)
        self.assertEqual(len(result["schools"]), 1)
        self.assertTrue(any(x["identity_status"] == "UNRESOLVED" for x in result["evidence"]))
        self.assertNotIn("noise", parsed["sections"][0]["text"])

    def test_xml_rss_and_atom(self):
        rss = b'<rss><channel><item><title>School roof collapse</title><description>School building collapsed</description><link>https://example.org/a</link></item></channel></rss>'
        parsed = parse_xml(rss)
        self.assertEqual(len(parsed["sections"]), 1)
        self.assertEqual(parsed["sections"][0]["entry_url"], "https://example.org/a")
        result = extract_school_evidence(parsed["sections"], META)
        self.assertTrue(result["evidence"])
        atom = b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>School major repair</title><link href="https://example.org/b"/><summary>School requires repair</summary></entry></feed>'
        self.assertEqual(parse_xml(atom)["sections"][0]["entry_url"], "https://example.org/b")

    def test_xml_dtd_rejected(self):
        malicious = b'<!DOCTYPE data [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><data>&xxe;</data>'
        with self.assertRaises(Exception):
            parse_xml(malicious)

    @unittest.skipUnless(shutil.which("pdftotext"), "Poppler pdftotext not installed")
    def test_real_pdf_layout_extraction(self):
        pages = parse_pdf(FIXTURE)
        self.assertEqual(len(pages), 1)
        self.assertIn("GPS CRPF Campus", pages[0]["text"])
        result = extract_school_evidence(pages, META)
        self.assertGreaterEqual(len(result["schools"]), 1)

    def test_manifest_and_idempotent_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "sample.pdf"
            shutil.copy(FIXTURE, path)
            manifest = root / "acquired_documents.jsonl"
            record = {"source": "GYAN_SANKALP", "url": "https://example.invalid/sample.pdf",
                      "title": META["title"], "saved_path": str(path),
                      "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                      "retrieved_at": "2026-11-23T11:15:15+00:00"}
            manifest.write_text(json.dumps(record, ensure_ascii=False) + "\n")
            out = root / "out"
            a = run([manifest], output_dir=out)
            b = run([manifest], output_dir=out)
            self.assertEqual((a["documents_processed"], a["school_records"]),
                             (b["documents_processed"], b["school_records"]))
            self.assertEqual(a["documents_processed"], 1)
            self.assertEqual(len((out / "documents.jsonl").read_text().splitlines()), 1)

    def test_manifest_wrong_sha_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "sample.pdf"
            shutil.copy(FIXTURE, path)
            manifest = root / "docs.jsonl"
            manifest.write_text(json.dumps({"saved_path": str(path), "sha256": "deadbeef", "url": "https://example.org/f"}) + "\n")
            summary = run([manifest], output_dir=root / "out")
            self.assertEqual(summary["documents_failed"], 1)
            self.assertEqual(summary["school_records"], 0)
            self.assertEqual(summary["status"], "FAILED")

    def test_latest_version_only_and_duplicate_content(self):
        rows = [{"saved_path": str(FIXTURE), "url": "https://example.org/doc", "title": "old", "retrieved_at": "2026-01-01"},
                {"saved_path": str(FIXTURE), "url": "https://example.org/doc", "title": "new", "retrieved_at": "2026-11-01"},
                {"saved_path": str(FIXTURE), "url": "https://example.org/duplicate", "title": "same"}]
        with tempfile.TemporaryDirectory() as temp:
            m = Path(temp) / "manifest.jsonl"
            m.write_text("\n".join(json.dumps(x) for x in rows) + "\n")
            summary = run([m], output_dir=Path(temp) / "out")
            self.assertEqual(summary["documents_processed"], 1)
            self.assertEqual(summary["duplicate_content_skipped"], 1)

    def test_excerpt_manifest_is_labeled_not_full_article(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manifest = root / "articles.jsonl"
            record = {"url": "https://newsonair.gov.in/story", "source": "AKASHVANI",
                      "title": "School roof collapse", "excerpt": "Government school roof collapsed today"}
            manifest.write_text(json.dumps(record) + "\n")
            s = run([manifest], output_dir=root / "out")
            self.assertEqual(s["documents_processed"], 1)
            self.assertIn("EXCERPT_ONLY_NOT_FULL_ARTICLE", (root / "out/review.jsonl").read_text())

    def test_detect_unknown_format(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "file.txt"
            path.write_text("normal plain text")
            with self.assertRaises(ValueError):
                detect_format(path)


if __name__ == "__main__":
    unittest.main()
