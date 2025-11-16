"""
Performance test for document processing in Docker environment
Tests PDF and DOCX processing with timing metrics
"""

import time
from pathlib import Path
from termcolor import cprint

# Import processing modules
from app.processing.document_processor import document_processor
from app.processing.chunker import document_chunker
from app.models import ChunkingMode


def test_document_processing(file_path: Path, file_type: str):
    """
    Test document processing performance

    Args:
        file_path: Path to test file
        file_type: Type of file (PDF or DOCX)
    """
    cprint(f"\n{'='*80}", "cyan")
    cprint(f"TESTING: {file_path.name} ({file_type})", "cyan", attrs=["bold"])
    cprint(f"{'='*80}", "cyan")

    # Read file content
    with open(file_path, "rb") as f:
        file_content = f.read()

    file_size_mb = len(file_content) / (1024 * 1024)
    cprint(f"File size: {file_size_mb:.2f} MB", "yellow")

    # Test 1: Document Conversion
    cprint("\n[TEST 1] Document Conversion (Docling)", "cyan", attrs=["bold"])
    start_time = time.time()

    try:
        result = document_processor.convert_document(
            file_content=file_content,
            filename=file_path.name,
            use_cache=False  # Disable cache for accurate timing
        )

        conversion_time = time.time() - start_time
        docling_document = result["docling_document"]
        page_count = result["page_count"]

        cprint(f"✅ Conversion successful", "green")
        cprint(f"   Pages: {page_count}", "white")
        cprint(f"   Time: {conversion_time:.2f}s", "white")
        cprint(f"   Speed: {page_count/conversion_time:.2f} pages/sec", "white")

    except Exception as e:
        cprint(f"❌ Conversion failed: {e}", "red")
        return

    # Test 2: Paragraph Chunking
    cprint("\n[TEST 2] Paragraph Chunking", "cyan", attrs=["bold"])
    start_time = time.time()

    try:
        para_chunks = document_chunker.chunk_document(
            docling_document=docling_document,
            mode=ChunkingMode.PARAGRAPH
        )

        para_time = time.time() - start_time
        para_avg_len = sum(len(c.text) for c in para_chunks) / len(para_chunks)

        cprint(f"✅ Paragraph chunking successful", "green")
        cprint(f"   Total chunks: {len(para_chunks)}", "white")
        cprint(f"   Avg chunk length: {para_avg_len:.0f} chars", "white")
        cprint(f"   Chunks per page: {len(para_chunks)/page_count:.1f}", "white")
        cprint(f"   Time: {para_time:.2f}s", "white")

    except Exception as e:
        cprint(f"❌ Paragraph chunking failed: {e}", "red")
        para_chunks = []
        para_time = 0

    # Test 3: Sentence Chunking
    cprint("\n[TEST 3] Sentence Chunking", "cyan", attrs=["bold"])
    start_time = time.time()

    try:
        sent_chunks = document_chunker.chunk_document(
            docling_document=docling_document,
            mode=ChunkingMode.SENTENCE
        )

        sent_time = time.time() - start_time
        sent_avg_len = sum(len(c.text) for c in sent_chunks) / len(sent_chunks)

        cprint(f"✅ Sentence chunking successful", "green")
        cprint(f"   Total chunks: {len(sent_chunks)}", "white")
        cprint(f"   Avg chunk length: {sent_avg_len:.0f} chars", "white")
        cprint(f"   Chunks per page: {len(sent_chunks)/page_count:.1f}", "white")
        cprint(f"   Time: {sent_time:.2f}s", "white")

    except Exception as e:
        cprint(f"❌ Sentence chunking failed: {e}", "red")
        sent_chunks = []
        sent_time = 0

    # Summary
    total_time = conversion_time + para_time + sent_time

    cprint(f"\n{'='*80}", "cyan")
    cprint(f"SUMMARY: {file_path.name}", "cyan", attrs=["bold"])
    cprint(f"{'='*80}", "cyan")
    cprint(f"Total processing time: {total_time:.2f}s", "yellow", attrs=["bold"])
    cprint(f"  - Conversion: {conversion_time:.2f}s ({conversion_time/total_time*100:.1f}%)", "white")
    cprint(f"  - Paragraph chunking: {para_time:.2f}s ({para_time/total_time*100:.1f}%)", "white")
    cprint(f"  - Sentence chunking: {sent_time:.2f}s ({sent_time/total_time*100:.1f}%)", "white")

    # Validation: paragraph chunks should be longer than sentence chunks
    if para_chunks and sent_chunks:
        para_avg = sum(len(c.text) for c in para_chunks) / len(para_chunks)
        sent_avg = sum(len(c.text) for c in sent_chunks) / len(sent_chunks)

        cprint(f"\n[VALIDATION]", "cyan", attrs=["bold"])
        if para_avg > sent_avg:
            cprint(f"✅ PASS: Paragraph chunks ({para_avg:.0f} chars) > Sentence chunks ({sent_avg:.0f} chars)", "green")
        else:
            cprint(f"❌ FAIL: Paragraph chunks ({para_avg:.0f} chars) ≤ Sentence chunks ({sent_avg:.0f} chars)", "red")

        if len(para_chunks) < len(sent_chunks):
            cprint(f"✅ PASS: Fewer paragraph chunks ({len(para_chunks)}) than sentence chunks ({len(sent_chunks)})", "green")
        else:
            cprint(f"❌ FAIL: More paragraph chunks ({len(para_chunks)}) than sentence chunks ({len(sent_chunks)})", "red")


def main():
    """Run performance tests"""
    cprint("\n" + "="*80, "cyan", attrs=["bold"])
    cprint("DOCUMENT PROCESSING PERFORMANCE TEST", "cyan", attrs=["bold"])
    cprint("Running inside Docker backend container", "cyan", attrs=["bold"])
    cprint("="*80 + "\n", "cyan", attrs=["bold"])

    # Test files
    test_files = [
        ("/tmp/test_files/AgentQuality-Abridged.pdf", "PDF"),
        ("/tmp/test_files/AgentQuality-ShortSummary.docx", "DOCX"),
    ]

    overall_start = time.time()

    for file_path_str, file_type in test_files:
        file_path = Path(file_path_str)

        if not file_path.exists():
            cprint(f"❌ File not found: {file_path}", "red")
            continue

        test_document_processing(file_path, file_type)

    overall_time = time.time() - overall_start

    cprint(f"\n{'='*80}", "cyan", attrs=["bold"])
    cprint(f"ALL TESTS COMPLETED", "cyan", attrs=["bold"])
    cprint(f"Total time: {overall_time:.2f}s", "yellow", attrs=["bold"])
    cprint(f"{'='*80}\n", "cyan", attrs=["bold"])


if __name__ == "__main__":
    main()
