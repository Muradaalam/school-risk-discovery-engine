# note : this code is written using AI

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from data_pipeline.acquisition.public_news import article_details, collect, feed_entries


class TestPublicNews(unittest.TestCase):

    def test_feed_and_article(self):
        xml = """<rss><channel><item>
        <title>Rajasthan school roof collapse</title>
        <link>https://newsonair.gov.in/example-school/</link>
        <pubDate>Fri, 13 Nov 2026 08:00:00 GMT</pubDate>
        <description>Government school roof damaged</description>
        </item></channel></rss>"""

        found = feed_entries(xml, "AKASHVANI")

        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["published_date"], "2026-11-13")

        html = """<html><head>
        <meta property="article:published_time" content="2026-11-13T08:00:00+05:30">
        </head><body><h1>School roof damaged</h1>
        <article><p>A government school roof collapsed in Rajasthan.</p></article>
        </body></html>"""

        self.assertIn("roof collapsed", article_details(html)["excerpt"])

    def test_collect_and_skip_existing(self):
        feed = """<rss><channel><item>
        <title>School roof collapse in Rajasthan</title>
        <link>https://newsonair.gov.in/example-school/</link>
        <description>school roof damaged</description>
        </item></channel></rss>"""

        html = """<html><h1>School roof collapse in Rajasthan</h1>
        <article><p>A school roof collapsed.</p></article></html>"""

        class Reply:
            def __init__(self, url, text):
                self.url, self.text = url, text

            def raise_for_status(self):
                pass

        client = Mock()

        def get(url, timeout):
            if "rss-feeds" in url:
                return Reply(url, feed)
            if "RssMain" in url:
                return Reply(url, "<rss><channel/></rss>")
            return Reply(url, html)

        client.get.side_effect = get

        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "reports.jsonl"

            first = collect(output, session=client)
            second = collect(output, session=client)

            self.assertEqual(first["new_reports"], 1)
            self.assertEqual(second["new_reports"], 0)

            records = [json.loads(line) for line in output.read_text().splitlines()]

            self.assertEqual(len(records), 1)
            self.assertEqual(
                records[0]["review_status"],
                "NEEDS_SCHOOL_IDENTITY_AND_CLAIM_REVIEW"
            )


if __name__ == "__main__":
    unittest.main()
