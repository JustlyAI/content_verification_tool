"""
Gemini Verification Service - Unified interface for tests
Combines CorpusManager and GeminiVerifier functionality
"""
from typing import List, Optional
import asyncio

from app.corpus.corpus_manager import CorpusManager, corpus_manager
from app.verification.gemini_verifier import GeminiVerifier, gemini_verifier
from app.models import DocumentChunk, DocumentMetadata


class GeminiVerificationService:
    """
    Unified service that combines CorpusManager and GeminiVerifier
    Provides a single interface for tests that expect a combined service
    """

    def __init__(self):
        """Initialize the unified service"""
        self.corpus_manager = corpus_manager
        self.verifier = gemini_verifier
        self.client = self.corpus_manager.client  # Expose client for tests

    def create_store(self, case_id: str):
        """Create a File Search store"""
        return self.corpus_manager.create_store(case_id)

    def generate_metadata(
        self, file_path: str, filename: str, case_context: Optional[str] = None
    ) -> DocumentMetadata:
        """Generate metadata for a reference document"""
        return self.corpus_manager.generate_metadata(file_path, filename, case_context)

    def upload_to_store(
        self, file_path: str, store_name: str, metadata: DocumentMetadata
    ) -> str:
        """Upload a file to a File Search store"""
        return self.corpus_manager.upload_to_store(file_path, store_name, metadata)

    def verify_chunk(
        self, chunk: DocumentChunk, store_name: str, case_context: Optional[str] = None
    ) -> DocumentChunk:
        """Verify a single chunk"""
        return self.verifier.verify_chunk(chunk, store_name, case_context)

    async def verify_batch(
        self,
        chunks: List[DocumentChunk],
        store_name: str,
        case_context: Optional[str] = None,
        batch_size: int = 3,
    ) -> List[DocumentChunk]:
        """Verify multiple chunks in batches"""
        return await self.verifier.verify_batch(
            chunks, store_name, case_context, batch_size
        )

    def _retry_with_backoff(self, func, *args, max_retries=3, **kwargs):
        """Retry a function with exponential backoff"""
        return self.verifier._retry_with_backoff(func, *args, max_retries=max_retries, **kwargs)

