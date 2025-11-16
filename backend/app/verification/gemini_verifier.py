"""
Gemini AI verification service for content verification
Handles chunk verification against reference corpus
"""

import os
import time
import asyncio
import json
from typing import List
from termcolor import cprint
from dotenv import load_dotenv

from google import genai
from google.genai import types

load_dotenv()

from app.models import DocumentChunk


class EmptyResponseError(Exception):
    """Raised when API returns empty response"""
    pass


class GeminiVerifier:
    """Service for AI-powered document chunk verification using Google Gemini"""

    def __init__(self):
        """Initialize the Gemini verifier"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            cprint("⚠️  GEMINI_API_KEY not found in environment variables", "yellow")
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)
            cprint("✓ Gemini verifier initialized", "green")

    def _retry_with_backoff(self, func, *args, max_retries=3, **kwargs):
        """
        Retry a function with exponential backoff

        Args:
            func: Function to retry
            max_retries: Maximum number of retry attempts
            *args, **kwargs: Arguments to pass to function

        Returns:
            Function result
        """
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise

                error_str = str(e).lower()
                is_retryable = (
                    isinstance(e, EmptyResponseError)
                    or any(
                        x in error_str
                        for x in [
                            "rate limit",
                            "429",
                            "timeout",
                            "500",
                            "503",
                            "temporarily",
                            "unavailable",
                            "deadline",
                            "resource_exhausted",
                        ]
                    )
                )

                if not is_retryable:
                    raise

                wait_time = 2**attempt
                if isinstance(e, EmptyResponseError):
                    wait_time = min(30, 5 * (2**attempt))
                    cprint(
                        f"[Verifier] Empty response. Retry {attempt + 1}/{max_retries} in {wait_time}s",
                        "yellow",
                    )
                elif "429" in error_str or "rate limit" in error_str:
                    wait_time = min(30, 10 * (2**attempt))
                    cprint(
                        f"[Verifier] Rate limit hit. Retry {attempt + 1}/{max_retries} in {wait_time}s",
                        "yellow",
                    )
                elif "503" in error_str or "overloaded" in error_str:
                    wait_time = min(60, 15 * (2**attempt))
                    cprint(
                        f"[Verifier] Model overloaded. Retry {attempt + 1}/{max_retries} in {wait_time}s",
                        "yellow",
                    )
                else:
                    cprint(
                        f"[Verifier] Retry {attempt + 1}/{max_retries} in {wait_time}s: {e}",
                        "yellow",
                    )

                time.sleep(wait_time)

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
            prompt = f"""You are a document verification assistant with access to reference documents.

## CONTEXT:

{case_context}

## TASK:

Verify if the following statement is supported by the reference documents.

## STATEMENT:
"Page {chunk.page_number}, Item {chunk.item_number}: {chunk.text}"

INSTRUCTIONS:
1. Search the reference documents for information about this statement
2. If you find supporting evidence, mark verified=true with high confidence (7-10)
3. If you find contradicting evidence, mark verified=false and explain
4. If you find no relevant information, mark verified=false with low confidence (1-3)

REQUIRED JSON OUTPUT FORMAT:
{{
  "verified": boolean,
  "confidence_score": integer (1-10),
  "verification_source": "citation or 'No match found'",
  "verification_note": "brief explanation"
}}

Provide ONLY the JSON object, no other text."""

            tool = types.Tool(
                file_search=types.FileSearch(file_search_store_names=[store_name])
            )

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    tools=[tool],
                ),
            )

            if not response.text:
                cprint(f"[Verifier] ⚠️  Empty response from API", "yellow")
                raise EmptyResponseError("API returned empty response")

            response_text = response.text.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()

            try:
                result = json.loads(response_text)
            except json.JSONDecodeError as e:
                cprint(f"[Verifier] ⚠️  Failed to parse JSON response: {e}", "yellow")
                cprint(f"[Verifier] Raw response: {response_text[:200]}...", "yellow")
                chunk.verified = False
                chunk.verification_score = 1
                chunk.verification_source = "JSON parse error"
                chunk.verification_note = f"Failed to parse API response: {str(e)}"
                chunk.citations = []
                return chunk

            # Extract grounding metadata if available
            actual_citations = []
            if hasattr(response, "candidates") and response.candidates:
                candidate = response.candidates[0]
                if (
                    hasattr(candidate, "grounding_metadata")
                    and candidate.grounding_metadata
                ):
                    if hasattr(candidate.grounding_metadata, "grounding_chunks"):
                        cprint(
                            f"[Verifier] Found {len(candidate.grounding_metadata.grounding_chunks)} grounding chunks",
                            "cyan",
                        )

                        for (
                            grounding_chunk
                        ) in candidate.grounding_metadata.grounding_chunks:
                            citation = {}

                            # File Search uses retrieved_context (check this first)
                            if hasattr(grounding_chunk, "retrieved_context"):
                                ctx = grounding_chunk.retrieved_context
                                citation["title"] = getattr(ctx, "title", "Document")
                                citation["excerpt"] = getattr(ctx, "text", "")[:300]
                            # Fallback to document attribute (generic grounding)
                            elif (
                                hasattr(grounding_chunk, "document")
                                and grounding_chunk.document
                            ):
                                citation["title"] = (
                                    grounding_chunk.document.title
                                    if hasattr(grounding_chunk.document, "title")
                                    else "Document"
                                )
                                # Extract text from content attribute
                                if hasattr(grounding_chunk, "content") and hasattr(
                                    grounding_chunk.content, "text"
                                ):
                                    citation["excerpt"] = grounding_chunk.content.text[:300]
                                else:
                                    citation["excerpt"] = ""
                            # Web grounding
                            elif (
                                hasattr(grounding_chunk, "web") and grounding_chunk.web
                            ):
                                citation["title"] = (
                                    grounding_chunk.web.title
                                    if hasattr(grounding_chunk.web, "title")
                                    else "Web Source"
                                )
                                if hasattr(grounding_chunk.web, "uri"):
                                    citation["uri"] = grounding_chunk.web.uri
                                if hasattr(grounding_chunk, "content") and hasattr(
                                    grounding_chunk.content, "text"
                                ):
                                    citation["excerpt"] = grounding_chunk.content.text[:300]
                                else:
                                    citation["excerpt"] = ""
                            else:
                                citation["title"] = "Unknown Source"
                                citation["excerpt"] = ""

                            actual_citations.append(citation)

            if actual_citations:
                cprint(
                    f"[Verifier] Using {len(actual_citations)} actual grounding citations",
                    "green",
                )
                chunk.citations = actual_citations
            else:
                cprint(
                    f"[Verifier] No grounding metadata found",
                    "yellow",
                )
                chunk.citations = []

            chunk.verified = result.get("verified", False)
            chunk.verification_score = min(
                10, max(1, result.get("confidence_score", 5))
            )
            chunk.verification_source = result.get(
                "verification_source", "No source found"
            )
            chunk.verification_note = result.get("verification_note", "")

            return chunk

        except EmptyResponseError as e:
            cprint(f"[Verifier] ✗ Empty response after retries", "yellow")
            chunk.verified = False
            chunk.verification_score = 1
            chunk.verification_source = "Empty API response"
            chunk.verification_note = "API returned empty response after retries"
            chunk.citations = []
            return chunk
        except Exception as e:
            cprint(f"[Verifier] ✗ Error verifying chunk: {e}", "yellow")
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
        batch_size: int = 3,
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

        cprint(f"[Verifier] Starting batch verification: {len(chunks)} chunks", "cyan")

        verified_chunks = []
        total_chunks = len(chunks)

        for batch_start in range(0, total_chunks, batch_size):
            batch_end = min(batch_start + batch_size, total_chunks)
            batch = chunks[batch_start:batch_end]

            cprint(
                f"[Verifier] Processing batch {batch_start // batch_size + 1}: chunks {batch_start + 1}-{batch_end} of {total_chunks}",
                "cyan",
            )

            batch_results = []
            for chunk in batch:
                try:
                    verified_chunk = self._retry_with_backoff(
                        self.verify_chunk, chunk, store_name, case_context
                    )
                    batch_results.append(verified_chunk)
                    await asyncio.sleep(1.5)

                except Exception as e:
                    cprint(
                        f"[Verifier] Error verifying chunk {chunk.item_number}: {e}",
                        "yellow",
                    )
                    chunk.verified = False
                    chunk.verification_score = 1
                    chunk.verification_source = "Error"
                    chunk.verification_note = f"Verification failed: {str(e)}"
                    batch_results.append(chunk)

            verified_chunks.extend(batch_results)

            if batch_end < total_chunks:
                cprint(
                    f"[Verifier] Batch complete. Waiting 3 seconds before next batch...",
                    "cyan",
                )
                await asyncio.sleep(3)

        # Final retry pass for empty responses
        failed_chunks = [
            (i, c) for i, c in enumerate(verified_chunks)
            if c.verification_source == "Empty API response"
        ]

        if failed_chunks:
            cprint(
                f"[Verifier] Retrying {len(failed_chunks)} chunks with empty responses...",
                "cyan",
            )

            for idx, chunk in failed_chunks:
                try:
                    cprint(f"[Verifier] Final retry for chunk {chunk.item_number}", "cyan")
                    verified_chunk = self._retry_with_backoff(
                        self.verify_chunk, chunk, store_name, case_context, max_retries=2
                    )
                    verified_chunks[idx] = verified_chunk
                    await asyncio.sleep(2)
                except Exception as e:
                    cprint(f"[Verifier] Final retry failed for chunk {chunk.item_number}", "yellow")
                    chunk.verification_note = "API returned empty response after all retries - needs manual review"

        verified_count = sum(1 for c in verified_chunks if c.verified)
        cprint(
            f"[Verifier] ✓ Batch verification complete: {verified_count}/{total_chunks} chunks verified",
            "green",
        )

        return verified_chunks


# Singleton instance
gemini_verifier = GeminiVerifier()
