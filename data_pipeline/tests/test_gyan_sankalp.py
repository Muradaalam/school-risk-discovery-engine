import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from data_pipeline.acquisition.gyan_sankalp import (
    HOST, collect, extract_candidates, pdf_link, approved,
)

PAGE = f"https://{HOST}/Home/HomePage.aspx"
REPAIR = f"https://{HOST}/PDF/FCRA/3.20260626_ACR_Raiparing_List_compressed.pdf"
BUILDING = f"https://{HOST}/PDF/FCRA/1.20260626_NewBuidlidng_Requirement_withPlan.pdf"
HELP = f"https://{HOST}/PDF/20261028_CSR_Help_Docs_Updated.pdf"
HTML = f"""<html><body><h1>Gyan Sankalp</h1>
  <div><span>मेजर रिपेयरिंग आवश्यकता वाले विद्यालयो की सूची</span>
  <a href='/PDF/FCRA/3.20260626_ACR_Raiparing_List_compressed.pdf'>Click Here To View PDF</a></div>
  <div><span>जर्जर विद्यालय भवनों की सूची</span>
  <a href='/PDF/FCRA/1.20260626_NewBuidlidng_Requirement_withPlan.pdf'>Click Here To View PDF</a></div>
  <div><a href='/PDF/20261028_CSR_Help_Docs_Updated.pdf'>Help</a></div>
  <div><a href='https://evil.example/school-repair.pdf'>School repair offsite</a></div>
  </body></html>""".encode()


class Reply:
    def __init__(self, url, body=b"", status=200, headers=None):
        self.url, self.content, self.status_code = url, body, status
        self.headers = headers or {"Content-Type": "application/pdf"}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise ValueError("HTTP error")

    def iter_content(self, chunk_size=65536):
        yield self.content[:3]
        yield self.content[3:]

    def close(self):
        pass


class FakeSession:
    def __init__(self, pdfs=None, listing=HTML):
        self.pdfs = pdfs if pdfs is not None else {REPAIR: b"%PDF-1.7\nrepair\n%%EOF", BUILDING: b"%PDF-1.7\nbuilding\n%%EOF"}
        self.listing = listing
        self.calls = []
        self.response_override = {}

    def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        if url in self.response_override:
            return self.response_override[url]
        if url == PAGE:
            return Reply(url, self.listing, headers={"Content-Type": "text/html; charset=utf-8"})
        if url in self.pdfs:
            return Reply(url, self.pdfs[url], headers={"Content-Type": "application/pdf"})
        raise AssertionError(f"Unexpected request: {url}")


class TestGyanSankalp(unittest.TestCase):
    def test_extract_repair_and_building_not_help(self):
        found = {d["url"] for d in extract_candidates(HTML, PAGE)}
        self.assertEqual(found, {REPAIR, BUILDING})

    def test_host_restrictions(self):
        self.assertTrue(approved(REPAIR))
        self.assertFalse(approved("https://evil.example/school-repair.pdf"))
        self.assertFalse(approved("http://" + HOST + "/PDF/repair.pdf"))
        self.assertEqual(pdf_link(PAGE, "javascript:__doPostBack('a','b')"), "")
        self.assertEqual(pdf_link(PAGE, "//evil.example/school-repair.pdf"), "")
        self.assertEqual(pdf_link(PAGE, "/PDF/repair.PDF"), f"https://{HOST}/PDF/repair.PDF")

    def test_initial_collection_and_no_repeat_before_recheck(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            client = FakeSession()
            kwargs = dict(output_dir=root / "pdfs", state_db=root / "state.sqlite", pages=(PAGE,), session=client)
            first = collect(**kwargs)
            self.assertEqual(first["pages_ok"], 1)
            self.assertEqual(first["discovered"], 2)
            self.assertEqual(first["new_urls"], 2)
            self.assertEqual(first["downloaded"], 2)
            self.assertEqual(len(list((root / "pdfs").glob("*.pdf"))), 2)
            events = (root / "pdfs" / "acquired_documents.jsonl").read_text().splitlines()
            self.assertEqual(len(events), 2)
            self.assertEqual(json.loads(events[0])["review_status"], "UNVERIFIED_SCHOOL_AND_REPAIR_STATUS")
            second = collect(**kwargs)
            self.assertEqual(second["downloaded"], 0)
            self.assertEqual(second["new_urls"], 0)
            self.assertEqual(len(client.calls), 4)  # two listing requests total + two PDFs

    def test_changed_pdf_is_versioned_and_identical_pdf_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            client = FakeSession(pdfs={REPAIR: b"%PDF-1.7\nVERSION1\n%%EOF"})
            # Keep one candidate by making the building link absent.
            client.listing = HTML.replace(b"/PDF/FCRA/1.20260626_NewBuidlidng_Requirement_withPlan.pdf", b"/PDF/FCRA/ignored.txt")
            kw = dict(output_dir=root / "pdfs", state_db=root / "state.sqlite", pages=(PAGE,), session=client, recheck_hours=0)
            first = collect(**kw)
            self.assertEqual(first["downloaded"], 1)
            second = collect(**kw)
            self.assertEqual(second["unchanged"], 1)
            client.pdfs[REPAIR] = b"%PDF-1.7\nVERSION2\n%%EOF"
            third = collect(**kw)
            self.assertEqual(third["updated"], 1)
            self.assertEqual(len(list((root / "pdfs").glob("*.pdf"))), 2)
            with sqlite3.connect(root / "state.sqlite") as db:
                self.assertEqual(db.execute("select count(*) from versions").fetchone()[0], 2)
            db.close()

    def test_http_304_preserves_original(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            client = FakeSession()
            kw = dict(output_dir=root / "pdfs", state_db=root / "state.sqlite", pages=(PAGE,), session=client, recheck_hours=0)
            collect(**kw)
            client.response_override[REPAIR] = Reply(REPAIR, status=304)
            client.response_override[BUILDING] = Reply(BUILDING, status=304)
            result = collect(**kw)
            self.assertEqual(result["unchanged"], 2)
            self.assertEqual(result["downloaded"], 0)

    def test_html_instead_of_pdf_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            client = FakeSession(pdfs={REPAIR: b"<html>captcha</html>", BUILDING: b"%PDF-1.7\nokay\n%%EOF"})
            result = collect(root / "pdfs", root / "state.sqlite", pages=(PAGE,), session=client)
            self.assertEqual(result["downloaded"], 1)
            self.assertIn(REPAIR, result["download_errors"])
            self.assertEqual(len(list((root / "pdfs").glob("*.pdf"))), 1)

    def test_offsite_redirect_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            client = FakeSession()
            client.response_override[REPAIR] = Reply(REPAIR, status=302, headers={"Location": "https://evil.example/x.pdf"})
            result = collect(root / "pdfs", root / "state.sqlite", pages=(PAGE,), session=client)
            self.assertIn(REPAIR, result["download_errors"])

    def test_limit_tracks_deferred(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            client = FakeSession()
            result = collect(root / "pdfs", root / "state.sqlite", limit=1, pages=(PAGE,), session=client)
            self.assertEqual(result["downloaded"], 1)
            self.assertEqual(result["deferred"], 1)
            second = collect(root / "pdfs", root / "state.sqlite", limit=1, pages=(PAGE,), session=client)
            self.assertEqual(second["downloaded"], 1)
            self.assertEqual(second["deferred"], 0)

    def test_partial_http_response_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            client = FakeSession()
            client.response_override[REPAIR] = Reply(REPAIR, b"%PDF-1.7\npartial", status=206)
            result = collect(root / "pdfs", root / "state.sqlite", pages=(PAGE,), session=client)
            self.assertIn("partial", result["download_errors"][REPAIR])
            self.assertEqual(result["status"], "PARTIAL")

    def test_deleted_pdf_gets_recovered(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            client = FakeSession()
            kw = dict(output_dir=root / "pdfs", state_db=root / "state.sqlite", pages=(PAGE,), session=client)
            collect(**kw)
            (root / "pdfs" / next(p.name for p in (root / "pdfs").glob("*.pdf") if p.read_bytes().find(b"repair") != -1)).unlink()
            result = collect(**kw)
            self.assertEqual(result["updated"], 1)
            self.assertEqual(len(list((root / "pdfs").glob("*.pdf"))), 2)

    def test_content_length_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            client = FakeSession()
            client.response_override[REPAIR] = Reply(REPAIR, b"%PDF-1.7\n%%EOF", headers={"Content-Type": "application/pdf", "Content-Length": "999"})
            result = collect(root / "pdfs", root / "state.sqlite", pages=(PAGE,), session=client)
            self.assertIn("Content-Length", result["download_errors"][REPAIR])

    def test_unavailable_listing_not_silent_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            client = FakeSession()
            client.response_override[PAGE] = Reply(PAGE, b"temporary", status=503)
            result = collect(root / "pdfs", root / "state.sqlite", pages=(PAGE,), session=client)
            self.assertEqual(result["pages_ok"], 0)
            self.assertIn(PAGE, result["page_errors"])
            self.assertEqual(result["downloaded"], 0)

    def test_invalid_pdf_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            client = FakeSession(pdfs={REPAIR: b"%PDF-1.7\n" + b"a" * 1024 * 1024})
            client.listing = HTML.replace(b"/PDF/FCRA/1.20260626_NewBuidlidng_Requirement_withPlan.pdf", b"/PDF/FCRA/ignored.txt")
            result = collect(root / "pdfs", root / "state.sqlite", pages=(PAGE,), session=client, max_pdf_mb=1)
            self.assertIn(REPAIR, result["download_errors"])


if __name__ == "__main__":
    unittest.main()
