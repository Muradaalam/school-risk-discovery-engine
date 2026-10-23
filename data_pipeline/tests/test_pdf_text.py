
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from pypdf import PdfWriter

from data_pipeline.extraction.pdf_text import extract_pdf_text


class TestPdfTextExtraction(unittest.TestCase):

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.pdf = Path(self.folder.name) / "schools.pdf"
        self.output = Path(self.folder.name) / "pages.jsonl"

        writer = PdfWriter()
        writer.add_blank_page(width=300, height=400)
        writer.add_blank_page(width=300, height=400)

        with self.pdf.open("wb") as file:
            writer.write(file)

    def test_extracts_pages_and_numbers(self):
        result = extract_pdf_text(self.pdf, self.output, limit=2)
        rows = [json.loads(line) for line in self.output.read_text().splitlines()]

        self.assertEqual(result["total_pages"], 2)
        self.assertEqual([row["page_number"] for row in rows], [1, 2])
        self.assertEqual(result["pages_with_text"], 0)
        self.assertFalse(rows[0]["has_text"])

    @patch("data_pipeline.extraction.pdf_text.PdfReader")
    def test_preserves_extracted_text(self, mock_reader):
        page = MagicMock()
        page.extract_text.return_value = "Government School Rampura\nजिला पाली"
        page.get.return_value = object()
        mock_reader.return_value.pages = [page]

        extract_pdf_text(self.pdf, self.output)
        row = json.loads(self.output.read_text().strip())

        self.assertIn("Government School Rampura", row["text"])
        self.assertIn("जिला पाली", row["text"])
        self.assertTrue(row["has_text"])

    def test_rejects_checksum_mismatch(self):
        self.pdf.with_suffix(".pdf.json").write_text(json.dumps({"sha256": "wrong"}))

        with self.assertRaises(ValueError):
            extract_pdf_text(self.pdf, self.output)

        self.assertFalse(self.output.exists())

    def test_preserves_source_metadata(self):
        sha = hashlib.sha256(self.pdf.read_bytes()).hexdigest()

        self.pdf.with_suffix(".pdf.json").write_text(json.dumps({
            "source_id": "TEST_SOURCE",
            "source_url": "https://example.org/schools.pdf",
            "sha256": sha
        }))

        extract_pdf_text(self.pdf, self.output, limit=1)
        row = json.loads(self.output.read_text().strip())

        self.assertEqual(row["source_id"], "TEST_SOURCE")
        self.assertEqual(row["source_url"], "https://example.org/schools.pdf")
        self.assertEqual(row["pdf_sha256"], sha)

    def test_rejects_invalid_page_range(self):
        with self.assertRaises(ValueError):
            extract_pdf_text(self.pdf, self.output, start_page=3)

        with self.assertRaises(ValueError):
            extract_pdf_text(self.pdf, self.output, limit=0)

    def test_does_not_overwrite_output(self):
        self.output.write_text("existing")

        with self.assertRaises(FileExistsError):
            extract_pdf_text(self.pdf, self.output)

        self.assertEqual(self.output.read_text(), "existing")


if __name__ == "__main__":
    unittest.main()
