"""
Unit tests for Gemini flash verification loop
Tests the AI-powered verification of document chunks against reference documents
"""
import pytest
import time
import asyncio
from pathlib import Path
from app.gemini_service import GeminiVerificationService
from app.models import DocumentChunk, DocumentMetadata
from termcolor import cprint


@pytest.mark.gemini
@pytest.mark.unit
class TestGeminiFileSearchStore:
    """Test suite for Gemini File Search store creation and management"""

    @pytest.fixture(autouse=True)
    def setup(self, gemini_api_key):
        """Setup for each test"""
        self.service = GeminiVerificationService()
        self.stores_to_cleanup = []

    def teardown_method(self):
        """Cleanup File Search stores after each test"""
        for store_name in self.stores_to_cleanup:
            try:
                self.service.client.file_search_stores.delete(name=store_name)
                cprint(f"[TEST] Cleaned up store: {store_name}", "cyan")
            except Exception as e:
                cprint(f"[TEST] Could not cleanup store {store_name}: {e}", "yellow")

    def test_create_file_search_store(self):
        """Test File Search store creation"""
        cprint("\n[TEST] Testing File Search store creation", "cyan")

        case_id = "test_case_001"
        store_name, display_name = self.service.create_store(case_id)

        # Track for cleanup
        self.stores_to_cleanup.append(store_name)

        # Verify store was created
        assert store_name is not None
        assert display_name is not None
        assert "file_search_stores/" in store_name
        assert case_id in display_name or "Verification" in display_name

        cprint(f"[TEST] ✓ Store created: {store_name}", "green")
        cprint(f"  Display Name: {display_name}", "cyan")

    def test_upload_file_to_store(self, sample_docx_content, sample_metadata, temp_dir):
        """Test uploading a file to File Search store"""
        cprint("\n[TEST] Testing file upload to File Search store", "cyan")

        # Create store
        case_id = "test_case_002"
        store_name, _ = self.service.create_store(case_id)
        self.stores_to_cleanup.append(store_name)

        # Save sample file
        temp_file = temp_dir / "reference.docx"
        temp_file.write_bytes(sample_docx_content)

        # Upload file to store
        file_name = self.service.upload_to_store(
            file_path=str(temp_file),
            store_name=store_name,
            metadata=sample_metadata
        )

        # Verify upload
        assert file_name is not None
        assert "files/" in file_name

        cprint(f"[TEST] ✓ File uploaded: {file_name}", "green")

    def test_upload_multiple_files_to_store(self, sample_docx_content, sample_document_content, sample_metadata, temp_dir):
        """Test uploading multiple files to File Search store"""
        cprint("\n[TEST] Testing multiple file uploads to store", "cyan")

        # Create store
        case_id = "test_case_003"
        store_name, _ = self.service.create_store(case_id)
        self.stores_to_cleanup.append(store_name)

        # Upload first file (DOCX)
        temp_file1 = temp_dir / "reference1.docx"
        temp_file1.write_bytes(sample_docx_content)

        metadata1 = sample_metadata.model_copy(update={"filename": "reference1.docx"})
        file_name1 = self.service.upload_to_store(
            file_path=str(temp_file1),
            store_name=store_name,
            metadata=metadata1
        )

        # Upload second file (PDF)
        temp_file2 = temp_dir / "reference2.pdf"
        temp_file2.write_bytes(sample_document_content)

        metadata2 = sample_metadata.model_copy(update={"filename": "reference2.pdf"})
        file_name2 = self.service.upload_to_store(
            file_path=str(temp_file2),
            store_name=store_name,
            metadata=metadata2
        )

        # Verify both uploads
        assert file_name1 is not None
        assert file_name2 is not None
        assert file_name1 != file_name2

        cprint(f"[TEST] ✓ Multiple files uploaded successfully", "green")


@pytest.mark.gemini
@pytest.mark.unit
class TestGeminiChunkVerification:
    """Test suite for Gemini-powered chunk verification using Flash model"""

    @pytest.fixture(autouse=True)
    def setup(self, gemini_api_key):
        """Setup for each test"""
        self.service = GeminiVerificationService()
        self.stores_to_cleanup = []

    def teardown_method(self):
        """Cleanup File Search stores after each test"""
        for store_name in self.stores_to_cleanup:
            try:
                self.service.client.file_search_stores.delete(name=store_name)
            except Exception:
                pass

    @pytest.mark.slow
    def test_verify_single_chunk(self, sample_docx_content, sample_metadata, sample_case_context, temp_dir):
        """Test verifying a single chunk against File Search store"""
        cprint("\n[TEST] Testing single chunk verification", "cyan")

        # Create store and upload reference document
        case_id = "test_case_verify_001"
        store_name, _ = self.service.create_store(case_id)
        self.stores_to_cleanup.append(store_name)

        temp_file = temp_dir / "reference.docx"
        temp_file.write_bytes(sample_docx_content)

        self.service.upload_to_store(
            file_path=str(temp_file),
            store_name=store_name,
            metadata=sample_metadata
        )

        # Create a chunk to verify
        chunk = DocumentChunk(
            page_number=1,
            item_number="1",
            text="This is a test paragraph for verification.",
            is_overlap=False
        )

        # Verify chunk
        verified_chunk = self.service.verify_chunk(
            chunk=chunk,
            store_name=store_name,
            case_context=sample_case_context
        )

        # Verify results
        assert verified_chunk.verified is not None
        assert isinstance(verified_chunk.verified, bool)
        assert verified_chunk.verification_score is not None
        assert 1 <= verified_chunk.verification_score <= 10
        assert verified_chunk.verification_source is not None
        assert verified_chunk.verification_note is not None
        assert isinstance(verified_chunk.citations, list)

        cprint(f"[TEST] ✓ Chunk verification complete:", "green")
        cprint(f"  - Verified: {verified_chunk.verified}", "cyan")
        cprint(f"  - Score: {verified_chunk.verification_score}/10", "cyan")
        cprint(f"  - Source: {verified_chunk.verification_source}", "cyan")
        cprint(f"  - Note: {verified_chunk.verification_note[:100]}...", "cyan")

    @pytest.mark.slow
    def test_verify_batch_chunks(self, sample_docx_content, sample_metadata, sample_case_context, sample_chunks_data, temp_dir):
        """Test batch verification of multiple chunks"""
        cprint("\n[TEST] Testing batch chunk verification", "cyan")

        # Create store and upload reference document
        case_id = "test_case_verify_002"
        store_name, _ = self.service.create_store(case_id)
        self.stores_to_cleanup.append(store_name)

        temp_file = temp_dir / "reference.docx"
        temp_file.write_bytes(sample_docx_content)

        self.service.upload_to_store(
            file_path=str(temp_file),
            store_name=store_name,
            metadata=sample_metadata
        )

        # Verify batch
        start_time = time.time()
        verified_chunks = asyncio.run(
            self.service.verify_batch(
                chunks=sample_chunks_data,
                store_name=store_name,
                case_context=sample_case_context,
                batch_size=2
            )
        )
        elapsed_time = time.time() - start_time

        # Verify results
        assert len(verified_chunks) == len(sample_chunks_data)

        for chunk in verified_chunks:
            assert chunk.verified is not None
            assert chunk.verification_score is not None
            assert 1 <= chunk.verification_score <= 10
            assert chunk.verification_source is not None
            assert chunk.verification_note is not None

        verified_count = sum(1 for c in verified_chunks if c.verified)

        cprint(f"[TEST] ✓ Batch verification complete:", "green")
        cprint(f"  - Total chunks: {len(verified_chunks)}", "cyan")
        cprint(f"  - Verified: {verified_count}", "cyan")
        cprint(f"  - Time: {elapsed_time:.2f}s", "cyan")

    def test_verification_with_citations(self, sample_docx_content, sample_metadata, sample_case_context, temp_dir):
        """Test that verification includes citation details"""
        cprint("\n[TEST] Testing verification with citations", "cyan")

        # Create store and upload reference document
        case_id = "test_case_citations_001"
        store_name, _ = self.service.create_store(case_id)
        self.stores_to_cleanup.append(store_name)

        temp_file = temp_dir / "reference.docx"
        temp_file.write_bytes(sample_docx_content)

        self.service.upload_to_store(
            file_path=str(temp_file),
            store_name=store_name,
            metadata=sample_metadata
        )

        # Create a chunk to verify
        chunk = DocumentChunk(
            page_number=1,
            item_number="1",
            text="This is a test paragraph for verification.",
            is_overlap=False
        )

        # Verify chunk
        verified_chunk = self.service.verify_chunk(
            chunk=chunk,
            store_name=store_name,
            case_context=sample_case_context
        )

        # Check citations
        assert verified_chunk.citations is not None
        assert isinstance(verified_chunk.citations, list)

        # If citations exist, verify structure
        if len(verified_chunk.citations) > 0:
            for citation in verified_chunk.citations:
                assert isinstance(citation, dict)
                # Citations should have title and excerpt at minimum
                assert "title" in citation or "excerpt" in citation

        cprint(f"[TEST] ✓ Citations included: {len(verified_chunk.citations)} citations", "green")

    def test_verification_score_range(self, sample_docx_content, sample_metadata, sample_case_context, temp_dir):
        """Test that verification scores are within valid range"""
        cprint("\n[TEST] Testing verification score range", "cyan")

        # Create store and upload reference document
        case_id = "test_case_score_001"
        store_name, _ = self.service.create_store(case_id)
        self.stores_to_cleanup.append(store_name)

        temp_file = temp_dir / "reference.docx"
        temp_file.write_bytes(sample_docx_content)

        self.service.upload_to_store(
            file_path=str(temp_file),
            store_name=store_name,
            metadata=sample_metadata
        )

        # Test with multiple different chunks
        test_chunks = [
            DocumentChunk(page_number=1, item_number="1", text="This is a test paragraph for verification.", is_overlap=False),
            DocumentChunk(page_number=1, item_number="2", text="Another sentence for testing verification.", is_overlap=False),
            DocumentChunk(page_number=1, item_number="3", text="Contract terms and conditions.", is_overlap=False),
        ]

        for chunk in test_chunks:
            verified_chunk = self.service.verify_chunk(
                chunk=chunk,
                store_name=store_name,
                case_context=sample_case_context
            )

            # Verify score is within range
            assert 1 <= verified_chunk.verification_score <= 10, \
                f"Score {verified_chunk.verification_score} out of range for chunk: {chunk.text}"

        cprint("[TEST] ✓ All verification scores within valid range (1-10)", "green")

    def test_verification_retry_mechanism(self, sample_docx_content, sample_metadata, sample_case_context, temp_dir):
        """Test that verification includes retry logic for rate limits"""
        cprint("\n[TEST] Testing verification retry mechanism", "cyan")

        # Create store and upload reference document
        case_id = "test_case_retry_001"
        store_name, _ = self.service.create_store(case_id)
        self.stores_to_cleanup.append(store_name)

        temp_file = temp_dir / "reference.docx"
        temp_file.write_bytes(sample_docx_content)

        self.service.upload_to_store(
            file_path=str(temp_file),
            store_name=store_name,
            metadata=sample_metadata
        )

        # Create chunk
        chunk = DocumentChunk(
            page_number=1,
            item_number="1",
            text="This is a test paragraph for verification.",
            is_overlap=False
        )

        # Verify using _retry_with_backoff method
        verified_chunk = self.service._retry_with_backoff(
            self.service.verify_chunk,
            chunk,
            store_name,
            sample_case_context,
            max_retries=2
        )

        # Should succeed
        assert verified_chunk is not None
        assert verified_chunk.verified is not None

        cprint("[TEST] ✓ Retry mechanism works correctly", "green")


@pytest.mark.gemini
@pytest.mark.integration
class TestGeminiVerificationWorkflow:
    """Integration tests for complete verification workflow"""

    @pytest.fixture(autouse=True)
    def setup(self, gemini_api_key):
        """Setup for each test"""
        self.service = GeminiVerificationService()
        self.stores_to_cleanup = []

    def teardown_method(self):
        """Cleanup File Search stores after each test"""
        for store_name in self.stores_to_cleanup:
            try:
                self.service.client.file_search_stores.delete(name=store_name)
            except Exception:
                pass

    @pytest.mark.slow
    def test_full_verification_workflow(self, sample_docx_content, sample_case_context, temp_dir):
        """Test complete workflow: create store → upload files → generate metadata → verify chunks"""
        cprint("\n[TEST] Testing full verification workflow", "cyan")

        # Step 1: Create store
        case_id = "test_workflow_001"
        store_name, display_name = self.service.create_store(case_id)
        self.stores_to_cleanup.append(store_name)
        cprint(f"[TEST] Step 1: Store created - {display_name}", "green")

        # Step 2: Generate metadata
        temp_file = temp_dir / "reference.docx"
        temp_file.write_bytes(sample_docx_content)

        metadata = self.service.generate_metadata(
            file_path=str(temp_file),
            filename="reference.docx",
            case_context=sample_case_context
        )
        cprint(f"[TEST] Step 2: Metadata generated - {metadata.document_type}", "green")

        # Step 3: Upload file to store
        file_name = self.service.upload_to_store(
            file_path=str(temp_file),
            store_name=store_name,
            metadata=metadata
        )
        cprint(f"[TEST] Step 3: File uploaded to store", "green")

        # Step 4: Verify chunks
        test_chunks = [
            DocumentChunk(page_number=1, item_number="1", text="This is a test paragraph for verification.", is_overlap=False),
            DocumentChunk(page_number=1, item_number="2", text="Another sentence for testing.", is_overlap=False),
        ]

        verified_chunks = asyncio.run(
            self.service.verify_batch(
                chunks=test_chunks,
                store_name=store_name,
                case_context=sample_case_context,
                batch_size=2
            )
        )

        cprint(f"[TEST] Step 4: Verified {len(verified_chunks)} chunks", "green")

        # Verify final results
        assert len(verified_chunks) == len(test_chunks)
        for chunk in verified_chunks:
            assert chunk.verified is not None
            assert chunk.verification_score is not None

        verified_count = sum(1 for c in verified_chunks if c.verified)

        cprint(f"[TEST] ✓ Full workflow complete:", "green")
        cprint(f"  - Store: {store_name}", "cyan")
        cprint(f"  - Files uploaded: 1", "cyan")
        cprint(f"  - Chunks verified: {verified_count}/{len(verified_chunks)}", "cyan")
