"""
Pydantic models for the Content Verification Tool
"""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ChunkingMode(str, Enum):
    """Chunking mode options"""
    PARAGRAPH = "paragraph"
    SENTENCE = "sentence"


class OutputFormat(str, Enum):
    """Output format options"""
    WORD_LANDSCAPE = "word_landscape"
    WORD_PORTRAIT = "word_portrait"
    EXCEL = "excel"
    CSV = "csv"


class DocumentChunk(BaseModel):
    """Represents a single chunk with metadata"""
    page_number: int = Field(..., description="Page number where the chunk appears")
    item_number: str = Field(..., description="Item number on the page (e.g., '1' or '1.2' for hierarchical)")
    text: str = Field(..., description="The chunk text content")
    is_overlap: bool = Field(False, description="True if item continues from previous page")

    class Config:
        json_schema_extra = {
            "example": {
                "page_number": 1,
                "item_number": "1.1",
                "text": "This is a sample paragraph or sentence.",
                "is_overlap": False
            }
        }


class UploadResponse(BaseModel):
    """Response from document upload"""
    document_id: str = Field(..., description="Unique identifier for the uploaded document")
    filename: str = Field(..., description="Original filename")
    page_count: int = Field(..., description="Number of pages in the document")
    file_size: int = Field(..., description="File size in bytes")
    message: str = Field(..., description="Status message")


class ChunkingRequest(BaseModel):
    """Request to chunk a document"""
    document_id: str = Field(..., description="Document ID from upload")
    chunking_mode: ChunkingMode = Field(..., description="Chunking mode to use")


class ChunkingResponse(BaseModel):
    """Response from document chunking"""
    document_id: str = Field(..., description="Document identifier")
    chunking_mode: ChunkingMode = Field(..., description="Chunking mode used")
    chunks: List[DocumentChunk] = Field(..., description="List of document chunks")
    total_chunks: int = Field(..., description="Total number of chunks")
    message: str = Field(..., description="Status message")


class ExportRequest(BaseModel):
    """Request to export verification document"""
    document_id: str = Field(..., description="Document ID from upload")
    chunking_mode: ChunkingMode = Field(..., description="Chunking mode to use")
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
