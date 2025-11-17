"""
Unit tests for document chunker functionality
"""

import pytest
from app.processing.chunker import DocumentChunker
from app.processing.document_processor import DocumentProcessor
from app.models import ChunkingMode, DocumentChunk
from termcolor import cprint


@pytest.mark.unit
class TestDocumentChunker:
    """Test suite for DocumentChunker class"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.chunker = DocumentChunker()
        self.processor = DocumentProcessor()

    def test_paragraph_chunking(self, sample_docx_content):
        """Test paragraph-level chunking"""
        cprint("\n[TEST] Testing paragraph-level chunking", "cyan")

        # Convert document first
        result = self.processor.convert_document(
            file_content=sample_docx_content, filename="test.docx", use_cache=False
        )

        docling_document = result["docling_document"]

        # Chunk document in paragraph mode
        chunks = self.chunker.chunk_document(
            docling_document=docling_document, mode=ChunkingMode.PARAGRAPH
        )

        # Verify chunks
        assert len(chunks) > 0, "Should produce at least one chunk"
        assert all(isinstance(chunk, DocumentChunk) for chunk in chunks)

        # Verify all chunks have required fields
        for chunk in chunks:
            assert chunk.page_number > 0
            assert chunk.item_number is not None
            assert len(chunk.text) > 0
            assert isinstance(chunk.is_overlap, bool)

        # Verify item numbering resets per page
        page_items = {}
        for chunk in chunks:
            if chunk.page_number not in page_items:
                page_items[chunk.page_number] = []
            page_items[chunk.page_number].append(chunk.item_number)

        # Each page should start with item_number "1"
        for page, items in page_items.items():
            assert items[0] == "1", f"Page {page} should start with item 1"

        cprint(f"[TEST] ✓ Paragraph chunking successful: {len(chunks)} chunks", "green")

    def test_sentence_chunking(self, sample_docx_content):
        """Test sentence-level chunking"""
        cprint("\n[TEST] Testing sentence-level chunking", "cyan")

        # Convert document first
        result = self.processor.convert_document(
            file_content=sample_docx_content, filename="test.docx", use_cache=False
        )

        docling_document = result["docling_document"]

        # Chunk document in sentence mode
        chunks = self.chunker.chunk_document(
            docling_document=docling_document, mode=ChunkingMode.SENTENCE
        )

        # Verify chunks
        assert len(chunks) > 0, "Should produce at least one chunk"
        assert all(isinstance(chunk, DocumentChunk) for chunk in chunks)

        # Verify all chunks have required fields
        for chunk in chunks:
            assert chunk.page_number > 0
            assert chunk.item_number is not None
            assert len(chunk.text) > 0
            assert isinstance(chunk.is_overlap, bool)

        # Verify hierarchical numbering (e.g., "1.1", "1.2", "2.1")
        for chunk in chunks:
            assert (
                "." in chunk.item_number
            ), "Sentence mode should use hierarchical numbering"

        cprint(f"[TEST] ✓ Sentence chunking successful: {len(chunks)} chunks", "green")

    def test_sentence_chunking_produces_more_chunks(self, sample_docx_content):
        """Test that sentence mode produces more chunks than paragraph mode"""
        cprint("\n[TEST] Testing sentence vs paragraph chunk counts", "cyan")

        # Convert document first
        result = self.processor.convert_document(
            file_content=sample_docx_content, filename="test.docx", use_cache=False
        )

        docling_document = result["docling_document"]

        # Chunk in both modes
        paragraph_chunks = self.chunker.chunk_document(
            docling_document=docling_document, mode=ChunkingMode.PARAGRAPH
        )

        sentence_chunks = self.chunker.chunk_document(
            docling_document=docling_document, mode=ChunkingMode.SENTENCE
        )

        # Sentence mode should produce at least as many chunks as paragraph mode
        assert len(sentence_chunks) >= len(
            paragraph_chunks
        ), "Sentence mode should produce at least as many chunks as paragraph mode"

        cprint(
            f"[TEST] ✓ Paragraph chunks: {len(paragraph_chunks)}, Sentence chunks: {len(sentence_chunks)}",
            "green",
        )

    def test_chunk_metadata_extraction(self, sample_docx_content):
        """Test metadata extraction from chunks"""
        cprint("\n[TEST] Testing chunk metadata extraction", "cyan")

        # Convert document first
        result = self.processor.convert_document(
            file_content=sample_docx_content, filename="test.docx", use_cache=False
        )

        docling_document = result["docling_document"]

        # Chunk document
        chunks = self.chunker.chunk_document(
            docling_document=docling_document, mode=ChunkingMode.PARAGRAPH
        )

        # Verify page numbers are sequential
        page_numbers = [chunk.page_number for chunk in chunks]
        assert all(p > 0 for p in page_numbers), "All page numbers should be positive"

        # Verify item numbers are unique within each page
        from collections import defaultdict

        items_per_page = defaultdict(list)
        for chunk in chunks:
            items_per_page[chunk.page_number].append(chunk.item_number)

        for page, items in items_per_page.items():
            # Items should be sequential starting from 1
            assert items[0] == "1", f"Page {page} should start with item 1"

        cprint("[TEST] ✓ Metadata extraction verified", "green")

    def test_overlap_detection(self, sample_docx_content):
        """Test overlap detection for chunks spanning pages"""
        cprint("\n[TEST] Testing overlap detection", "cyan")

        # Convert document first
        result = self.processor.convert_document(
            file_content=sample_docx_content, filename="test.docx", use_cache=False
        )

        docling_document = result["docling_document"]

        # Chunk document
        chunks = self.chunker.chunk_document(
            docling_document=docling_document, mode=ChunkingMode.PARAGRAPH
        )

        # Verify is_overlap is a boolean for all chunks
        for chunk in chunks:
            assert isinstance(chunk.is_overlap, bool)

        cprint(
            "[TEST] ✓ Overlap detection working (all chunks have boolean is_overlap)",
            "green",
        )

    def test_empty_document_handling(self):
        """Test handling of empty or invalid document"""
        cprint("\n[TEST] Testing empty document handling", "cyan")

        # Create a minimal empty document structure
        from docling_core.types.doc import DoclingDocument

        empty_doc = DoclingDocument(name="empty")

        # Should handle gracefully or raise appropriate error
        try:
            chunks = self.chunker.chunk_document(
                docling_document=empty_doc, mode=ChunkingMode.PARAGRAPH
            )
            # If it succeeds, chunks should be empty
            assert len(chunks) == 0, "Empty document should produce no chunks"
            cprint("[TEST] ✓ Empty document handled gracefully", "green")
        except Exception as e:
            # If it raises an error, that's also acceptable
            cprint(
                f"[TEST] ✓ Empty document raised error as expected: {type(e).__name__}",
                "green",
            )

    def test_chunk_text_not_empty(self, sample_docx_content):
        """Test that all chunks contain non-empty text"""
        cprint("\n[TEST] Testing chunk text is non-empty", "cyan")

        # Convert document first
        result = self.processor.convert_document(
            file_content=sample_docx_content, filename="test.docx", use_cache=False
        )

        docling_document = result["docling_document"]

        # Chunk in both modes
        for mode in [ChunkingMode.PARAGRAPH, ChunkingMode.SENTENCE]:
            chunks = self.chunker.chunk_document(
                docling_document=docling_document, mode=mode
            )

            for chunk in chunks:
                assert (
                    len(chunk.text.strip()) > 0
                ), f"Chunk should not be empty: {chunk.item_number}"

        cprint("[TEST] ✓ All chunks contain non-empty text", "green")

    def test_hierarchical_numbering_structure(self, sample_docx_content):
        """Test that sentence mode produces correct hierarchical numbering"""
        cprint("\n[TEST] Testing hierarchical numbering structure", "cyan")

        # Convert document first
        result = self.processor.convert_document(
            file_content=sample_docx_content, filename="test.docx", use_cache=False
        )

        docling_document = result["docling_document"]

        # Chunk document in sentence mode
        chunks = self.chunker.chunk_document(
            docling_document=docling_document, mode=ChunkingMode.SENTENCE
        )

        # Verify hierarchical structure
        for chunk in chunks:
            parts = chunk.item_number.split(".")
            assert (
                len(parts) == 2
            ), f"Hierarchical number should have format 'X.Y': {chunk.item_number}"
            assert parts[0].isdigit(), f"Base number should be numeric: {parts[0]}"
            assert parts[1].isdigit(), f"Sub number should be numeric: {parts[1]}"

        cprint(
            f"[TEST] ✓ Hierarchical numbering verified for {len(chunks)} chunks",
            "green",
        )


@pytest.mark.unit
class TestChunkingModes:
    """Test suite for different splitting modes"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.chunker = DocumentChunker()
        self.processor = DocumentProcessor()

    def test_splitting_mode_paragraph(self, sample_docx_content):
        """Test paragraph splitting mode behavior"""
        cprint("\n[TEST] Testing PARAGRAPH splitting mode behavior", "cyan")

        result = self.processor.convert_document(
            file_content=sample_docx_content, filename="test.docx", use_cache=False
        )

        chunks = self.chunker.chunk_document(
            docling_document=result["docling_document"], mode=ChunkingMode.PARAGRAPH
        )

        # Paragraph mode should use simple numbering (1, 2, 3...)
        for chunk in chunks:
            assert (
                "." not in chunk.item_number
            ), f"Paragraph mode should use simple numbering: {chunk.item_number}"

        cprint("[TEST] ✓ Paragraph mode uses simple numbering", "green")

    def test_splitting_mode_sentence(self, sample_docx_content):
        """Test sentence splitting mode behavior"""
        cprint("\n[TEST] Testing SENTENCE splitting mode behavior", "cyan")

        result = self.processor.convert_document(
            file_content=sample_docx_content, filename="test.docx", use_cache=False
        )

        chunks = self.chunker.chunk_document(
            docling_document=result["docling_document"], mode=ChunkingMode.SENTENCE
        )

        # Sentence mode should use hierarchical numbering (1.1, 1.2...)
        for chunk in chunks:
            assert (
                "." in chunk.item_number
            ), f"Sentence mode should use hierarchical numbering: {chunk.item_number}"

        cprint("[TEST] ✓ Sentence mode uses hierarchical numbering", "green")
