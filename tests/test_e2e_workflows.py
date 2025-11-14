"""
End-to-end workflow tests
Tests complete workflows from document upload to final output
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.models import ChunkingMode, OutputFormat
from backend.app.gemini_service import GeminiVerificationService
from termcolor import cprint
import io
from pathlib import Path
import pandas as pd


@pytest.fixture(scope="module")
def test_client():
    """Create test client for FastAPI app"""
    return TestClient(app)


@pytest.mark.integration
@pytest.mark.slow
class TestBasicWorkflow:
    """Test suite for basic document processing workflow (no AI verification)"""

    def test_complete_document_workflow_paragraph(self, test_client, sample_docx_content):
        """
        Test complete workflow: Upload → Chunk (paragraph) → Export (Excel) → Download
        """
        cprint("\n[TEST] Testing complete document workflow (paragraph mode)", "cyan")

        # Step 1: Upload document
        cprint("[TEST] Step 1: Uploading document...", "cyan")
        files = {"file": ("contract.docx", io.BytesIO(sample_docx_content), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        upload_response = test_client.post("/upload", files=files)

        assert upload_response.status_code == 200
        document_id = upload_response.json()["document_id"]
        page_count = upload_response.json()["page_count"]
        cprint(f"[TEST] ✓ Document uploaded: {document_id} ({page_count} pages)", "green")

        # Step 2: Chunk document
        cprint("[TEST] Step 2: Chunking document...", "cyan")
        chunk_request = {
            "document_id": document_id,
            "chunking_mode": ChunkingMode.PARAGRAPH.value
        }
        chunk_response = test_client.post("/chunk", json=chunk_request)

        assert chunk_response.status_code == 200
        total_chunks = chunk_response.json()["total_chunks"]
        chunks = chunk_response.json()["chunks"]
        cprint(f"[TEST] ✓ Document chunked: {total_chunks} paragraphs", "green")

        # Verify chunk structure
        assert len(chunks) > 0
        for chunk in chunks:
            assert chunk["page_number"] > 0
            assert chunk["item_number"] is not None
            assert len(chunk["text"]) > 0

        # Step 3: Export document
        cprint("[TEST] Step 3: Exporting to Excel...", "cyan")
        export_request = {
            "document_id": document_id,
            "chunking_mode": ChunkingMode.PARAGRAPH.value,
            "output_format": OutputFormat.EXCEL.value
        }
        export_response = test_client.post("/export", json=export_request)

        assert export_response.status_code == 200
        filename = export_response.json()["filename"]
        cprint(f"[TEST] ✓ Document exported: {filename}", "green")

        # Step 4: Download file
        cprint("[TEST] Step 4: Downloading file...", "cyan")
        download_response = test_client.get(f"/download/{document_id}")

        assert download_response.status_code == 200
        assert len(download_response.content) > 0
        cprint(f"[TEST] ✓ File downloaded: {len(download_response.content)} bytes", "green")

        cprint("[TEST] ✓ Complete workflow successful!", "green", attrs=["bold"])

    def test_complete_document_workflow_sentence(self, test_client, sample_docx_content):
        """
        Test complete workflow: Upload → Chunk (sentence) → Export (Word) → Download
        """
        cprint("\n[TEST] Testing complete document workflow (sentence mode)", "cyan")

        # Step 1: Upload
        files = {"file": ("contract.docx", io.BytesIO(sample_docx_content), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        upload_response = test_client.post("/upload", files=files)
        document_id = upload_response.json()["document_id"]

        # Step 2: Chunk (sentence mode)
        chunk_request = {
            "document_id": document_id,
            "chunking_mode": ChunkingMode.SENTENCE.value
        }
        chunk_response = test_client.post("/chunk", json=chunk_request)
        total_chunks = chunk_response.json()["total_chunks"]
        chunks = chunk_response.json()["chunks"]

        # Verify hierarchical numbering
        for chunk in chunks:
            assert "." in chunk["item_number"], "Sentence mode should use hierarchical numbering"

        cprint(f"[TEST] ✓ Sentence chunking: {total_chunks} sentences", "green")

        # Step 3: Export as Word landscape
        export_request = {
            "document_id": document_id,
            "chunking_mode": ChunkingMode.SENTENCE.value,
            "output_format": OutputFormat.WORD_LANDSCAPE.value
        }
        export_response = test_client.post("/export", json=export_request)

        assert export_response.status_code == 200
        filename = export_response.json()["filename"]
        assert filename.endswith(".docx")

        # Step 4: Download
        download_response = test_client.get(f"/download/{document_id}")
        assert download_response.status_code == 200

        cprint("[TEST] ✓ Complete workflow successful!", "green", attrs=["bold"])

    def test_multiple_export_formats(self, test_client, sample_docx_content):
        """
        Test exporting same document to multiple formats
        """
        cprint("\n[TEST] Testing multiple export formats", "cyan")

        # Upload and chunk
        files = {"file": ("contract.docx", io.BytesIO(sample_docx_content), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        upload_response = test_client.post("/upload", files=files)
        document_id = upload_response.json()["document_id"]

        formats_to_test = [
            OutputFormat.WORD_LANDSCAPE,
            OutputFormat.WORD_PORTRAIT,
            OutputFormat.EXCEL,
            OutputFormat.CSV,
            OutputFormat.JSON
        ]

        for output_format in formats_to_test:
            export_request = {
                "document_id": document_id,
                "chunking_mode": ChunkingMode.PARAGRAPH.value,
                "output_format": output_format.value
            }
            export_response = test_client.post("/export", json=export_request)

            assert export_response.status_code == 200
            filename = export_response.json()["filename"]
            cprint(f"[TEST] ✓ Exported as {output_format.value}: {filename}", "green")

        cprint("[TEST] ✓ All export formats successful!", "green", attrs=["bold"])


@pytest.mark.gemini
@pytest.mark.integration
@pytest.mark.slow
class TestAIVerificationWorkflow:
    """Test suite for complete AI-powered verification workflow"""

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

    def test_full_ai_verification_workflow(
        self,
        test_client,
        sample_docx_content,
        sample_case_context,
        temp_dir
    ):
        """
        Test complete AI verification workflow:
        1. Upload target document
        2. Upload reference documents
        3. Generate metadata (Flash-lite)
        4. Create File Search store
        5. Chunk target document
        6. Verify chunks (Flash verification loop)
        7. Export verified results
        8. Download final document
        """
        cprint("\n[TEST] Testing full AI verification workflow", "cyan", attrs=["bold"])

        # Step 1: Upload target document
        cprint("[TEST] Step 1: Uploading target document...", "cyan")
        files = {"file": ("target.docx", io.BytesIO(sample_docx_content), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        upload_response = test_client.post("/upload", files=files)

        assert upload_response.status_code == 200
        document_id = upload_response.json()["document_id"]
        cprint(f"[TEST] ✓ Target document uploaded: {document_id}", "green")

        # Step 2: Create File Search store and upload reference documents
        cprint("[TEST] Step 2: Creating File Search store...", "cyan")
        case_id = "e2e_test_001"
        store_name, display_name = self.service.create_store(case_id)
        self.stores_to_cleanup.append(store_name)
        cprint(f"[TEST] ✓ Store created: {display_name}", "green")

        # Step 3: Generate metadata for reference document (Flash-lite)
        cprint("[TEST] Step 3: Generating metadata with Gemini Flash...", "cyan")
        temp_file = temp_dir / "reference.docx"
        temp_file.write_bytes(sample_docx_content)

        metadata = self.service.generate_metadata(
            file_path=str(temp_file),
            filename="reference.docx",
            case_context=sample_case_context
        )
        cprint(f"[TEST] ✓ Metadata generated: {metadata.document_type}", "green")

        # Step 4: Upload reference document to store
        cprint("[TEST] Step 4: Uploading reference to File Search store...", "cyan")
        file_name = self.service.upload_to_store(
            file_path=str(temp_file),
            store_name=store_name,
            metadata=metadata
        )
        cprint(f"[TEST] ✓ Reference uploaded: {file_name}", "green")

        # Step 5: Chunk target document
        cprint("[TEST] Step 5: Chunking target document...", "cyan")
        chunk_request = {
            "document_id": document_id,
            "chunking_mode": ChunkingMode.PARAGRAPH.value
        }
        chunk_response = test_client.post("/chunk", json=chunk_request)

        assert chunk_response.status_code == 200
        chunks_data = chunk_response.json()["chunks"]
        cprint(f"[TEST] ✓ Document chunked: {len(chunks_data)} chunks", "green")

        # Step 6: Verify chunks with Gemini Flash
        cprint("[TEST] Step 6: Verifying chunks with Gemini Flash...", "cyan")

        # Use API endpoint for verification
        verify_request = {
            "document_id": document_id,
            "store_id": store_name,
            "case_context": sample_case_context,
            "chunking_mode": ChunkingMode.PARAGRAPH.value
        }
        verify_response = test_client.post("/api/verify/execute", json=verify_request)

        assert verify_response.status_code == 200
        verify_data = verify_response.json()

        total_verified = verify_data["total_verified"]
        total_chunks = verify_data["total_chunks"]
        processing_time = verify_data["processing_time_seconds"]

        cprint(f"[TEST] ✓ Verification complete: {total_verified}/{total_chunks} verified in {processing_time:.2f}s", "green")

        # Step 7: Export verified document
        cprint("[TEST] Step 7: Exporting verified document...", "cyan")
        export_request = {
            "document_id": document_id,
            "chunking_mode": ChunkingMode.PARAGRAPH.value,
            "output_format": OutputFormat.EXCEL.value
        }
        export_response = test_client.post("/export", json=export_request)

        assert export_response.status_code == 200
        filename = export_response.json()["filename"]
        cprint(f"[TEST] ✓ Verified document exported: {filename}", "green")

        # Step 8: Download and verify content
        cprint("[TEST] Step 8: Downloading and verifying content...", "cyan")
        download_response = test_client.get(f"/download/{document_id}")

        assert download_response.status_code == 200
        assert len(download_response.content) > 0

        # Save and verify Excel contains verification data
        output_file = temp_dir / "verified_output.xlsx"
        output_file.write_bytes(download_response.content)

        df = pd.read_excel(output_file, sheet_name='Verification')

        # Verify Excel has verification columns
        assert "Verified ☑" in df.columns
        assert "Verification Score" in df.columns
        assert "Verification Source" in df.columns
        assert "Verification Note" in df.columns

        # Verify some chunks have verification data
        has_verification = df["Verification Score"].notna().any()
        assert has_verification, "Output should contain verification data"

        cprint(f"[TEST] ✓ Verified content downloaded: {len(download_response.content)} bytes", "green")

        cprint("[TEST] ✓✓✓ FULL AI VERIFICATION WORKFLOW SUCCESSFUL! ✓✓✓", "green", attrs=["bold"])

    def test_upload_references_endpoint(self, test_client, sample_docx_content, sample_case_context):
        """
        Test the /api/verify/upload-references endpoint for bulk reference upload
        """
        cprint("\n[TEST] Testing bulk reference upload endpoint", "cyan")

        # Upload multiple reference files
        files = [
            ("files", ("reference1.docx", io.BytesIO(sample_docx_content), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")),
            ("files", ("reference2.docx", io.BytesIO(sample_docx_content), "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))
        ]

        data = {"case_context": sample_case_context}

        response = test_client.post("/api/verify/upload-references", data=data, files=files)

        assert response.status_code == 200
        result = response.json()

        assert "store_id" in result
        assert "store_name" in result
        assert "documents_uploaded" in result
        assert "metadata" in result

        assert result["documents_uploaded"] == 2
        assert len(result["metadata"]) == 2

        # Track for cleanup
        self.stores_to_cleanup.append(result["store_id"])

        cprint(f"[TEST] ✓ Uploaded {result['documents_uploaded']} references to store {result['store_id']}", "green")

    def test_verification_reset(self, test_client, sample_docx_content, sample_case_context, temp_dir):
        """
        Test resetting verification results for a document
        """
        cprint("\n[TEST] Testing verification reset", "cyan")

        # Upload document
        files = {"file": ("target.docx", io.BytesIO(sample_docx_content), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        upload_response = test_client.post("/upload", files=files)
        document_id = upload_response.json()["document_id"]

        # Create store and upload reference
        store_name, _ = self.service.create_store("reset_test")
        self.stores_to_cleanup.append(store_name)

        temp_file = temp_dir / "ref.docx"
        temp_file.write_bytes(sample_docx_content)

        metadata = self.service.generate_metadata(str(temp_file), "ref.docx", sample_case_context)
        self.service.upload_to_store(str(temp_file), store_name, metadata)

        # Verify chunks
        verify_request = {
            "document_id": document_id,
            "store_id": store_name,
            "case_context": sample_case_context,
            "chunking_mode": ChunkingMode.PARAGRAPH.value
        }
        test_client.post("/api/verify/execute", json=verify_request)

        # Reset verification
        reset_response = test_client.delete(f"/api/verify/reset/{document_id}")

        assert reset_response.status_code == 200
        result = reset_response.json()

        assert "message" in result
        assert "chunks_reset" in result
        assert result["chunks_reset"] > 0

        cprint(f"[TEST] ✓ Reset {result['chunks_reset']} chunks", "green")


@pytest.mark.integration
class TestErrorHandling:
    """Test suite for error handling in workflows"""

    def test_workflow_with_invalid_document_id(self, test_client):
        """Test workflow steps with invalid document ID"""
        cprint("\n[TEST] Testing error handling with invalid document ID", "cyan")

        invalid_id = "invalid_doc_id_999"

        # Try chunking
        chunk_request = {
            "document_id": invalid_id,
            "chunking_mode": ChunkingMode.PARAGRAPH.value
        }
        chunk_response = test_client.post("/chunk", json=chunk_request)
        assert chunk_response.status_code == 404

        # Try exporting
        export_request = {
            "document_id": invalid_id,
            "chunking_mode": ChunkingMode.PARAGRAPH.value,
            "output_format": OutputFormat.EXCEL.value
        }
        export_response = test_client.post("/export", json=export_request)
        assert export_response.status_code == 404

        # Try downloading
        download_response = test_client.get(f"/download/{invalid_id}")
        assert download_response.status_code == 404

        cprint("[TEST] ✓ All error cases handled correctly", "green")

    def test_workflow_with_missing_export(self, test_client, sample_docx_content):
        """Test downloading without exporting first"""
        cprint("\n[TEST] Testing download without export", "cyan")

        # Upload only
        files = {"file": ("test.docx", io.BytesIO(sample_docx_content), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        upload_response = test_client.post("/upload", files=files)
        document_id = upload_response.json()["document_id"]

        # Try download without export
        download_response = test_client.get(f"/download/{document_id}")
        assert download_response.status_code == 404

        cprint("[TEST] ✓ Missing export handled correctly", "green")
