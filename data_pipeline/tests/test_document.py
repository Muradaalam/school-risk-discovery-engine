import unittest

from data_pipeline.models.document import Document, DocumentType


class TestDocument(unittest.TestCase):

    def test_document_creation(self):
        document = Document(
            source_id="RAJ_EPROC",
            title="School Repair Tender",
            url="https://example.org/tender/123",
            document_type=DocumentType.TENDER,
            raw_content=b"Sample tender content",
        )

        self.assertTrue(document.document_id.startswith("DOC_"))
        self.assertIsNotNone(document.retrieved_at)
        self.assertEqual(len(document.content_hash), 64)

    def test_identical_content_has_same_hash(self):
        first = Document(
            source_id="RAJ_EPROC",
            title="Tender A",
            url="https://example.org/tender/a",
            document_type=DocumentType.TENDER,
            raw_content=b"Same content",
        )

        second = Document(
            source_id="RAJ_EPROC",
            title="Tender B",
            url="https://example.org/tender/b",
            document_type=DocumentType.TENDER,
            raw_content=b"Same content",
        )

        self.assertEqual(first.content_hash, second.content_hash)

    def test_different_content_has_different_hash(self):
        first = Document(
            source_id="RAJ_EPROC",
            title="Tender A",
            url="https://example.org/tender/a",
            document_type=DocumentType.TENDER,
            raw_content=b"Content A",
        )

        second = Document(
            source_id="RAJ_EPROC",
            title="Tender B",
            url="https://example.org/tender/b",
            document_type=DocumentType.TENDER,
            raw_content=b"Content B",
        )

        self.assertNotEqual(first.content_hash, second.content_hash)

    def test_invalid_url_rejected(self):
        with self.assertRaises(ValueError):
            Document(
                source_id="RAJ_EPROC",
                title="Tender",
                url="invalid-url",
                document_type=DocumentType.TENDER,
                raw_content=b"Content",
            )

    def test_non_bytes_content_rejected(self):
        with self.assertRaises(TypeError):
            Document(
                source_id="RAJ_EPROC",
                title="Tender",
                url="https://example.org/tender",
                document_type=DocumentType.TENDER,
                raw_content="Content",
            )


if __name__ == "__main__":
    unittest.main()