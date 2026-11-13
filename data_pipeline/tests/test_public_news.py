#this code is AI generated

import json
import tempfile
import unittest
from pathlib import Path

from data_pipeline.acquisition.public_news import article_details, collect, feed_entries


class Reply:
    def __init__(self, url, text):
        self.url = url
        self.text = text

    def raise_for_status(self):
        pass


class TestPublicNews(unittest.TestCase):
    def test_extract_html_and_rss(self):
        xml = """<rss><channel><item><title>School roof collapse</title>
        <link>https://newsonair.gov.in/abc/</link>
        <pubDate>Fri, 13 Nov 2026 08:00:00 GMT</pubDate>
        <description>Government school roof damaged</description>
        </item></channel></rss>"""
        found = feed_entries(xml, "AKASHVANI")
        self.assertEqual(found[0]["published_date"], "2026-11-13")

        html = """<html><head><meta property="og:title" content="School roof damage"></head>
        <body><div>Published: July 25, 2025</div><article><p>A government school roof collapsed.</p></article></body></html>"""
        extracted = article_details(html)
        self.assertEqual(extracted["title"], "School roof damage")
        self.assertEqual(extracted["published_date"], "2025-07-25")
        self.assertIn("roof collapsed", extracted["excerpt"])

    def test_seed_urls_without_feeds_are_incremental(self):
        from unittest.mock import Mock
        html = """<html><h1>School building collapse</h1>
        <article><p>A government school building collapsed in Jhalawar district.</p></article></html>"""
        session = Mock()
        session.get.side_effect = lambda url, timeout: Reply(url, html)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "reports.jsonl"
            first = collect(path, include_seed=True, session=session, skip_feeds=True)
            second = collect(path, include_seed=True, session=session, skip_feeds=True)
            self.assertEqual(first["new_reports"], 2)
            self.assertEqual(second["new_reports"], 0)
            self.assertEqual(len(path.read_text().splitlines()), 2)
            self.assertEqual(session.get.call_count, 2)

    def test_url_file_supported_sources_only(self):
        from unittest.mock import Mock
        html = "<h1>Government school roof collapsed</h1><article><p>School roof collapsed.</p></article>"
        session = Mock()
        session.get.side_effect = lambda url, timeout: Reply(url, html)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            urls = root / "urls.txt"
            urls.write_text("https://newsonair.gov.in/newreport/\nhttps://other.example/not-allowed/\n")
            result = collect(root / "reports.jsonl", session=session, skip_feeds=True, urls_file=urls)
            self.assertEqual(result["new_reports"], 1)
            self.assertEqual(result["unsupported_urls"], 1)


if __name__ == "__main__":
    unittest.main()
