"""
Unit tests for document processor and file upload functionality
"""
import pytest
from pathlib import Path
from backend.app.document_processor import DocumentProcessor, MAX_FILE_SIZE
from backend.app.cache import document_cache
from termcolor import cprint


@pytest.mark.unit
class TestDocumentProcessor:
    """Test suite for DocumentProcessor class"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.processor = DocumentProcessor()
        yield
        # Cleanup: clear cache after each test
        document_cache.clear_all()

    def test_validate_file_success(self, sample_document_content):
        """Test successful file validation"""
        cprint("\n[TEST] Testing file validation - valid file", "cyan")

        # Should not raise any exception
        self.processor.validate_file(sample_document_content, "test.pdf")
        cprint("[TEST] ✓ File validation passed", "green")

    def test_validate_file_too_large(self):
        """Test file size validation - file too large"""
        cprint("\n[TEST] Testing file validation - file too large", "cyan")

        # Create file content larger than MAX_FILE_SIZE
        large_content = b"x" * (MAX_FILE_SIZE + 1000)

        with pytest.raises(ValueError, match="exceeds maximum allowed size"):
            self.processor.validate_file(large_content, "large.pdf")

        cprint("[TEST] ✓ Large file rejected as expected", "green")

    def test_validate_file_unsupported_format(self, sample_document_content):
        """Test file format validation - unsupported format"""
        cprint("\n[TEST] Testing file validation - unsupported format", "cyan")

        with pytest.raises(ValueError, match="Unsupported file format"):
            self.processor.validate_file(sample_document_content, "test.txt")

        cprint("[TEST] ✓ Unsupported format rejected as expected", "green")

    def test_convert_document_pdf(self, sample_document_content):
        """Test PDF document conversion"""
        cprint("\n[TEST] Testing PDF document conversion", "cyan")

        result = self.processor.convert_document(
            file_content=sample_document_content,
            filename="test.pdf",
            use_cache=False
        )

        # Verify result structure
        assert "docling_document" in result
        assert "filename" in result
        assert "page_count" in result
        assert "file_size" in result

        assert result["filename"] == "test.pdf"
        assert result["page_count"] >= 1
        assert result["file_size"] == len(sample_document_content)

        cprint(f"[TEST] ✓ PDF conversion successful: {result['page_count']} pages", "green")

    def test_convert_document_with_cache(self, sample_document_content):
        """Test document caching functionality"""
        cprint("\n[TEST] Testing document caching", "cyan")

        # First conversion (cache miss)
        result1 = self.processor.convert_document(
            file_content=sample_document_content,
            filename="test.pdf",
            use_cache=True
        )

        # Second conversion (cache hit)
        result2 = self.processor.convert_document(
            file_content=sample_document_content,
            filename="test.pdf",
            use_cache=True
        )

        # Both results should be identical
        assert result1["filename"] == result2["filename"]
        assert result1["page_count"] == result2["page_count"]
        assert result1["file_size"] == result2["file_size"]

        cprint("[TEST] ✓ Cache hit successful - both conversions return same result", "green")

    def test_convert_document_docx(self, sample_docx_content):
        """Test DOCX document conversion"""
        cprint("\n[TEST] Testing DOCX document conversion", "cyan")

        result = self.processor.convert_document(
            file_content=sample_docx_content,
            filename="test.docx",
            use_cache=False
        )

        # Verify result structure
        assert "docling_document" in result
        assert "filename" in result
        assert "page_count" in result
        assert "file_size" in result

        assert result["filename"] == "test.docx"
        assert result["page_count"] >= 1

        cprint(f"[TEST] ✓ DOCX conversion successful: {result['page_count']} pages", "green")

    def test_convert_document_invalid_content(self):
        """Test conversion with invalid PDF content"""
        cprint("\n[TEST] Testing conversion with invalid content", "cyan")

        invalid_content = b"This is not a valid PDF"

        with pytest.raises(Exception):
            self.processor.convert_document(
                file_content=invalid_content,
                filename="invalid.pdf",
                use_cache=False
            )

        cprint("[TEST] ✓ Invalid content rejected as expected", "green")

    def test_convert_document_cache_disabled(self, sample_document_content):
        """Test conversion with caching disabled"""
        cprint("\n[TEST] Testing conversion with cache disabled", "cyan")

        # Convert twice with cache disabled
        result1 = self.processor.convert_document(
            file_content=sample_document_content,
            filename="test.pdf",
            use_cache=False
        )

        result2 = self.processor.convert_document(
            file_content=sample_document_content,
            filename="test.pdf",
            use_cache=False
        )

        # Results should be equivalent but not from cache
        assert result1["filename"] == result2["filename"]
        assert result1["page_count"] == result2["page_count"]

        cprint("[TEST] ✓ Both conversions completed without cache", "green")


@pytest.mark.unit
class TestDocumentCache:
    """Test suite for document cache functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        document_cache.clear_all()
        yield
        document_cache.clear_all()

    def test_cache_set_and_get(self, sample_document_content):
        """Test setting and getting cache"""
        cprint("\n[TEST] Testing cache set and get", "cyan")

        test_data = {
            "filename": "test.pdf",
            "page_count": 5,
            "file_size": len(sample_document_content)
        }

        # Set cache
        document_cache.set(sample_document_content, test_data)

        # Get cache
        cached_data = document_cache.get(sample_document_content)

        assert cached_data is not None
        assert cached_data["filename"] == test_data["filename"]
        assert cached_data["page_count"] == test_data["page_count"]

        cprint("[TEST] ✓ Cache set and get successful", "green")

    def test_cache_miss(self):
        """Test cache miss scenario"""
        cprint("\n[TEST] Testing cache miss", "cyan")

        non_existent_content = b"This content was never cached"

        result = document_cache.get(non_existent_content)

        assert result is None

        cprint("[TEST] ✓ Cache miss returns None as expected", "green")

    def test_cache_clear(self, sample_document_content):
        """Test cache clearing"""
        cprint("\n[TEST] Testing cache clear", "cyan")

        # Set cache
        test_data = {"filename": "test.pdf"}
        document_cache.set(sample_document_content, test_data)

        # Verify cache exists
        assert document_cache.get(sample_document_content) is not None

        # Clear cache
        document_cache.clear_all()

        # Verify cache is cleared
        assert document_cache.get(sample_document_content) is None

        cprint("[TEST] ✓ Cache cleared successfully", "green")
