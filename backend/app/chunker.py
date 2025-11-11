"""
Document chunking module with HierarchicalChunker, paragraph, and sentence modes
"""
from typing import List, Dict, Any
from termcolor import cprint
from docling_core.types.doc import DoclingDocument
from docling.chunking import HybridChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.models import DocumentChunk, ChunkingMode


class DocumentChunker:
    """Handles document chunking with different strategies"""

    def __init__(self):
        """Initialize chunkers"""
        cprint("[CHUNKER] Initializing chunking strategies...", "cyan")

        # Initialize HybridChunker (Docling's hierarchical chunker)
        self.hierarchical_chunker = HybridChunker()

        # Initialize paragraph-level splitter (LangChain)
        # Enhanced with legal document-specific separators and keep_separator
        self.paragraph_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len,
            separators=["\n\n", "\n", ". ", ".\n", "! ", "? ", "; ", ": ", " ", ""],
            keep_separator='end'  # Preserve punctuation at chunk boundaries
        )

        # Initialize SpaCy for sentence-level splitting
        # This will be lazy-loaded when needed to avoid loading spacy model at startup
        self._nlp = None

        cprint("[CHUNKER] Chunking strategies initialized", "green")

    @property
    def nlp(self):
        """Lazy load SpaCy NLP model for sentence splitting"""
        if self._nlp is None:
            cprint("[CHUNKER] Loading SpaCy model for sentence splitting...", "cyan")
            # Download spacy model if not already installed
            import spacy
            try:
                self._nlp = spacy.load("en_core_web_sm")
            except OSError:
                cprint("[CHUNKER] Downloading spacy model en_core_web_sm...", "yellow")
                import subprocess
                subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
                self._nlp = spacy.load("en_core_web_sm")

            cprint("[CHUNKER] SpaCy model ready for sentence splitting", "green")

        return self._nlp

    def _get_page_number_from_chunk(self, chunk: Any) -> int:
        """
        Extract page number from Docling chunk metadata

        Args:
            chunk: Docling chunk object

        Returns:
            Page number (1-indexed)
        """
        try:
            # Try to get page number from chunk metadata
            if hasattr(chunk, 'meta') and hasattr(chunk.meta, 'doc_items'):
                # Get the first doc_item to determine page
                doc_items = chunk.meta.doc_items
                if doc_items and len(doc_items) > 0:
                    # doc_items contain references to source elements
                    # Try to get page from first item
                    first_item = doc_items[0]
                    if hasattr(first_item, 'prov') and first_item.prov:
                        # Provenance contains page information
                        page_no = first_item.prov[0].page_no if first_item.prov[0].page_no is not None else 1
                        return page_no + 1  # Convert to 1-indexed

            # Fallback: try direct page attribute
            if hasattr(chunk, 'page'):
                return chunk.page + 1

            # Default to page 1 if we can't determine
            return 1

        except Exception as e:
            cprint(f"[CHUNKER] Warning: Could not extract page number: {e}", "yellow")
            return 1

    def _detect_overlap(self, chunk: Any) -> bool:
        """
        Detect if chunk spans multiple pages using provenance data

        Args:
            chunk: Docling chunk object

        Returns:
            True if chunk continues from previous page
        """
        try:
            if hasattr(chunk, 'meta') and hasattr(chunk.meta, 'doc_items'):
                doc_items = chunk.meta.doc_items
                if doc_items and len(doc_items) > 0:
                    # Check if first item has provenance indicating multi-page span
                    first_item = doc_items[0]
                    if hasattr(first_item, 'prov') and first_item.prov:
                        # If there are multiple provenance entries, it spans pages
                        if len(first_item.prov) > 1:
                            return True

                        # Check if the provenance indicates partial text
                        # (This is a heuristic - may need adjustment based on actual Docling behavior)
                        prov = first_item.prov[0]
                        if hasattr(prov, 'charspan'):
                            # If charspan starts at 0, it's likely the beginning of content
                            # Otherwise, it might be a continuation
                            return prov.charspan[0] > 0

            return False

        except Exception as e:
            cprint(f"[CHUNKER] Warning: Could not detect overlap: {e}", "yellow")
            return False

    def _apply_hierarchical_chunking(self, docling_document: DoclingDocument) -> List[Dict[str, Any]]:
        """
        Apply HierarchicalChunker (base processing)

        Args:
            docling_document: Docling document object

        Returns:
            List of chunk dictionaries with metadata
        """
        cprint("[CHUNKER] Applying HierarchicalChunker...", "cyan")

        chunks = []
        try:
            # Use HybridChunker to get base chunks
            chunk_iter = self.hierarchical_chunker.chunk(docling_document)

            for chunk in chunk_iter:
                # Extract text
                text = chunk.text if hasattr(chunk, 'text') else str(chunk)

                # Skip empty chunks
                if not text or not text.strip():
                    continue

                # Extract metadata
                page_number = self._get_page_number_from_chunk(chunk)
                is_overlap = self._detect_overlap(chunk)

                chunks.append({
                    "text": text.strip(),
                    "page_number": page_number,
                    "is_overlap": is_overlap,
                    "chunk_obj": chunk  # Keep reference for debugging
                })

            cprint(f"[CHUNKER] HierarchicalChunker produced {len(chunks)} chunks", "green")

        except Exception as e:
            cprint(f"[CHUNKER] Error in hierarchical chunking: {e}", "red")
            raise

        return chunks

    def _apply_paragraph_splitting(self, base_chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply paragraph-level splitting on top of hierarchical chunks

        Args:
            base_chunks: Base chunks from HierarchicalChunker

        Returns:
            List of paragraph-level chunks
        """
        cprint("[CHUNKER] Applying paragraph-level splitting...", "cyan")

        paragraph_chunks = []

        for base_chunk in base_chunks:
            text = base_chunk["text"]
            page_number = base_chunk["page_number"]
            is_overlap = base_chunk["is_overlap"]

            # Split text into paragraphs
            paragraphs = self.paragraph_splitter.split_text(text)

            for para in paragraphs:
                if para.strip():
                    paragraph_chunks.append({
                        "text": para.strip(),
                        "page_number": page_number,
                        "is_overlap": is_overlap
                    })

        cprint(f"[CHUNKER] Paragraph splitting produced {len(paragraph_chunks)} chunks", "green")
        return paragraph_chunks

    def _apply_sentence_splitting(self, base_chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply TRUE sentence-level splitting using SpaCy directly

        This implementation uses SpaCy's sentence boundary detection (doc.sents)
        to extract individual sentences, ensuring each chunk contains exactly one sentence.
        This fixes the previous issue where SpacyTextSplitter with chunk_size=1000
        was grouping multiple sentences together.

        Args:
            base_chunks: Base chunks from HierarchicalChunker

        Returns:
            List of sentence-level chunks (one sentence per chunk)
        """
        cprint("[CHUNKER] Applying sentence-level splitting with SpaCy...", "cyan")

        sentence_chunks = []

        for base_chunk in base_chunks:
            text = base_chunk["text"]
            page_number = base_chunk["page_number"]
            is_overlap = base_chunk["is_overlap"]

            # Use SpaCy to detect sentence boundaries
            doc = self.nlp(text)

            # Extract individual sentences
            for sent in doc.sents:
                sentence_text = sent.text.strip()
                if sentence_text:
                    sentence_chunks.append({
                        "text": sentence_text,
                        "page_number": page_number,
                        "is_overlap": is_overlap
                    })

        cprint(f"[CHUNKER] Sentence splitting produced {len(sentence_chunks)} individual sentences", "green")
        return sentence_chunks

    def _assign_item_numbers(self, chunks: List[Dict[str, Any]]) -> List[DocumentChunk]:
        """
        Assign item numbers to chunks (resets per page)

        Args:
            chunks: List of chunk dictionaries

        Returns:
            List of DocumentChunk objects with item numbers
        """
        cprint("[CHUNKER] Assigning item numbers...", "cyan")

        # Sort by page number first
        chunks.sort(key=lambda x: x["page_number"])

        result = []
        current_page = None
        item_number = 0

        for chunk in chunks:
            page_number = chunk["page_number"]

            # Reset item number when page changes
            if current_page != page_number:
                current_page = page_number
                item_number = 1
            else:
                item_number += 1

            # Create DocumentChunk object
            result.append(DocumentChunk(
                page_number=page_number,
                item_number=item_number,
                text=chunk["text"],
                is_overlap=chunk["is_overlap"]
            ))

        cprint(f"[CHUNKER] Assigned item numbers to {len(result)} chunks", "green")
        return result

    def chunk_document(
        self,
        docling_document: DoclingDocument,
        mode: ChunkingMode
    ) -> List[DocumentChunk]:
        """
        Chunk document according to specified mode

        Args:
            docling_document: Docling document object
            mode: Chunking mode (paragraph or sentence)

        Returns:
            List of DocumentChunk objects with metadata
        """
        cprint(f"[CHUNKER] Chunking document in {mode.value} mode...", "cyan")

        # Step 1: Apply HierarchicalChunker (base)
        base_chunks = self._apply_hierarchical_chunking(docling_document)

        # Step 2: Apply mode-specific splitting
        if mode == ChunkingMode.PARAGRAPH:
            chunks = self._apply_paragraph_splitting(base_chunks)
        elif mode == ChunkingMode.SENTENCE:
            chunks = self._apply_sentence_splitting(base_chunks)
        else:
            raise ValueError(f"Unknown chunking mode: {mode}")

        # Step 3: Assign item numbers
        final_chunks = self._assign_item_numbers(chunks)

        cprint(f"[CHUNKER] Chunking complete: {len(final_chunks)} total chunks", "green")
        return final_chunks


# Global chunker instance
document_chunker = DocumentChunker()
