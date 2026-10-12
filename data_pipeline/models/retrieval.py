from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4


class RetrievalStatus(str, Enum):
    SUCCESS = "SUCCESS"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"


@dataclass
class SourceRetrieval:
    source_id: str
    status: RetrievalStatus
    record_count: int
    error: Optional[str] = None
    retrieved_at: Optional[datetime] = None
    retrieval_id: Optional[str] = None

    def __post_init__(self):
        if self.record_count < 0:
            raise ValueError("record_count cannot be negative")

        if self.retrieved_at is None:
            self.retrieved_at = datetime.now(timezone.utc)

        if self.retrieval_id is None:
            self.retrieval_id = f"RET_{uuid4().hex[:12].upper()}"

    @property
    def is_empty_success(self) -> bool:
        return (
            self.status == RetrievalStatus.SUCCESS
            and self.record_count == 0
        )
