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
    """Test sentence splitting uses SpaCy directly"""
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
        print(f"  {i}. '{chunk['text']}'")

    # Should get 3 individual sentences
    assert len(result) == 3, f"Expected 3 sentences, got {len(result)}"
    assert "First" in result[0]["text"]
    assert "Second" in result[1]["text"]
    assert "Third" in result[2]["text"]

    print("\n✓ PASSED: Sentence splitting produces individual sentences")


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


def main():
    print("\n" + "="*80)
    print("LANGCHAIN CHUNKING FIXES VERIFICATION")
    print("="*80)

    try:
        test_paragraph_splitter()
        test_sentence_splitting()
        test_legal_text_splitting()
        test_no_langchain_spacytextsplitter()

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
        print("")
        print("3. Code Quality:")
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
