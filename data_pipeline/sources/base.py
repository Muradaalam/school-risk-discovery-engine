
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from data_pipeline.models.document import Document
from data_pipeline.models.retrieval import SourceRetrieval, RetrievalStatus


@dataclass
class AcquisitionResult:
    retrieval: SourceRetrieval
    documents: list[Document] = field(default_factory=list)

    def __post_init__(self):
        if self.retrieval.status == RetrievalStatus.FAILED and self.documents:
            raise ValueError("Failed retrieval cannot contain documents")

        for document in self.documents:
            if document.source_id != self.retrieval.source_id:
                raise ValueError("Document source does not match retrieval source")


class SourceAdapter(ABC):

    def __init__(self, source_id: str):
        if not source_id.strip():
            raise ValueError("source_id cannot be empty")

        self.source_id = source_id

    @abstractmethod
    def fetch(self) -> AcquisitionResult:
        pass
