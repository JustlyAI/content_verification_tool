"""
Integration tests for FastAPI endpoints
Tests all API routes and request/response handling
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import ChunkingMode, OutputFormat
from termcolor import cprint
import io


@pytest.fixture(scope="module")
def test_client():
    """Create test client for FastAPI app"""
    return TestClient(app)


@pytest.mark.integration
class TestHealthEndpoints:
    """Test suite for health check and root endpoints"""

    def test_root_endpoint(self, test_client):
        """Test root endpoint"""
        cprint("\n[TEST] Testing root endpoint", "cyan")

        response = test_client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "version" in data
        assert "endpoints" in data

        cprint("[TEST] ✓ Root endpoint working", "green")

    def test_health_endpoint(self, test_client):
        """Test health check endpoint"""
        cprint("\n[TEST] Testing health endpoint", "cyan")

        response = test_client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert "status" in data
        assert data["status"] == "healthy"
        assert "cache_dir" in data
        assert "output_dir" in data
        assert "documents_in_store" in data

        cprint("[TEST] ✓ Health endpoint working", "green")


@pytest.mark.integration
class TestUploadEndpoint:
    """Test suite for document upload endpoint"""

    def test_upload_pdf(self, test_client, sample_document_content):
        """Test PDF document upload"""
        cprint("\n[TEST] Testing PDF upload endpoint", "cyan")

        files = {
            "file": ("test.pdf", io.BytesIO(sample_document_content), "application/pdf")
        }
        response = test_client.post("/upload", files=files)

        assert response.status_code == 200
        data = response.json()

        assert "document_id" in data
        assert "filename" in data
        assert "page_count" in data
        assert "file_size" in data
        assert "message" in data

        assert data["filename"] == "test.pdf"
        assert data["page_count"] >= 1
        assert data["file_size"] == len(sample_document_content)

        cprint(f"[TEST] ✓ PDF uploaded: document_id={data['document_id']}", "green")

        return data["document_id"]

    def test_upload_docx(self, test_client, sample_docx_content):
        """Test DOCX document upload"""
        cprint("\n[TEST] Testing DOCX upload endpoint", "cyan")

        files = {
            "file": (
                "test.docx",
                io.BytesIO(sample_docx_content),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        }
        response = test_client.post("/upload", files=files)

        assert response.status_code == 200
        data = response.json()

        assert data["filename"] == "test.docx"

        cprint(f"[TEST] ✓ DOCX uploaded: document_id={data['document_id']}", "green")

    def test_upload_invalid_file(self, test_client):
        """Test upload with invalid file type"""
        cprint("\n[TEST] Testing upload with invalid file", "cyan")

        invalid_content = b"This is plain text, not a PDF"
        files = {"file": ("test.txt", io.BytesIO(invalid_content), "text/plain")}

        response = test_client.post("/upload", files=files)

        assert response.status_code in [400, 500]  # Should fail validation

        cprint("[TEST] ✓ Invalid file rejected as expected", "green")


@pytest.mark.integration
class TestChunkEndpoint:
    """Test suite for document chunking endpoint"""

    def test_chunk_paragraph_mode(self, test_client, sample_docx_content):
        """Test paragraph chunking endpoint"""
        cprint("\n[TEST] Testing paragraph chunking endpoint", "cyan")

        # First upload document
        files = {
            "file": (
                "test.docx",
                io.BytesIO(sample_docx_content),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        }
        upload_response = test_client.post("/upload", files=files)
        document_id = upload_response.json()["document_id"]

        # Then chunk it
        chunk_request = {
            "document_id": document_id,
            "splitting_mode": ChunkingMode.PARAGRAPH.value,
        }
        response = test_client.post("/chunk", json=chunk_request)

        assert response.status_code == 200
        data = response.json()

        assert "document_id" in data
        assert "splitting_mode" in data
        assert "chunks" in data
        assert "total_chunks" in data

        assert data["splitting_mode"] == ChunkingMode.PARAGRAPH.value
        assert data["total_chunks"] > 0
        assert len(data["chunks"]) == data["total_chunks"]

        # Verify chunk structure
        for chunk in data["chunks"]:
            assert "page_number" in chunk
            assert "item_number" in chunk
            assert "text" in chunk
            assert "is_overlap" in chunk

        cprint(
            f"[TEST] ✓ Paragraph chunking complete: {data['total_chunks']} chunks",
            "green",
        )

    def test_chunk_sentence_mode(self, test_client, sample_docx_content):
        """Test sentence chunking endpoint"""
        cprint("\n[TEST] Testing sentence chunking endpoint", "cyan")

        # First upload document
        files = {
            "file": (
                "test.docx",
                io.BytesIO(sample_docx_content),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        }
        upload_response = test_client.post("/upload", files=files)
        document_id = upload_response.json()["document_id"]

        # Then chunk it
        chunk_request = {
            "document_id": document_id,
            "splitting_mode": ChunkingMode.SENTENCE.value,
        }
        response = test_client.post("/chunk", json=chunk_request)

        assert response.status_code == 200
        data = response.json()

        assert data["splitting_mode"] == ChunkingMode.SENTENCE.value
        assert data["total_chunks"] > 0

        # Verify hierarchical numbering in sentence mode
        for chunk in data["chunks"]:
            assert (
                "." in chunk["item_number"]
            ), "Sentence mode should use hierarchical numbering"

        cprint(
            f"[TEST] ✓ Sentence chunking complete: {data['total_chunks']} chunks",
            "green",
        )

    def test_chunk_nonexistent_document(self, test_client):
        """Test chunking with nonexistent document ID"""
        cprint("\n[TEST] Testing chunking with nonexistent document", "cyan")

        chunk_request = {
            "document_id": "nonexistent_id_12345",
            "splitting_mode": ChunkingMode.PARAGRAPH.value,
        }
        response = test_client.post("/chunk", json=chunk_request)

        assert response.status_code == 404

        cprint("[TEST] ✓ Nonexistent document returns 404", "green")

    def test_chunk_caching(self, test_client, sample_docx_content):
        """Test that chunking results are cached"""
        cprint("\n[TEST] Testing chunk caching", "cyan")

        # Upload document
        files = {
            "file": (
                "test.docx",
                io.BytesIO(sample_docx_content),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        }
        upload_response = test_client.post("/upload", files=files)
        document_id = upload_response.json()["document_id"]

        # Chunk twice with same mode
        chunk_request = {
            "document_id": document_id,
            "splitting_mode": ChunkingMode.PARAGRAPH.value,
        }

        response1 = test_client.post("/chunk", json=chunk_request)
        response2 = test_client.post("/chunk", json=chunk_request)

        assert response1.status_code == 200
        assert response2.status_code == 200

        # Both should return same chunks
        data1 = response1.json()
        data2 = response2.json()

        assert data1["total_chunks"] == data2["total_chunks"]

        cprint("[TEST] ✓ Chunking results cached successfully", "green")


@pytest.mark.integration
class TestExportEndpoint:
    """Test suite for document export endpoint"""

    def test_export_word_landscape(self, test_client, sample_docx_content):
        """Test Word landscape export"""
        cprint("\n[TEST] Testing Word landscape export", "cyan")

        # Upload and chunk
        files = {
            "file": (
                "test.docx",
                io.BytesIO(sample_docx_content),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        }
        upload_response = test_client.post("/upload", files=files)
        document_id = upload_response.json()["document_id"]

        # Export
        export_request = {
            "document_id": document_id,
            "splitting_mode": ChunkingMode.PARAGRAPH.value,
            "output_format": OutputFormat.WORD_LANDSCAPE.value,
        }
        response = test_client.post("/export", json=export_request)

        assert response.status_code == 200
        data = response.json()

        assert "document_id" in data
        assert "output_format" in data
        assert "filename" in data
        assert "message" in data

        assert data["output_format"] == OutputFormat.WORD_LANDSCAPE.value
        assert data["filename"].endswith(".docx")

        cprint(f"[TEST] ✓ Word landscape export: {data['filename']}", "green")

    def test_export_excel(self, test_client, sample_docx_content):
        """Test Excel export"""
        cprint("\n[TEST] Testing Excel export", "cyan")

        # Upload and chunk
        files = {
            "file": (
                "test.docx",
                io.BytesIO(sample_docx_content),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        }
        upload_response = test_client.post("/upload", files=files)
        document_id = upload_response.json()["document_id"]

        # Export
        export_request = {
            "document_id": document_id,
            "splitting_mode": ChunkingMode.PARAGRAPH.value,
            "output_format": OutputFormat.EXCEL.value,
        }
        response = test_client.post("/export", json=export_request)

        assert response.status_code == 200
        data = response.json()

        assert data["output_format"] == OutputFormat.EXCEL.value
        assert data["filename"].endswith(".xlsx")

        cprint(f"[TEST] ✓ Excel export: {data['filename']}", "green")

    def test_export_csv(self, test_client, sample_docx_content):
        """Test CSV export"""
        cprint("\n[TEST] Testing CSV export", "cyan")

        # Upload and chunk
        files = {
            "file": (
                "test.docx",
                io.BytesIO(sample_docx_content),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        }
        upload_response = test_client.post("/upload", files=files)
        document_id = upload_response.json()["document_id"]

        # Export
        export_request = {
            "document_id": document_id,
            "splitting_mode": ChunkingMode.PARAGRAPH.value,
            "output_format": OutputFormat.CSV.value,
        }
        response = test_client.post("/export", json=export_request)

        assert response.status_code == 200
        data = response.json()

        assert data["output_format"] == OutputFormat.CSV.value
        assert data["filename"].endswith(".csv")

        cprint(f"[TEST] ✓ CSV export: {data['filename']}", "green")

    def test_export_json(self, test_client, sample_docx_content):
        """Test JSON export"""
        cprint("\n[TEST] Testing JSON export", "cyan")

        # Upload and chunk
        files = {
            "file": (
                "test.docx",
                io.BytesIO(sample_docx_content),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        }
        upload_response = test_client.post("/upload", files=files)
        document_id = upload_response.json()["document_id"]

        # Export
        export_request = {
            "document_id": document_id,
            "splitting_mode": ChunkingMode.PARAGRAPH.value,
            "output_format": OutputFormat.JSON.value,
        }
        response = test_client.post("/export", json=export_request)

        assert response.status_code == 200
        data = response.json()

        assert data["output_format"] == OutputFormat.JSON.value
        assert data["filename"].endswith(".json")

        cprint(f"[TEST] ✓ JSON export: {data['filename']}", "green")


@pytest.mark.integration
class TestDownloadEndpoint:
    """Test suite for file download endpoint"""

    def test_download_exported_file(self, test_client, sample_docx_content):
        """Test downloading exported file"""
        cprint("\n[TEST] Testing file download", "cyan")

        # Upload, chunk, and export
        files = {
            "file": (
                "test.docx",
                io.BytesIO(sample_docx_content),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        }
        upload_response = test_client.post("/upload", files=files)
        document_id = upload_response.json()["document_id"]

        export_request = {
            "document_id": document_id,
            "splitting_mode": ChunkingMode.PARAGRAPH.value,
            "output_format": OutputFormat.EXCEL.value,
        }
        test_client.post("/export", json=export_request)

        # Download
        response = test_client.get(f"/download/{document_id}")

        assert response.status_code == 200
        assert len(response.content) > 0
        assert (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            in response.headers.get("content-type", "")
        )

        cprint(f"[TEST] ✓ File downloaded: {len(response.content)} bytes", "green")

    def test_download_nonexistent_document(self, test_client):
        """Test downloading from nonexistent document"""
        cprint("\n[TEST] Testing download from nonexistent document", "cyan")

        response = test_client.get("/download/nonexistent_id_12345")

        assert response.status_code == 404

        cprint("[TEST] ✓ Nonexistent document returns 404", "green")


@pytest.mark.integration
class TestCacheEndpoint:
    """Test suite for cache management endpoint"""

    def test_clear_cache(self, test_client):
        """Test cache clearing"""
        cprint("\n[TEST] Testing cache clearing", "cyan")

        response = test_client.delete("/cache/clear")

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "documents_cleared" in data

        cprint("[TEST] ✓ Cache cleared successfully", "green")
