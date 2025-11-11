"""
Simple test to verify LangChain chunking fixes
Run this inside the backend container: python test_langchain_fixes.py
"""
import sys
from app.chunker import DocumentChunker


def test_paragraph_splitter():
    """Test paragraph splitter configuration"""
    print("\n" + "="*80)
    print("TEST 1: Paragraph Splitter Configuration")
    print("="*80)

    chunker = DocumentChunker()
    splitter = chunker.paragraph_splitter

    print(f"✓ chunk_size: {splitter._chunk_size}")
    print(f"✓ chunk_overlap: {splitter._chunk_overlap}")
    print(f"✓ separators: {splitter._separators}")
    print(f"✓ keep_separator: {splitter._keep_separator}")

    # Verify enhanced configuration
    assert splitter._chunk_size == 1000
    assert splitter._chunk_overlap == 100
    assert splitter._keep_separator == 'end', "keep_separator should be 'end'"
    assert "; " in splitter._separators, "Should include semicolon separator"
    assert ": " in splitter._separators, "Should include colon separator"

    print("\n✓ PASSED: Paragraph splitter has enhanced legal document configuration")


def test_sentence_splitting():
    """Test sentence splitting uses SpaCy directly and tracks base_chunk_index"""
    print("\n" + "="*80)
    print("TEST 2: Sentence Splitting Implementation")
    print("="*80)

    chunker = DocumentChunker()

    # Test text with clear sentence boundaries
    test_text = "First sentence. Second sentence. Third sentence."

    base_chunks = [{
        "text": test_text,
        "page_number": 1,
        "is_overlap": False
    }]

    result = chunker._apply_sentence_splitting(base_chunks)

    print(f"\nInput text: {test_text}")
    print(f"Number of sentences detected: {len(result)}")
    print("\nSentences:")
    for i, chunk in enumerate(result, 1):
        print(f"  {i}. '{chunk['text']}' (base_chunk_index: {chunk.get('base_chunk_index')})")

    # Should get 3 individual sentences
    assert len(result) == 3, f"Expected 3 sentences, got {len(result)}"
    assert "First" in result[0]["text"]
    assert "Second" in result[1]["text"]
    assert "Third" in result[2]["text"]

    # All should have same base_chunk_index (0 since it's the first base chunk)
    assert result[0].get("base_chunk_index") == 0
    assert result[1].get("base_chunk_index") == 0
    assert result[2].get("base_chunk_index") == 0

    print("\n✓ PASSED: Sentence splitting produces individual sentences with base_chunk_index")


def test_legal_text_splitting():
    """Test with legal-style text"""
    print("\n" + "="*80)
    print("TEST 3: Legal Document Text Splitting")
    print("="*80)

    chunker = DocumentChunker()

    legal_text = (
        "The Agreement is subject to the following terms: "
        "(a) payment within 30 days; "
        "(b) interest at 5%; "
        "and (c) arbitration. "
        "This is binding. "
        "Each party has authority."
    )

    base_chunks = [{
        "text": legal_text,
        "page_number": 1,
        "is_overlap": False
    }]

    result = chunker._apply_sentence_splitting(base_chunks)

    print(f"\nInput: {legal_text}")
    print(f"\nDetected {len(result)} sentences:")
    for i, chunk in enumerate(result, 1):
        print(f"  {i}. {chunk['text']}")

    # Should detect at least 3 sentences
    assert len(result) >= 3, f"Expected at least 3 sentences in legal text"

    print("\n✓ PASSED: Legal text correctly split into sentences")


def test_no_langchain_spacytextsplitter():
    """Verify we're not using SpacyTextSplitter anymore"""
    print("\n" + "="*80)
    print("TEST 4: Verify No SpacyTextSplitter Usage")
    print("="*80)

    chunker = DocumentChunker()

    # Check that we have nlp property, not sentence_splitter
    assert hasattr(chunker, 'nlp'), "Should have nlp property"
    assert hasattr(chunker, '_nlp'), "Should have _nlp attribute"

    # Verify nlp loads SpaCy model directly
    nlp = chunker.nlp
    assert nlp is not None, "nlp should load SpaCy model"

    # Check it's a SpaCy Language object, not SpacyTextSplitter
    import spacy
    assert isinstance(nlp, spacy.language.Language), "Should be SpaCy Language object"

    print(f"✓ nlp type: {type(nlp)}")
    print(f"✓ Using SpaCy directly: {isinstance(nlp, spacy.language.Language)}")

    print("\n✓ PASSED: Using SpaCy directly, not SpacyTextSplitter")


def test_hierarchical_numbering():
    """Test hierarchical item numbering in sentence mode"""
    print("\n" + "="*80)
    print("TEST 5: Hierarchical Item Numbering")
    print("="*80)

    from app.models import ChunkingMode
    chunker = DocumentChunker()

    # Simulate two base chunks, each with multiple sentences
    base_chunks = [
        {
            "text": "First base chunk, sentence one. First base chunk, sentence two.",
            "page_number": 1,
            "is_overlap": False
        },
        {
            "text": "Second base chunk, sentence one. Second base chunk, sentence two. Second base chunk, sentence three.",
            "page_number": 1,
            "is_overlap": False
        }
    ]

    # Apply sentence splitting
    sentence_chunks = chunker._apply_sentence_splitting(base_chunks)

    print(f"\nInput: {len(base_chunks)} base chunks")
    print(f"Output: {len(sentence_chunks)} sentences")

    # Assign hierarchical numbers for sentence mode
    final_chunks = chunker._assign_item_numbers(sentence_chunks, ChunkingMode.SENTENCE)

    print("\nHierarchical numbering:")
    for chunk in final_chunks:
        print(f"  Item {chunk.item_number}: {chunk.text}")

    # Verify hierarchical numbering
    assert len(final_chunks) == 5, f"Expected 5 sentences total, got {len(final_chunks)}"

    # First base chunk sentences should be 1.1, 1.2
    assert final_chunks[0].item_number == "1.1", f"Expected 1.1, got {final_chunks[0].item_number}"
    assert final_chunks[1].item_number == "1.2", f"Expected 1.2, got {final_chunks[1].item_number}"

    # Second base chunk sentences should be 2.1, 2.2, 2.3
    assert final_chunks[2].item_number == "2.1", f"Expected 2.1, got {final_chunks[2].item_number}"
    assert final_chunks[3].item_number == "2.2", f"Expected 2.2, got {final_chunks[3].item_number}"
    assert final_chunks[4].item_number == "2.3", f"Expected 2.3, got {final_chunks[4].item_number}"

    print("\n✓ PASSED: Hierarchical numbering works correctly (1.1, 1.2, 2.1, 2.2, 2.3)")


def test_paragraph_mode_numbering():
    """Test that paragraph mode still uses simple numbering"""
    print("\n" + "="*80)
    print("TEST 6: Paragraph Mode Simple Numbering")
    print("="*80)

    from app.models import ChunkingMode
    chunker = DocumentChunker()

    # Simulate paragraph chunks (no base_chunk_index)
    paragraph_chunks = [
        {"text": "Paragraph 1", "page_number": 1, "is_overlap": False},
        {"text": "Paragraph 2", "page_number": 1, "is_overlap": False},
        {"text": "Paragraph 3", "page_number": 1, "is_overlap": False}
    ]

    # Assign simple numbers for paragraph mode
    final_chunks = chunker._assign_item_numbers(paragraph_chunks, ChunkingMode.PARAGRAPH)

    print("\nParagraph mode numbering:")
    for chunk in final_chunks:
        print(f"  Item {chunk.item_number}: {chunk.text}")

    # Verify simple sequential numbering
    assert final_chunks[0].item_number == "1", f"Expected '1', got {final_chunks[0].item_number}"
    assert final_chunks[1].item_number == "2", f"Expected '2', got {final_chunks[1].item_number}"
    assert final_chunks[2].item_number == "3", f"Expected '3', got {final_chunks[2].item_number}"

    print("\n✓ PASSED: Paragraph mode uses simple numbering (1, 2, 3)")


def main():
    print("\n" + "="*80)
    print("LANGCHAIN CHUNKING FIXES VERIFICATION")
    print("="*80)

    try:
        test_paragraph_splitter()
        test_sentence_splitting()
        test_legal_text_splitting()
        test_no_langchain_spacytextsplitter()
        test_hierarchical_numbering()
        test_paragraph_mode_numbering()

        print("\n" + "="*80)
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("="*80)

        print("\nSUMMARY OF FIXES:")
        print("-" * 80)
        print("1. RecursiveCharacterTextSplitter (Paragraph Mode):")
        print("   ✓ Added keep_separator='end' to preserve punctuation")
        print("   ✓ Enhanced separators: '; ' and ': ' for legal documents")
        print("   ✓ Separators: ['\\n\\n', '\\n', '. ', '.\\n', '! ', '? ', '; ', ': ', ' ', '']")
        print("")
        print("2. Sentence Splitting:")
        print("   ✓ Replaced SpacyTextSplitter with direct SpaCy usage")
        print("   ✓ Now produces TRUE individual sentences")
        print("   ✓ Fixed issue where chunk_size=1000 was grouping sentences")
        print("   ✓ Uses doc.sents for accurate sentence boundary detection")
        print("   ✓ Tracks base_chunk_index to preserve paragraph structure")
        print("")
        print("3. Hierarchical Item Numbering:")
        print("   ✓ Sentence mode: Hierarchical numbering (1.1, 1.2, 2.1, 2.2...)")
        print("   ✓ Paragraph mode: Simple numbering (1, 2, 3...)")
        print("   ✓ Changed item_number from int to str in DocumentChunk model")
        print("   ✓ Each sentence preserves relationship to parent paragraph")
        print("")
        print("4. Code Quality:")
        print("   ✓ Removed unused SpacyTextSplitter import")
        print("   ✓ Cleaner lazy-loading of SpaCy model")
        print("   ✓ Better documentation in code comments")
        print("="*80)

        return 0

    except AssertionError as e:
        print("\n" + "="*80)
        print(f"✗✗✗ TEST FAILED ✗✗✗")
        print("="*80)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print("\n" + "="*80)
        print(f"✗✗✗ ERROR ✗✗✗")
        print("="*80)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
