import unittest

from data_pipeline.models.retrieval import (
    RetrievalStatus,
    SourceRetrieval,
)


class TestSourceRetrieval(unittest.TestCase):

    def test_success_with_records(self):
        result = SourceRetrieval(
            source_id="RAJ_EPROC",
            status=RetrievalStatus.SUCCESS,
            record_count=5,
        )

        self.assertFalse(result.is_empty_success)

    def test_success_without_records(self):
        result = SourceRetrieval(
            source_id="RAJ_EPROC",
            status=RetrievalStatus.SUCCESS,
            record_count=0,
        )

        self.assertTrue(result.is_empty_success)

    def test_failure_is_not_empty_success(self):
        result = SourceRetrieval(
            source_id="RAJ_EPROC",
            status=RetrievalStatus.FAILED,
            record_count=0,
            error="Source unavailable",
        )

        self.assertFalse(result.is_empty_success)

    def test_negative_record_count_rejected(self):
        with self.assertRaises(ValueError):
            SourceRetrieval(
                source_id="RAJ_EPROC",
                status=RetrievalStatus.SUCCESS,
                record_count=-1,
            )


if __name__ == "__main__":
    unittest.main()
