
# Note: half of the things in this file are developed with the help of AI 

import hashlib
import json
import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError

from data_pipeline.acquisition.pdf import download_pdf


class TestPdfDownload(unittest.TestCase):

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "schools.pdf"
        self.url = "https://example.org/schools.pdf"

    @patch("data_pipeline.acquisition.pdf.urlopen")
    def test_success_saves_pdf_and_metadata(self, mock_open):
        payload = b"%PDF-1.7\n" + b"school records" * 100
        mock_open.return_value.__enter__.return_value = BytesIO(payload)

        result = download_pdf(self.url, self.path)

        self.assertEqual(self.path.read_bytes(), payload)
        self.assertEqual(result["sha256"], hashlib.sha256(payload).hexdigest())
        self.assertEqual(result["size_bytes"], len(payload))

        metadata = json.loads(self.path.with_suffix(".pdf.json").read_text())
        self.assertEqual(metadata["source_url"], self.url)

    @patch("data_pipeline.acquisition.pdf.urlopen")
    def test_html_response_rejected_and_removed(self, mock_open):
        mock_open.return_value.__enter__.return_value = BytesIO(b"<html>Access denied</html>")

        with self.assertRaises(ValueError):
            download_pdf(self.url, self.path)

        self.assertFalse(self.path.exists())
        self.assertEqual(list(self.path.parent.glob(".pdf_*")), [])

    @patch("data_pipeline.acquisition.pdf.urlopen")
    def test_oversized_response_rejected(self, mock_open):
        mock_open.return_value.__enter__.return_value = BytesIO(b"%PDF-" + b"x" * 20)

        with self.assertRaises(ValueError):
            download_pdf(self.url, self.path, max_bytes=10)

        self.assertFalse(self.path.exists())

    @patch("data_pipeline.acquisition.pdf.urlopen")
    def test_network_error_does_not_create_file(self, mock_open):
        mock_open.side_effect = URLError("Connection failed")

        with self.assertRaises(URLError):
            download_pdf(self.url, self.path)

        self.assertFalse(self.path.exists())

    @patch("data_pipeline.acquisition.pdf.urlopen")
    def test_existing_file_is_not_overwritten(self, mock_open):
        self.path.write_bytes(b"existing original")

        with self.assertRaises(FileExistsError):
            download_pdf(self.url, self.path)

        self.assertEqual(self.path.read_bytes(), b"existing original")
        mock_open.assert_not_called()


if __name__ == "__main__":
    unittest.main()