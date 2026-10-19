
import unittest

from data_pipeline.models.document import Document, DocumentType
from data_pipeline.models.retrieval import SourceRetrieval, RetrievalStatus
from data_pipeline.sources.base import SourceAdapter, AcquisitionResult


class FakeSourceAdapter(SourceAdapter):

    def fetch(self) -> AcquisitionResult:
        document = Document(source_id=self.source_id,title="Sample School Report",url="https://example.org/report/1",document_type=DocumentType.WEB_PAGE,
                            raw_content=b"Sample school report")

        retrieval = SourceRetrieval(source_id=self.source_id,status=RetrievalStatus.SUCCESS,record_count=1)

        return AcquisitionResult(retrieval, [document])


class TestSourceAdapter(unittest.TestCase):

    def test_successful_acquisition(self):
        adapter = FakeSourceAdapter("TEST_SOURCE")
        result = adapter.fetch()

        self.assertEqual(result.retrieval.status, RetrievalStatus.SUCCESS)
        self.assertEqual(result.retrieval.record_count, 1)
        self.assertEqual(len(result.documents), 1)

    def test_empty_success(self):
        retrieval = SourceRetrieval("TEST_SOURCE", RetrievalStatus.SUCCESS, 0)
        result = AcquisitionResult(retrieval)

        self.assertTrue(result.retrieval.is_empty_success)
        self.assertEqual(len(result.documents), 0)

    def test_failed_retrieval(self):
        retrieval = SourceRetrieval("TEST_SOURCE", RetrievalStatus.FAILED, 0)
        result = AcquisitionResult(retrieval)

        self.assertFalse(result.retrieval.is_empty_success)

    def test_failed_retrieval_with_documents_rejected(self):
        document = Document("TEST_SOURCE", "Report", "https://example.org/report",DocumentType.WEB_PAGE, b"Content")

        retrieval = SourceRetrieval("TEST_SOURCE", RetrievalStatus.FAILED, 0)

        with self.assertRaises(ValueError):
            AcquisitionResult(retrieval, [document])

    def test_mismatched_source_rejected(self):
        document = Document("SOURCE_A", "Report", "https://example.org/report",DocumentType.WEB_PAGE, b"Content")

        retrieval = SourceRetrieval("SOURCE_B", RetrievalStatus.SUCCESS, 1)

        with self.assertRaises(ValueError):
            AcquisitionResult(retrieval, [document])

    def test_abstract_adapter_cannot_be_created(self):
        with self.assertRaises(TypeError):
            SourceAdapter("TEST_SOURCE")


if __name__ == "__main__":
    unittest.main()
