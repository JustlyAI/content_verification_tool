"""
Pydantic models for the Content Verification Tool
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ChunkingMode(str, Enum):
    """Splitting mode options"""

    PARAGRAPH = "paragraph"
    SENTENCE = "sentence"


class OutputFormat(str, Enum):
    """Output format options"""

    WORD_LANDSCAPE = "word_landscape"
    WORD_PORTRAIT = "word_portrait"
    EXCEL = "excel"
    CSV = "csv"
    JSON = "json"


class DocumentChunk(BaseModel):
    """Represents a single chunk with metadata"""

    page_number: int = Field(..., description="Page number where the chunk appears")
    item_number: str = Field(
        ..., description="Item number on the page (e.g., '1' or '1.2' for hierarchical)"
    )
    text: str = Field(..., description="The chunk text content")
    is_overlap: bool = Field(
        False, description="True if item continues from previous page"
    )

    # AI verification fields
    verified: Optional[bool] = Field(
        None, description="Whether the chunk was verified by AI"
    )
    verification_score: Optional[int] = Field(None, description="Confidence score 1-10")
    verification_source: Optional[str] = Field(
        None, description="Source citations for verification"
    )
    verification_note: Optional[str] = Field(None, description="AI reasoning and notes")
    citations: Optional[List[Dict[str, Any]]] = Field(
        None, description="Detailed citation objects"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "page_number": 1,
                "item_number": "1.1",
                "text": "This is a sample paragraph or sentence.",
                "is_overlap": False,
                "verified": True,
                "verification_score": 8,
                "verification_source": "Reference Doc A, page 5",
                "verification_note": "Verified against contract section 2.1",
                "citations": [{"title": "Reference Doc A", "excerpt": "matching text"}],
            }
        }


class UploadResponse(BaseModel):
    """Response from document upload"""

    document_id: str = Field(
        ..., description="Unique identifier for the uploaded document"
    )
    filename: str = Field(..., description="Original filename")
    page_count: int = Field(..., description="Number of pages in the document")
    file_size: int = Field(..., description="File size in bytes")
    message: str = Field(..., description="Status message")


class ChunkingRequest(BaseModel):
    """Request to chunk a document"""

    document_id: str = Field(..., description="Document ID from upload")
    splitting_mode: ChunkingMode = Field(..., description="Splitting mode to use")


class ChunkingResponse(BaseModel):
    """Response from document chunking"""

    document_id: str = Field(..., description="Document identifier")
    splitting_mode: ChunkingMode = Field(..., description="Splitting mode used")
    chunks: List[DocumentChunk] = Field(..., description="List of document chunks")
    total_chunks: int = Field(..., description="Total number of chunks")
    message: str = Field(..., description="Status message")


class ExportRequest(BaseModel):
    """Request to export verification document"""

    document_id: str = Field(..., description="Document ID from upload")
    splitting_mode: ChunkingMode = Field(..., description="Splitting mode to use")
    output_format: OutputFormat = Field(..., description="Output format")


class ExportResponse(BaseModel):
    """Response from document export"""

    document_id: str = Field(..., description="Document identifier")
    output_format: OutputFormat = Field(..., description="Format used")
    filename: str = Field(..., description="Generated filename")
    message: str = Field(..., description="Status message")


class ErrorResponse(BaseModel):
    """Error response model"""

    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")


# AI Verification Models


class DocumentMetadata(BaseModel):
    """Metadata for a reference document"""

    document_id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., description="Original filename")
    summary: str = Field(
        ...,
        max_length=256,
        description="AI-generated summary (max 256 chars for File Search)",
    )
    contextualization: str = Field(
        ..., description="How document relates to case context"
    )
    document_type: str = Field(
        ...,
        max_length=256,
        description="Type of document (max 256 chars for File Search)",
    )
    keywords: List[str] = Field(..., description="Key terms extracted from document")
    generated_at: datetime = Field(..., description="When metadata was generated")
    file_size_bytes: int = Field(..., description="File size in bytes")
    page_count: int = Field(..., description="Number of pages in document")


class VerificationResult(BaseModel):
    """Result from AI verification of a chunk"""

    verified: bool = Field(..., description="Whether the chunk was verified")
    verification_score: int = Field(
        ..., ge=1, le=10, description="Confidence score 1-10"
    )
    verification_source: str = Field(..., description="Source citations")
    verification_note: str = Field(..., description="AI reasoning and notes")
    citations: List[Dict[str, Any]] = Field(
        default_factory=list, description="Detailed citation objects"
    )
    verified_at: datetime = Field(..., description="Timestamp of verification")


class UploadReferencesRequest(BaseModel):
    """Request to upload reference documents"""

    case_context: Optional[str] = Field(None, description="Context about the verification case (optional)")


class UploadReferencesResponse(BaseModel):
    """Response from uploading reference documents"""

    store_id: str = Field(..., description="File Search store ID")
    store_name: str = Field(..., description="File Search store name")
    documents_uploaded: int = Field(..., description="Number of documents uploaded")
    metadata: List[DocumentMetadata] = Field(
        ..., description="Metadata for uploaded documents"
    )


class VerificationRequest(BaseModel):
    """Request to verify chunks against reference documents"""

    document_id: str = Field(..., description="Document ID to verify")
    store_id: str = Field(..., description="File Search store ID")
    case_context: Optional[str] = Field(None, description="Context about the verification case (optional)")
    splitting_mode: ChunkingMode = Field(..., description="Splitting mode used")


class VerificationResponse(BaseModel):
    """Response from chunk verification"""

    document_id: str = Field(..., description="Document identifier")
    verified_chunks: List[DocumentChunk] = Field(
        ..., description="Chunks with verification results"
    )
    total_verified: int = Field(..., description="Number of chunks verified")
    total_chunks: int = Field(..., description="Total number of chunks")
    processing_time_seconds: float = Field(
        ..., description="Time taken for verification"
    )
    store_id: str = Field(..., description="File Search store ID used")
