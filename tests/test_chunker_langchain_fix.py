"""
Test to verify LangChain chunking fixes are working correctly
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.chunker import DocumentChunker
from app.models import ChunkingMode


def test_paragraph_splitter_configuration():
    """Test that RecursiveCharacterTextSplitter is configured correctly"""
    print("\n[TEST] Testing paragraph splitter configuration...")

    chunker = DocumentChunker()

    # Check that paragraph_splitter exists
    assert hasattr(chunker, 'paragraph_splitter'), "paragraph_splitter should exist"

    # Verify configuration
    splitter = chunker.paragraph_splitter
    assert splitter._chunk_size == 1000, "chunk_size should be 1000"
    assert splitter._chunk_overlap == 100, "chunk_overlap should be 100"

    # Check for enhanced separators (including legal document separators)
    expected_separators = ["\n\n", "\n", ". ", ".\n", "! ", "? ", "; ", ": ", " ", ""]
    actual_separators = splitter._separators
    assert actual_separators == expected_separators, f"Separators mismatch: {actual_separators}"

    # Check keep_separator is set to 'end'
    assert splitter._keep_separator == 'end', "keep_separator should be 'end'"

    print("✓ Paragraph splitter configuration is correct")
    print(f"  - chunk_size: {splitter._chunk_size}")
    print(f"  - chunk_overlap: {splitter._chunk_overlap}")
    print(f"  - separators: {actual_separators}")
    print(f"  - keep_separator: {splitter._keep_separator}")


def test_sentence_splitting_uses_spacy_directly():
    """Test that sentence splitting uses SpaCy directly, not SpacyTextSplitter"""
    print("\n[TEST] Testing sentence splitting implementation...")

    chunker = DocumentChunker()

    # Check that _nlp exists for direct SpaCy usage
    assert hasattr(chunker, '_nlp'), "_nlp attribute should exist"
    assert hasattr(chunker, 'nlp'), "nlp property should exist"

    # Test that the nlp property loads SpaCy correctly
    test_text = "This is sentence one. This is sentence two. This is sentence three."

    # Create a mock base chunk
    base_chunks = [{
        "text": test_text,
        "page_number": 1,
        "is_overlap": False
    }]

    # Apply sentence splitting
    result = chunker._apply_sentence_splitting(base_chunks)

    # Verify we get individual sentences
    assert len(result) == 3, f"Expected 3 sentences, got {len(result)}"

    # Verify each chunk contains only one sentence
    assert "sentence one" in result[0]["text"].lower(), "First sentence should contain 'sentence one'"
    assert "sentence two" in result[1]["text"].lower(), "Second sentence should contain 'sentence two'"
    assert "sentence three" in result[2]["text"].lower(), "Third sentence should contain 'sentence three'"

    print("✓ Sentence splitting produces individual sentences")
    print(f"  - Input: {test_text}")
    print(f"  - Output: {len(result)} individual sentences")
    for i, chunk in enumerate(result, 1):
        print(f"    {i}. {chunk['text']}")


def test_complex_sentence_splitting():
    """Test sentence splitting with more complex legal-style text"""
    print("\n[TEST] Testing complex sentence splitting...")

    chunker = DocumentChunker()

    # Legal-style text with semicolons and colons
    test_text = (
        "The parties agree as follows: (a) payment shall be made within 30 days; "
        "(b) interest will accrue at 5% per annum; and (c) disputes will be resolved by arbitration. "
        "This agreement is binding. Each party represents that they have authority to enter into this agreement."
    )

    base_chunks = [{
        "text": test_text,
        "page_number": 1,
        "is_overlap": False
    }]

    # Apply sentence splitting
    result = chunker._apply_sentence_splitting(base_chunks)

    # SpaCy should detect 3 sentences:
    # 1. "The parties agree as follows: (a) payment shall be made within 30 days; (b) interest will accrue at 5% per annum; and (c) disputes will be resolved by arbitration."
    # 2. "This agreement is binding."
    # 3. "Each party represents that they have authority to enter into this agreement."

    print(f"✓ Complex text split into {len(result)} sentences")
    for i, chunk in enumerate(result, 1):
        print(f"  {i}. {chunk['text']}")

    # Verify at least 3 sentences detected
    assert len(result) >= 3, f"Expected at least 3 sentences, got {len(result)}"


def test_paragraph_splitting_preserves_punctuation():
    """Test that paragraph splitting preserves punctuation at chunk ends"""
    print("\n[TEST] Testing paragraph splitting preserves punctuation...")

    chunker = DocumentChunker()

    # Create text that will need to be split
    long_text = "This is a sentence. " * 100  # Create text longer than chunk_size

    base_chunks = [{
        "text": long_text.strip(),
        "page_number": 1,
        "is_overlap": False
    }]

    # Apply paragraph splitting
    result = chunker._apply_paragraph_splitting(base_chunks)

    # With keep_separator='end', periods should be preserved
    chunks_with_periods = [r for r in result if r["text"].endswith(".")]

    print(f"✓ Paragraph splitting produced {len(result)} chunks")
    print(f"  - Chunks ending with period: {len(chunks_with_periods)}/{len(result)}")

    # Most chunks should end with a period (keep_separator='end')
    # Some might not if they're at boundaries, but majority should
    if len(result) > 1:
        assert len(chunks_with_periods) >= len(result) // 2, "Most chunks should preserve punctuation"


def main():
    """Run all tests"""
    print("=" * 80)
    print("Testing LangChain Chunking Fixes")
    print("=" * 80)

    try:
        test_paragraph_splitter_configuration()
        test_sentence_splitting_uses_spacy_directly()
        test_complex_sentence_splitting()
        test_paragraph_splitting_preserves_punctuation()

        print("\n" + "=" * 80)
        print("✓ ALL TESTS PASSED")
        print("=" * 80)
        print("\nSummary of fixes:")
        print("1. RecursiveCharacterTextSplitter now includes:")
        print("   - Legal document separators (; : etc.)")
        print("   - keep_separator='end' to preserve punctuation")
        print("\n2. Sentence splitting now uses direct SpaCy instead of SpacyTextSplitter:")
        print("   - Produces true individual sentences")
        print("   - No longer groups sentences due to chunk_size")
        print("   - More accurate sentence boundary detection")

        return 0

    except AssertionError as e:
        print("\n" + "=" * 80)
        print(f"✗ TEST FAILED: {e}")
        print("=" * 80)
        return 1
    except Exception as e:
        print("\n" + "=" * 80)
        print(f"✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 80)
        return 1


if __name__ == "__main__":
    exit(main())
