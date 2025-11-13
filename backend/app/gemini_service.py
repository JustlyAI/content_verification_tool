"""
Gemini AI verification service for content verification
"""
import os
import time
import asyncio
import json
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from termcolor import cprint
from pathlib import Path

from google import genai
from google.genai import types

from .models import (
    DocumentChunk,
    DocumentMetadata,
    VerificationResult
)


class GeminiVerificationService:
    """Service for AI-powered document verification using Google Gemini"""

    def __init__(self):
        """Initialize the Gemini verification service"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            cprint("⚠️  GEMINI_API_KEY not found in environment variables", "yellow")
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)
            cprint("✓ Gemini client initialized", "green")

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

        store_name = f"verification_case_{case_id}_{int(time.time())}"

        try:
            cprint(f"[Gemini] Creating File Search store: {store_name}", "cyan")

            # Create the corpus (store)
            corpus = self.client.corpora.create(
                name=store_name,
                display_name=f"Verification Case {case_id}"
            )

            cprint(f"[Gemini] ✓ Store created: {corpus.name}", "green")
            return corpus.name, store_name

        except Exception as e:
            cprint(f"[Gemini] ✗ Error creating store: {e}", "red")
            raise

    def generate_metadata(
        self, file_path: str, filename: str, case_context: str
    ) -> DocumentMetadata:
        """
        Generate metadata for a reference document using Gemini

        Args:
            file_path: Path to the document file
            filename: Original filename
            case_context: Context about the verification case

        Returns:
            DocumentMetadata object with AI-generated metadata
        """
        if not self.client:
            raise ValueError("Gemini client not initialized - check GEMINI_API_KEY")

        try:
            cprint(f"[Gemini] Generating metadata for {filename}", "cyan")

            # Upload file to Gemini for analysis
            uploaded_file = self.client.files.upload(file_path=file_path)

            # Wait for file to be processed
            cprint(f"[Gemini] Waiting for file processing...", "cyan")
            while uploaded_file.state == "PROCESSING":
                time.sleep(1)
                uploaded_file = self.client.files.get(name=uploaded_file.name)

            if uploaded_file.state == "FAILED":
                raise ValueError(f"File processing failed: {uploaded_file.error}")

            # Generate metadata using Gemini Flash
            prompt = f"""Analyze this document in the context of: {case_context}

Provide a JSON response with the following fields:
- summary: A 2-3 sentence summary of the document
- contextualization: How this document relates to the case context
- document_type: The type of document (e.g., contract, invoice, receipt, report)
- keywords: A list of 5-10 key terms or concepts from the document

Return only valid JSON, no markdown formatting."""

            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[uploaded_file, prompt]
            )

            # Parse response
            response_text = response.text.strip()
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()

            metadata_dict = json.loads(response_text)

            # Clean up the uploaded file
            self.client.files.delete(name=uploaded_file.name)

            document_id = hashlib.md5(filename.encode()).hexdigest()

            metadata = DocumentMetadata(
                document_id=document_id,
                filename=filename,
                summary=metadata_dict.get("summary", ""),
                contextualization=metadata_dict.get("contextualization", ""),
                document_type=metadata_dict.get("document_type", "document"),
                keywords=metadata_dict.get("keywords", []),
                generated_at=datetime.now()
            )

            cprint(f"[Gemini] ✓ Metadata generated for {filename}", "green")
            return metadata

        except Exception as e:
            cprint(f"[Gemini] ✗ Error generating metadata: {e}", "red")
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
            Document name from the upload
        """
        if not self.client:
            raise ValueError("Gemini client not initialized - check GEMINI_API_KEY")

        try:
            cprint(f"[Gemini] Uploading {metadata.filename} to store {store_name}", "cyan")

            # Create metadata dict for the document
            custom_metadata = [
                types.CustomMetadata(
                    key="summary",
                    string_value=metadata.summary[:500]  # Limit to 500 chars
                ),
                types.CustomMetadata(
                    key="document_type",
                    string_value=metadata.document_type
                ),
                types.CustomMetadata(
                    key="keywords",
                    string_list_value=types.StringList(values=metadata.keywords[:10])
                )
            ]

            # Upload document to corpus
            document = self.client.corpora.documents.create(
                corpus=store_name,
                display_name=metadata.filename,
                custom_metadata=custom_metadata
            )

            # Upload the actual file as a chunk
            chunk = self.client.corpora.documents.chunks.create(
                document=document.name,
                data=types.ChunkData(
                    string_value=open(file_path, 'rb').read().decode('utf-8', errors='ignore')
                ),
                custom_metadata=custom_metadata
            )

            cprint(f"[Gemini] ✓ Uploaded {metadata.filename} to store", "green")
            return document.name

        except Exception as e:
            cprint(f"[Gemini] ✗ Error uploading to store: {e}", "red")
            raise

    def verify_chunk(
        self, chunk: DocumentChunk, store_name: str, case_context: str
    ) -> DocumentChunk:
        """
        Verify a single chunk against the File Search store

        Args:
            chunk: DocumentChunk to verify
            store_name: Name of the File Search store
            case_context: Context about the verification case

        Returns:
            DocumentChunk with verification fields populated
        """
        if not self.client:
            raise ValueError("Gemini client not initialized - check GEMINI_API_KEY")

        try:
            # Build verification prompt
            prompt = f"""Context: {case_context}

Verify this content against the reference documents:

Page {chunk.page_number}, Item {chunk.item_number}:
"{chunk.text}"

Please verify if this content appears in or is supported by the reference documents. Provide your response in JSON format with these fields:

1. verified: (boolean) true if the content is found/supported, false otherwise
2. confidence_score: (integer 1-10) how confident you are in this verification
3. verification_source: (string) citation with document name and location (e.g., "Contract.pdf, Section 2.1")
4. verification_note: (string) brief explanation of your reasoning
5. citations: (array) list of specific passages that support this verification, each with "title" and "excerpt" fields

Return only valid JSON, no markdown formatting."""

            # Configure tool with grounding
            tool = types.Tool(
                google_search_retrieval=types.GoogleSearchRetrieval(
                    dynamic_retrieval_config=types.DynamicRetrievalConfig(
                        mode="MODE_DYNAMIC"
                    )
                )
            )

            # Generate verification using Gemini Flash
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,  # Low temperature for consistent results
                    response_mime_type="application/json"
                )
            )

            # Parse response
            result = json.loads(response.text)

            # Update chunk with verification results
            chunk.verified = result.get("verified", False)
            chunk.verification_score = min(10, max(1, result.get("confidence_score", 5)))
            chunk.verification_source = result.get("verification_source", "No source found")
            chunk.verification_note = result.get("verification_note", "")
            chunk.citations = result.get("citations", [])

            return chunk

        except Exception as e:
            cprint(f"[Gemini] ✗ Error verifying chunk: {e}", "yellow")
            # Return chunk with unverified status
            chunk.verified = False
            chunk.verification_score = 1
            chunk.verification_source = "Error during verification"
            chunk.verification_note = f"Verification failed: {str(e)}"
            chunk.citations = []
            return chunk

    async def verify_batch(
        self,
        chunks: List[DocumentChunk],
        store_name: str,
        case_context: str,
        batch_size: int = 5,
    ) -> List[DocumentChunk]:
        """
        Verify multiple chunks in batches with rate limiting

        Args:
            chunks: List of DocumentChunk objects to verify
            store_name: Name of the File Search store
            case_context: Context about the verification case
            batch_size: Number of chunks to process concurrently

        Returns:
            List of DocumentChunk objects with verification results
        """
        if not self.client:
            raise ValueError("Gemini client not initialized - check GEMINI_API_KEY")

        cprint(f"[Gemini] Starting batch verification: {len(chunks)} chunks", "cyan")

        verified_chunks = []
        total_chunks = len(chunks)

        # Process chunks in batches
        for batch_start in range(0, total_chunks, batch_size):
            batch_end = min(batch_start + batch_size, total_chunks)
            batch = chunks[batch_start:batch_end]

            cprint(f"[Gemini] Processing batch {batch_start // batch_size + 1}: chunks {batch_start + 1}-{batch_end} of {total_chunks}", "cyan")

            # Process each chunk in the batch
            batch_results = []
            for chunk in batch:
                try:
                    verified_chunk = self.verify_chunk(chunk, store_name, case_context)
                    batch_results.append(verified_chunk)

                    # Small delay between individual verifications to avoid rate limits
                    await asyncio.sleep(0.2)

                except Exception as e:
                    cprint(f"[Gemini] Error verifying chunk {chunk.item_number}: {e}", "yellow")
                    # Add unverified chunk
                    chunk.verified = False
                    chunk.verification_score = 1
                    chunk.verification_source = "Error"
                    chunk.verification_note = f"Verification failed: {str(e)}"
                    batch_results.append(chunk)

            verified_chunks.extend(batch_results)

            # Delay between batches to respect rate limits
            if batch_end < total_chunks:
                cprint(f"[Gemini] Batch complete. Waiting 1 second before next batch...", "cyan")
                await asyncio.sleep(1)

        verified_count = sum(1 for c in verified_chunks if c.verified)
        cprint(f"[Gemini] ✓ Batch verification complete: {verified_count}/{total_chunks} chunks verified", "green")

        return verified_chunks


# Singleton instance
gemini_service = GeminiVerificationService()
