from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class FileType(str, Enum):
    DOCX = "docx"
    PDF = "pdf"
    IMAGE = "image"
    UNKNOWN = "unknown"

class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class FileRecord(SQLModel):
    id: str = Field(primary_key=True)
    session_id: str
    original_name: str
    file_type: FileType
    file_path: str
    file_size: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Session(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: ProcessingStatus = Field(default=ProcessingStatus.PENDING)

class Export(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    export_id: str = Field(unique=True, index=True)
    session_id: str
    pdf_path: str
    metadata_json: str
    warnings: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MetadataRequest(SQLModel):
    title: str
    author: str
    supervisor: Optional[str] = None
    year: int
    faculty: Optional[str] = None
    form: Optional[str] = None

class PrepareRequest(SQLModel):
    session_id: str
    order: List[str]
    metadata: MetadataRequest

class UploadResponse(SQLModel):
    session_id: str
    files: List[dict]

class PrepareResponse(SQLModel):
    export_id: str
    pdf_url: str
    metadata_url: str
    warnings: List[str] = []

