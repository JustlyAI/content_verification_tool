"""
Corpus management service for Gemini File Search
Handles reference document uploads and store management
"""

import os
import time
import json
import hashlib
from typing import Tuple
from datetime import datetime
from termcolor import cprint
from dotenv import load_dotenv

from google import genai
from google.genai import types

load_dotenv()

from app.models import DocumentMetadata


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

    def _generate_metadata_from_file(
        self, uploaded_file, filename: str, case_context: str
    ) -> DocumentMetadata:
        """
        Generate metadata for a reference document from an already-uploaded file

        Args:
            uploaded_file: Already uploaded Gemini file object
            filename: Original filename
            case_context: Context about the verification case

        Returns:
            DocumentMetadata object with AI-generated metadata
        """
        try:
            cprint(f"[Corpus] Generating metadata for {filename}", "cyan")

            prompt = f"""Analyze this document in the context of: {case_context}

Provide a JSON response with the following fields:
- summary: A 2-3 sentence summary of the document
- contextualization: How this document relates to the case context
- document_type: The type of document (e.g., contract, invoice, receipt, report)
- keywords: A list of 5-10 key terms or concepts from the document

Return only valid JSON, no markdown formatting."""

            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite", contents=[uploaded_file, prompt]
            )

            response_text = response.text.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()

            metadata_dict = json.loads(response_text)

            document_id = hashlib.md5(filename.encode()).hexdigest()

            metadata = DocumentMetadata(
                document_id=document_id,
                filename=filename,
                summary=metadata_dict.get("summary", ""),
                contextualization=metadata_dict.get("contextualization", ""),
                document_type=metadata_dict.get("document_type", "document"),
                keywords=metadata_dict.get("keywords", []),
                generated_at=datetime.now(),
            )

            cprint(f"[Corpus] ✓ Metadata generated for {filename}", "green")
            return metadata

        except Exception as e:
            cprint(f"[Corpus] ✗ Error generating metadata: {e}", "red")
            raise

    def upload_reference_with_metadata(
        self, file_path: str, filename: str, store_name: str, case_context: str
    ) -> Tuple[DocumentMetadata, str]:
        """
        Upload a reference document with metadata generation (optimized - single upload)

        Args:
            file_path: Path to the file to upload
            filename: Original filename
            store_name: Name of the File Search store
            case_context: Context about the verification case

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
                uploaded_file, filename, case_context
            )

            # Create custom metadata for file search store
            custom_metadata = [
                types.CustomMetadata(
                    key="summary",
                    string_value=metadata.summary[:500],
                ),
                types.CustomMetadata(
                    key="document_type", string_value=metadata.document_type
                ),
                types.CustomMetadata(
                    key="keywords",
                    string_list_value=types.StringList(values=metadata.keywords[:10]),
                ),
            ]

            # Add file to File Search store (reusing uploaded file)
            cprint(
                f"[Corpus] Adding file to File Search store (reusing uploaded file)...",
                "cyan",
            )
            operation = self.client.file_search_stores.upload_to_file_search_store(
                file_search_store_name=store_name,
                file=uploaded_file,
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
                operation = self.client.operations.get(name=operation.name)

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
                    string_value=metadata.summary[:500],
                ),
                types.CustomMetadata(
                    key="document_type", string_value=metadata.document_type
                ),
                types.CustomMetadata(
                    key="keywords",
                    string_list_value=types.StringList(values=metadata.keywords[:10]),
                ),
            ]

            cprint(f"[Corpus] Adding file to File Search store...", "cyan")
            operation = self.client.file_search_stores.upload_to_file_search_store(
                file_search_store_name=store_name,
                file=uploaded_file,
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
                operation = self.client.operations.get(name=operation.name)
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
