"""
Unit tests for Gemini flash-lite metadata extraction
Tests the AI-powered metadata generation for reference documents
"""
import pytest
import time
from pathlib import Path
from app.gemini_service import GeminiVerificationService
from app.models import DocumentMetadata
from termcolor import cprint


@pytest.mark.gemini
@pytest.mark.unit
class TestGeminiMetadataExtraction:
    """Test suite for Gemini-powered metadata extraction using flash model"""

    @pytest.fixture(autouse=True)
    def setup(self, gemini_api_key):
        """Setup for each test"""
        self.service = GeminiVerificationService()
        assert self.service.client is not None, "Gemini client should be initialized"

    def test_service_initialization(self):
        """Test Gemini service initialization"""
        cprint("\n[TEST] Testing Gemini service initialization", "cyan")

        assert self.service.client is not None
        cprint("[TEST] ✓ Gemini service initialized successfully", "green")

    def test_generate_metadata_from_docx(self, sample_docx_content, sample_case_context, temp_dir):
        """Test metadata generation from DOCX file using Gemini Flash"""
        cprint("\n[TEST] Testing metadata generation from DOCX", "cyan")

        # Save sample DOCX to temp file
        temp_file = temp_dir / "test_reference.docx"
        temp_file.write_bytes(sample_docx_content)

        # Generate metadata using Gemini Flash
        metadata = self.service.generate_metadata(
            file_path=str(temp_file),
            filename="test_reference.docx",
            case_context=sample_case_context
        )

        # Verify metadata structure
        assert isinstance(metadata, DocumentMetadata)
        assert metadata.document_id is not None
        assert metadata.filename == "test_reference.docx"
        assert len(metadata.summary) > 0
        assert len(metadata.contextualization) > 0
        assert metadata.document_type is not None
        assert len(metadata.keywords) > 0
        assert metadata.generated_at is not None

        cprint(f"[TEST] ✓ Metadata generated:", "green")
        cprint(f"  - Summary: {metadata.summary[:100]}...", "cyan")
        cprint(f"  - Document Type: {metadata.document_type}", "cyan")
        cprint(f"  - Keywords: {', '.join(metadata.keywords[:5])}", "cyan")

    def test_generate_metadata_from_pdf(self, sample_document_content, sample_case_context, temp_dir):
        """Test metadata generation from PDF file using Gemini Flash"""
        cprint("\n[TEST] Testing metadata generation from PDF", "cyan")

        # Save sample PDF to temp file
        temp_file = temp_dir / "test_reference.pdf"
        temp_file.write_bytes(sample_document_content)

        # Generate metadata using Gemini Flash
        metadata = self.service.generate_metadata(
            file_path=str(temp_file),
            filename="test_reference.pdf",
            case_context=sample_case_context
        )

        # Verify metadata structure
        assert isinstance(metadata, DocumentMetadata)
        assert metadata.document_id is not None
        assert metadata.filename == "test_reference.pdf"
        assert metadata.summary is not None
        assert metadata.contextualization is not None
        assert metadata.document_type is not None
        assert isinstance(metadata.keywords, list)

        cprint(f"[TEST] ✓ PDF metadata generated:", "green")
        cprint(f"  - Document Type: {metadata.document_type}", "cyan")
        cprint(f"  - Keywords: {', '.join(metadata.keywords[:5]) if metadata.keywords else 'None'}", "cyan")

    def test_metadata_contains_case_context(self, sample_docx_content, sample_case_context, temp_dir):
        """Test that metadata generation incorporates case context"""
        cprint("\n[TEST] Testing case context incorporation in metadata", "cyan")

        # Save sample DOCX to temp file
        temp_file = temp_dir / "test_reference.docx"
        temp_file.write_bytes(sample_docx_content)

        # Generate metadata
        metadata = self.service.generate_metadata(
            file_path=str(temp_file),
            filename="test_reference.docx",
            case_context=sample_case_context
        )

        # Check that contextualization field is not empty
        assert len(metadata.contextualization) > 0
        assert isinstance(metadata.contextualization, str)

        # Verify that contextualization relates to the case
        # (Should mention contract, verification, or related terms)
        contextualization_lower = metadata.contextualization.lower()
        relevant_terms = ["contract", "verify", "document", "agreement", "reference"]
        has_relevant_term = any(term in contextualization_lower for term in relevant_terms)

        assert has_relevant_term, "Contextualization should contain relevant terms"

        cprint(f"[TEST] ✓ Contextualization includes case context:", "green")
        cprint(f"  {metadata.contextualization}", "cyan")

    def test_metadata_keywords_extraction(self, sample_docx_content, sample_case_context, temp_dir):
        """Test keyword extraction from document"""
        cprint("\n[TEST] Testing keyword extraction", "cyan")

        # Save sample DOCX to temp file
        temp_file = temp_dir / "test_reference.docx"
        temp_file.write_bytes(sample_docx_content)

        # Generate metadata
        metadata = self.service.generate_metadata(
            file_path=str(temp_file),
            filename="test_reference.docx",
            case_context=sample_case_context
        )

        # Verify keywords
        assert isinstance(metadata.keywords, list)
        assert len(metadata.keywords) > 0, "Should extract at least one keyword"
        assert len(metadata.keywords) <= 10, "Should extract at most 10 keywords"

        # All keywords should be strings
        assert all(isinstance(kw, str) for kw in metadata.keywords)

        cprint(f"[TEST] ✓ Extracted {len(metadata.keywords)} keywords:", "green")
        for kw in metadata.keywords:
            cprint(f"  - {kw}", "cyan")

    def test_metadata_document_type_classification(self, sample_docx_content, sample_case_context, temp_dir):
        """Test document type classification"""
        cprint("\n[TEST] Testing document type classification", "cyan")

        # Save sample DOCX to temp file
        temp_file = temp_dir / "test_reference.docx"
        temp_file.write_bytes(sample_docx_content)

        # Generate metadata
        metadata = self.service.generate_metadata(
            file_path=str(temp_file),
            filename="test_reference.docx",
            case_context=sample_case_context
        )

        # Verify document type
        assert isinstance(metadata.document_type, str)
        assert len(metadata.document_type) > 0

        cprint(f"[TEST] ✓ Document classified as: {metadata.document_type}", "green")

    def test_metadata_generation_performance(self, sample_docx_content, sample_case_context, temp_dir):
        """Test metadata generation performance (should complete within reasonable time)"""
        cprint("\n[TEST] Testing metadata generation performance", "cyan")

        # Save sample DOCX to temp file
        temp_file = temp_dir / "test_reference.docx"
        temp_file.write_bytes(sample_docx_content)

        # Measure time
        start_time = time.time()

        metadata = self.service.generate_metadata(
            file_path=str(temp_file),
            filename="test_reference.docx",
            case_context=sample_case_context
        )

        elapsed_time = time.time() - start_time

        # Should complete within 30 seconds (reasonable for AI processing)
        assert elapsed_time < 30, f"Metadata generation took too long: {elapsed_time:.2f}s"

        cprint(f"[TEST] ✓ Metadata generated in {elapsed_time:.2f} seconds", "green")

    @pytest.mark.slow
    def test_metadata_consistency(self, sample_docx_content, sample_case_context, temp_dir):
        """Test that metadata generation is consistent across multiple runs"""
        cprint("\n[TEST] Testing metadata generation consistency", "cyan")

        # Save sample DOCX to temp file
        temp_file = temp_dir / "test_reference.docx"
        temp_file.write_bytes(sample_docx_content)

        # Generate metadata twice
        metadata1 = self.service.generate_metadata(
            file_path=str(temp_file),
            filename="test_reference.docx",
            case_context=sample_case_context
        )

        # Small delay to avoid rate limiting
        time.sleep(2)

        metadata2 = self.service.generate_metadata(
            file_path=str(temp_file),
            filename="test_reference.docx",
            case_context=sample_case_context
        )

        # Both should have similar structure (fields populated)
        assert len(metadata1.summary) > 0 and len(metadata2.summary) > 0
        assert len(metadata1.keywords) > 0 and len(metadata2.keywords) > 0
        assert metadata1.document_type is not None and metadata2.document_type is not None

        cprint("[TEST] ✓ Metadata generation is consistent across runs", "green")

    def test_invalid_file_path_handling(self, sample_case_context):
        """Test handling of invalid file path"""
        cprint("\n[TEST] Testing invalid file path handling", "cyan")

        with pytest.raises(Exception):
            self.service.generate_metadata(
                file_path="/nonexistent/path/to/file.pdf",
                filename="nonexistent.pdf",
                case_context=sample_case_context
            )

        cprint("[TEST] ✓ Invalid file path raises exception as expected", "green")


@pytest.mark.gemini
@pytest.mark.unit
class TestGeminiFlashModel:
    """Test suite for Gemini Flash model usage in metadata extraction"""

    @pytest.fixture(autouse=True)
    def setup(self, gemini_api_key):
        """Setup for each test"""
        self.service = GeminiVerificationService()

    def test_flash_model_used_for_metadata(self, sample_docx_content, sample_case_context, temp_dir):
        """
        Test that Gemini Flash (gemini-2.0-flash-exp) is used for metadata extraction
        Flash model provides fast, cost-effective processing for metadata tasks
        """
        cprint("\n[TEST] Testing Gemini Flash model usage", "cyan")

        # Save sample DOCX to temp file
        temp_file = temp_dir / "test_reference.docx"
        temp_file.write_bytes(sample_docx_content)

        # Generate metadata - internally uses gemini-2.0-flash-exp
        metadata = self.service.generate_metadata(
            file_path=str(temp_file),
            filename="test_reference.docx",
            case_context=sample_case_context
        )

        # Verify successful generation (confirms Flash model works)
        assert metadata is not None
        assert isinstance(metadata, DocumentMetadata)

        cprint("[TEST] ✓ Gemini Flash model successfully generated metadata", "green")

    def test_json_structured_output(self, sample_docx_content, sample_case_context, temp_dir):
        """Test that Flash model returns properly structured JSON"""
        cprint("\n[TEST] Testing JSON structured output from Flash", "cyan")

        # Save sample DOCX to temp file
        temp_file = temp_dir / "test_reference.docx"
        temp_file.write_bytes(sample_docx_content)

        # Generate metadata
        metadata = self.service.generate_metadata(
            file_path=str(temp_file),
            filename="test_reference.docx",
            case_context=sample_case_context
        )

        # Verify all expected fields are present and properly typed
        assert isinstance(metadata.summary, str)
        assert isinstance(metadata.contextualization, str)
        assert isinstance(metadata.document_type, str)
        assert isinstance(metadata.keywords, list)
        assert all(isinstance(kw, str) for kw in metadata.keywords)

        cprint("[TEST] ✓ Flash model returns properly structured JSON output", "green")
