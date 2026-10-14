from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from typing import Optional
from uuid import uuid4


class DocumentType(str, Enum):
    WEB_PAGE = "WEB_PAGE"
    PDF = "PDF"
    TENDER = "TENDER"
    INSPECTION_REPORT = "INSPECTION_REPORT"
    NOTICE = "NOTICE"
    DATASET_RECORD = "DATASET_RECORD"
    NEWS_ARTICLE = "NEWS_ARTICLE"
    OTHER = "OTHER"


@dataclass
class Document:
    source_id: str
    title: str
    url: str
    document_type: DocumentType
    raw_content: bytes

    published_at: Optional[datetime] = None
    retrieved_at: Optional[datetime] = None
    document_id: Optional[str] = None
    content_hash: Optional[str] = None

    def __post_init__(self):
        if not self.source_id.strip():
            raise ValueError("source_id cannot be empty")

        if not self.url.startswith(("https://", "http://")):
            raise ValueError("Document URL must use HTTP or HTTPS")

        if not isinstance(self.raw_content, bytes):
            raise TypeError("raw_content must be bytes")

        if self.retrieved_at is None:
            self.retrieved_at = datetime.now(timezone.utc)

        if self.document_id is None:
            self.document_id = f"DOC_{uuid4().hex[:12].upper()}"

        if self.content_hash is None:
            self.content_hash = sha256(self.raw_content).hexdigest()