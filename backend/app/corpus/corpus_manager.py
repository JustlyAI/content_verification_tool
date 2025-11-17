"""
Corpus management service for Gemini File Search
Handles reference document uploads and store management
"""

import os
import time
import json
import hashlib
from typing import Tuple, List, Optional
from datetime import datetime
from pathlib import Path
from termcolor import cprint
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from google import genai
from google.genai import types
from pypdf import PdfReader

load_dotenv()

from app.models import DocumentMetadata


def _count_pages_simple(file_path: str) -> int:
    """
    Simple page counter for PDF and DOCX files

    Args:
        file_path: Path to the file

    Returns:
        Number of pages (0 if unable to determine)
    """
    try:
        suffix = Path(file_path).suffix.lower()

        if suffix == '.pdf':
            # Count PDF pages using pypdf
            try:
                with open(file_path, 'rb') as f:
                    reader = PdfReader(f)
                    return len(reader.pages)
            except Exception as e:
                cprint(f"[Corpus] Warning: Failed to count PDF pages: {e}", "yellow")
                return 0

        elif suffix in ['.docx', '.doc']:
            # Try to count DOCX pages (rough estimate based on content)
            try:
                from docx import Document
                doc = Document(file_path)
                # Rough estimate: assume 500 words per page
                word_count = sum(len(paragraph.text.split()) for paragraph in doc.paragraphs)
                return max(1, word_count // 500)
            except ImportError:
                # python-docx not available, return 0
                return 0
            except Exception:
                # Failed to read DOCX
                return 0
        else:
            return 0

    except Exception:
        return 0


class MetadataResponse(BaseModel):
    """Response schema for AI-generated metadata (subset of DocumentMetadata)"""
    summary: str = Field(description="2-3 sentence summary of the document")
    contextualization: str = Field(description="Relationship to the provided case context")
    document_type: str = Field(description="Document classification (e.g., contract, invoice)")
    keywords: List[str] = Field(description="Key concepts extracted from the document")


class CorpusManager:
    """Service for managing Gemini File Search corpus and reference documents"""

    def __init__(self):
        """Initialize the corpus manager"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            cprint("⚠️  GEMINI_API_KEY not found in environment variables", "yellow")
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)
            cprint("✓ Corpus manager initialized", "green")

    def create_store(self, case_id: str) -> Tuple[str, str]:
        """
        Create a File Search store for reference documents

        Args:
            case_id: Unique identifier for the verification case

        Returns:
            Tuple of (store_id, store_name)
        """
        if not self.client:
            raise ValueError("Gemini client not initialized - check GEMINI_API_KEY")

        display_name = f"Verification Case {case_id} - {int(time.time())}"

        try:
            cprint(f"[Corpus] Creating File Search store: {display_name}", "cyan")

            store = self.client.file_search_stores.create(
                config={"display_name": display_name}
            )

            cprint(f"[Corpus] ✓ Store created: {store.name}", "green")
            cprint(f"[Corpus]   Display Name: {store.display_name}", "cyan")
            return store.name, store.display_name

        except Exception as e:
            cprint(f"[Corpus] ✗ Error creating store: {e}", "red")
            raise

    def delete_store(self, store_id: str) -> bool:
        """
        Delete a File Search store and all its documents

        Args:
            store_id: ID of the store to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        if not self.client:
            raise ValueError("Gemini client not initialized - check GEMINI_API_KEY")

        try:
            cprint(f"[Corpus] Deleting File Search store: {store_id}", "cyan")

            # Delete the store with force flag to delete all documents
            self.client.file_search_stores.delete(
                name=store_id,
                config={'force': True}
            )

            cprint(f"[Corpus] ✓ Store deleted successfully: {store_id}", "green")
            return True

        except Exception as e:
            cprint(f"[Corpus] ✗ Error deleting store: {e}", "red")
            return False

    def _generate_metadata_from_file(
        self, uploaded_file, filename: str, case_context: Optional[str], file_path: str
    ) -> DocumentMetadata:
        """
        Generate metadata for a reference document from an already-uploaded file

        Args:
            uploaded_file: Already uploaded Gemini file object
            filename: Original filename
            case_context: Context about the verification case (optional)
            file_path: Path to the file (for extracting size and page count)

        Returns:
            DocumentMetadata object with AI-generated metadata
        """
        try:
            cprint(f"[Corpus] Generating metadata for {filename}", "cyan")

            # Build prompt with optional case context
            if case_context:
                context_instruction = f"Analyze this document in the context of: {case_context}\n\n"
                contextualization_field = "- contextualization: How this document relates to the case context"
            else:
                context_instruction = "Analyze this document.\n\n"
                contextualization_field = "- contextualization: General description of the document's purpose and key topics"

            prompt = f"""{context_instruction}Provide a JSON response with the following fields:
- summary: A 2-3 sentence summary of the document
{contextualization_field}
- document_type: The type of document (e.g., contract, invoice, receipt, report)
- keywords: A list of 5-10 key terms or concepts from the document

Return only valid JSON, no markdown formatting."""

            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=[uploaded_file, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=MetadataResponse,
                ),
            )

            # Use parsed attribute if available, otherwise parse JSON
            has_parsed = hasattr(response, "parsed") and response.parsed is not None
            metadata_response = (
                response.parsed
                if has_parsed
                else MetadataResponse(**json.loads(response.text))
            )

            document_id = hashlib.md5(filename.encode()).hexdigest()

            # Extract file size and page count
            file_size_bytes = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            page_count = _count_pages_simple(file_path)

            metadata = DocumentMetadata(
                document_id=document_id,
                filename=filename,
                summary=metadata_response.summary[:256],  # Truncate to API limit
                contextualization=metadata_response.contextualization,
                document_type=metadata_response.document_type[:256],  # Truncate to API limit
                keywords=metadata_response.keywords,
                generated_at=datetime.now(),
                file_size_bytes=file_size_bytes,
                page_count=page_count,
            )

            cprint(f"[Corpus] ✓ Metadata generated for {filename} ({page_count} pages, {file_size_bytes/1024:.1f} KB)", "green")
            return metadata

        except Exception as e:
            cprint(f"[Corpus] ✗ Error generating metadata: {e}", "red")
            raise

    def generate_metadata(
        self, file_path: str, filename: str, case_context: Optional[str] = None
    ) -> DocumentMetadata:
        """
        Generate metadata for a reference document from a file path

        Args:
            file_path: Path to the file
            filename: Original filename
            case_context: Context about the verification case (optional)

        Returns:
            DocumentMetadata object with AI-generated metadata
        """
        if not self.client:
            raise ValueError("Gemini client not initialized - check GEMINI_API_KEY")

        try:
            # Upload file
            uploaded_file = self.client.files.upload(file=file_path)
            cprint(f"[Corpus] File uploaded for metadata: {uploaded_file.name}", "cyan")

            # Wait for file processing
            while uploaded_file.state == "PROCESSING":
                time.sleep(1)
                uploaded_file = self.client.files.get(name=uploaded_file.name)

            if uploaded_file.state == "FAILED":
                raise ValueError(
                    f"File processing failed: {getattr(uploaded_file, 'error', 'Unknown error')}"
                )

            # Generate metadata
            metadata = self._generate_metadata_from_file(
                uploaded_file, filename, case_context, file_path
            )

            # Clean up uploaded file
            self.client.files.delete(name=uploaded_file.name)
            cprint(f"[Corpus] ✓ File cleaned up: {uploaded_file.name}", "cyan")

            return metadata

        except Exception as e:
            cprint(f"[Corpus] ✗ Error generating metadata: {e}", "red")
            raise

    def upload_reference_with_metadata(
        self, file_path: str, filename: str, store_name: str, case_context: Optional[str] = None
    ) -> Tuple[DocumentMetadata, str]:
        """
        Upload a reference document with metadata generation (optimized - single upload)

        Args:
            file_path: Path to the file to upload
            filename: Original filename
            store_name: Name of the File Search store
            case_context: Context about the verification case (optional)

        Returns:
            Tuple of (DocumentMetadata, uploaded_file_name)
        """
        if not self.client:
            raise ValueError("Gemini client not initialized - check GEMINI_API_KEY")

        try:
            cprint(
                f"[Corpus] Uploading and processing {filename} (optimized flow)", "cyan"
            )

            # Upload file once
            uploaded_file = self.client.files.upload(file=file_path)
            cprint(f"[Corpus] File uploaded: {uploaded_file.name}", "cyan")

            # Wait for file processing
            cprint(f"[Corpus] Waiting for file to be processed...", "cyan")
            while uploaded_file.state == "PROCESSING":
                time.sleep(1)
                uploaded_file = self.client.files.get(name=uploaded_file.name)

            if uploaded_file.state == "FAILED":
                raise ValueError(
                    f"File processing failed: {getattr(uploaded_file, 'error', 'Unknown error')}"
                )

            cprint(f"[Corpus] File processed successfully", "green")

            # Generate metadata using the uploaded file
            metadata = self._generate_metadata_from_file(
                uploaded_file, filename, case_context, file_path
            )

            # Create custom metadata for file search store
            custom_metadata = [
                types.CustomMetadata(
                    key="summary",
                    string_value=metadata.summary[:256],  # API limit is 256 chars
                ),
                types.CustomMetadata(
                    key="document_type", string_value=metadata.document_type[:256]
                ),
                types.CustomMetadata(
                    key="keywords",
                    string_list_value=types.StringList(values=metadata.keywords[:10]),
                ),
            ]

            # Add file to File Search store
            cprint(
                f"[Corpus] Adding file to File Search store...",
                "cyan",
            )
            operation = self.client.file_search_stores.upload_to_file_search_store(
                file_search_store_name=store_name,
                file=file_path,
                config={
                    "custom_metadata": custom_metadata,
                    "display_name": metadata.filename,
                },
            )

            # Wait for indexing to complete
            cprint(f"[Corpus] Waiting for indexing to complete...", "cyan")
            max_wait = 60
            elapsed = 0
            while not operation.done and elapsed < max_wait:
                time.sleep(2)
                elapsed += 2
                operation = self.client.operations.get(operation)

            if not operation.done:
                cprint(
                    f"[Corpus] ⚠️  Indexing timeout, but file may still be processing",
                    "yellow",
                )
            elif operation.error:
                raise ValueError(f"Upload operation failed: {operation.error}")
            else:
                cprint(f"[Corpus] ✓ Indexing complete", "green")

            # Clean up - delete the file after both operations complete
            self.client.files.delete(name=uploaded_file.name)
            cprint(f"[Corpus] ✓ File cleaned up: {uploaded_file.name}", "cyan")

            cprint(
                f"[Corpus] ✓ Successfully processed {filename} with optimized flow",
                "green",
            )
            return metadata, uploaded_file.name

        except Exception as e:
            cprint(f"[Corpus] ✗ Error in optimized upload: {e}", "red")
            raise

    def upload_to_store(
        self, file_path: str, store_name: str, metadata: DocumentMetadata
    ) -> str:
        """
        Upload a file to a File Search store with metadata

        Args:
            file_path: Path to the file to upload
            store_name: Name of the File Search store
            metadata: DocumentMetadata to attach to the file

        Returns:
            File name from the upload
        """
        if not self.client:
            raise ValueError("Gemini client not initialized - check GEMINI_API_KEY")

        try:
            cprint(
                f"[Corpus] Uploading {metadata.filename} to store {store_name}", "cyan"
            )

            uploaded_file = self.client.files.upload(file=file_path)
            cprint(f"[Corpus] File uploaded: {uploaded_file.name}", "cyan")

            cprint(f"[Corpus] Waiting for file to be processed...", "cyan")
            while uploaded_file.state == "PROCESSING":
                time.sleep(1)
                uploaded_file = self.client.files.get(name=uploaded_file.name)

            if uploaded_file.state == "FAILED":
                raise ValueError(
                    f"File processing failed: {getattr(uploaded_file, 'error', 'Unknown error')}"
                )

            custom_metadata = [
                types.CustomMetadata(
                    key="summary",
                    string_value=metadata.summary[:256],  # API limit is 256 chars
                ),
                types.CustomMetadata(
                    key="document_type", string_value=metadata.document_type[:256]
                ),
                types.CustomMetadata(
                    key="keywords",
                    string_list_value=types.StringList(values=metadata.keywords[:10]),
                ),
            ]

            cprint(f"[Corpus] Adding file to File Search store...", "cyan")
            operation = self.client.file_search_stores.upload_to_file_search_store(
                file_search_store_name=store_name,
                file=file_path,
                config={
                    "custom_metadata": custom_metadata,
                    "display_name": metadata.filename,
                },
            )

            cprint(f"[Corpus] Waiting for indexing to complete...", "cyan")
            max_wait = 60
            elapsed = 0
            while not operation.done and elapsed < max_wait:
                time.sleep(2)
                elapsed += 2
                operation = self.client.operations.get(operation)
                cprint(f"[Corpus] Indexing... ({elapsed}s)", "cyan")

            if not operation.done:
                cprint(
                    f"[Corpus] ⚠️  Indexing timeout, but file may still be processing",
                    "yellow",
                )
            elif operation.error:
                raise ValueError(f"Upload operation failed: {operation.error}")
            else:
                cprint(f"[Corpus] ✓ Indexing complete", "green")

            cprint(f"[Corpus] ✓ Uploaded {metadata.filename} to store", "green")
            return uploaded_file.name

        except Exception as e:
            cprint(f"[Corpus] ✗ Error uploading to store: {e}", "red")
            raise


# Singleton instance
corpus_manager = CorpusManager()
