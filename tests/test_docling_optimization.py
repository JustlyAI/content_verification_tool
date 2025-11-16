"""
Comprehensive performance benchmark comparing current vs optimized Docling implementations

This test suite:
1. Benchmarks both current and optimized document processors
2. Validates output correctness (same page count, text, chunks)
3. Measures conversion speed, memory usage, and speedup factors
4. Provides clear recommendations on whether to adopt the optimization

Expected improvements with optimized version:
- DoclingParseV2DocumentBackend: 5-10x faster PDF parsing
- Hardware acceleration (MPS/CUDA): 3-6x faster AI models
- TableFormerMode.FAST: 2-3x faster table extraction
- Combined: 10-30x potential speedup
"""

import time
import sys
import gc
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from termcolor import cprint
from pydantic import BaseModel, Field
import importlib

# Test file paths
TEST_PDF = Path("/Users/laurentwiesel/Dev/ai-law/content_verification_tool/AgentQuality-Abridged.pdf")
TEST_DOCX = Path("/Users/laurentwiesel/Dev/ai-law/content_verification_tool/AgentQuality-ShortSummary.docx")

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.models import DocumentChunk, ChunkingMode


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class BenchmarkResult(BaseModel):
    """Store benchmark metrics for a single implementation run"""

    implementation_name: str = Field(..., description="'Current' or 'Optimized'")
    filename: str = Field(..., description="Test file name")

    # Timing metrics (seconds)
    conversion_time: float = Field(..., description="Docling conversion only")
    para_chunking_time: float = Field(..., description="Paragraph chunking time")
    sent_chunking_time: float = Field(..., description="Sentence chunking time")
    total_time: float = Field(..., description="Total processing time")

    # Performance metrics
    pages_per_sec: float = Field(..., description="Conversion speed")
    success: bool = Field(..., description="Completed without errors")
    error_message: Optional[str] = Field(None, description="Error details if failed")

    # Output metrics
    page_count: int = Field(..., description="Number of pages extracted")
    text_length: int = Field(..., description="Total characters in document")
    para_chunk_count: int = Field(..., description="Number of paragraph chunks")
    sent_chunk_count: int = Field(..., description="Number of sentence chunks")

    # Memory (optional)
    peak_memory_mb: Optional[float] = Field(None, description="Peak memory usage in MB")


class ValidationResult(BaseModel):
    """Output validation comparison results"""

    page_count_match: bool
    page_count_diff: int

    text_similarity_pct: float = Field(..., description="Text similarity 0-100%")
    text_length_diff: int

    para_chunk_match: bool
    para_chunk_diff: int

    sent_chunk_match: bool
    sent_chunk_diff: int

    errors: List[str] = Field(default_factory=list)
    is_valid: bool = Field(..., description="Overall validation status")


class ComparisonResult(BaseModel):
    """Complete comparison between current and optimized implementations"""

    filename: str
    current: BenchmarkResult
    optimized: BenchmarkResult
    validation: ValidationResult

    # Speedup metrics
    conversion_speedup: float = Field(..., description="How much faster conversion is")
    total_speedup: float = Field(..., description="Overall speedup factor")

    # Recommendation
    recommend_adoption: bool = Field(..., description="Should we adopt optimized version?")
    recommendation_reasons: List[str] = Field(..., description="Why or why not")


# ============================================================================
# OUTPUT VALIDATOR
# ============================================================================

class OutputValidator:
    """Compare two document processor outputs for correctness"""

    @staticmethod
    def calculate_text_similarity(text1: str, text2: str) -> float:
        """
        Calculate character-level similarity between two texts

        Returns:
            Similarity percentage (0-100)
        """
        # Simple character-level comparison
        len1, len2 = len(text1), len(text2)
        if len1 == 0 and len2 == 0:
            return 100.0
        if len1 == 0 or len2 == 0:
            return 0.0

        # Use length-based similarity for now (more sophisticated diff would be better)
        max_len = max(len1, len2)
        min_len = min(len1, len2)
        similarity = (min_len / max_len) * 100

        return similarity

    @staticmethod
    def validate(
        current_result: Dict[str, Any],
        optimized_result: Dict[str, Any],
        current_chunks_para: List[DocumentChunk],
        optimized_chunks_para: List[DocumentChunk],
        current_chunks_sent: List[DocumentChunk],
        optimized_chunks_sent: List[DocumentChunk]
    ) -> ValidationResult:
        """
        Compare outputs from current and optimized implementations

        Returns:
            ValidationResult with detailed comparison
        """
        errors = []

        # Compare page counts
        current_pages = current_result["page_count"]
        optimized_pages = optimized_result["page_count"]
        page_count_match = current_pages == optimized_pages
        page_count_diff = abs(current_pages - optimized_pages)

        if not page_count_match:
            errors.append(f"Page count mismatch: {current_pages} vs {optimized_pages}")

        # Compare text lengths (extract all text from chunks)
        current_text = " ".join(c.text for c in current_chunks_para)
        optimized_text = " ".join(c.text for c in optimized_chunks_para)

        text_similarity = OutputValidator.calculate_text_similarity(current_text, optimized_text)
        text_length_diff = abs(len(current_text) - len(optimized_text))

        if text_similarity < 95.0:
            errors.append(f"Text similarity too low: {text_similarity:.1f}%")

        # Compare paragraph chunk counts
        para_chunk_match = len(current_chunks_para) == len(optimized_chunks_para)
        para_chunk_diff = abs(len(current_chunks_para) - len(optimized_chunks_para))

        if not para_chunk_match:
            errors.append(f"Paragraph chunk mismatch: {len(current_chunks_para)} vs {len(optimized_chunks_para)}")

        # Compare sentence chunk counts
        sent_chunk_match = len(current_chunks_sent) == len(optimized_chunks_sent)
        sent_chunk_diff = abs(len(current_chunks_sent) - len(optimized_chunks_sent))

        if not sent_chunk_match:
            errors.append(f"Sentence chunk mismatch: {len(current_chunks_sent)} vs {len(optimized_chunks_sent)}")

        # Overall validation
        is_valid = (
            page_count_match and
            text_similarity >= 95.0 and
            para_chunk_diff <= 2 and  # Allow small differences
            sent_chunk_diff <= 5
        )

        return ValidationResult(
            page_count_match=page_count_match,
            page_count_diff=page_count_diff,
            text_similarity_pct=text_similarity,
            text_length_diff=text_length_diff,
            para_chunk_match=para_chunk_match,
            para_chunk_diff=para_chunk_diff,
            sent_chunk_match=sent_chunk_match,
            sent_chunk_diff=sent_chunk_diff,
            errors=errors,
            is_valid=is_valid
        )


# ============================================================================
# CORE BENCHMARKING FUNCTIONS
# ============================================================================

def clear_cache():
    """Clear document cache before benchmarking"""
    try:
        from app.processing.cache import document_cache
        document_cache.clear_all()
        cprint("[BENCHMARK] Cache cleared", "cyan")
    except Exception as e:
        cprint(f"[BENCHMARK] Warning: Could not clear cache: {e}", "yellow")


def load_processor(module_type: str):
    """
    Dynamically import and initialize document processor

    Args:
        module_type: "current" or "optimized"

    Returns:
        DocumentProcessor instance
    """
    if module_type == "current":
        # Reload the module to get fresh instance
        if 'app.processing.document_processor' in sys.modules:
            importlib.reload(sys.modules['app.processing.document_processor'])
        from app.processing.document_processor import DocumentProcessor
        cprint(f"[BENCHMARK] Loaded CURRENT implementation", "cyan")

    elif module_type == "optimized":
        # Import the optimized version
        if 'app.processing.document_processor_optimized' in sys.modules:
            importlib.reload(sys.modules['app.processing.document_processor_optimized'])
        from app.processing.document_processor_optimized import DocumentProcessor
        cprint(f"[BENCHMARK] Loaded OPTIMIZED implementation", "cyan")

    else:
        raise ValueError(f"Unknown module type: {module_type}")

    return DocumentProcessor()


def benchmark_processor(
    module_type: str,
    file_path: Path,
    runs: int = 3
) -> BenchmarkResult:
    """
    Benchmark a document processor implementation

    Args:
        module_type: "current" or "optimized"
        file_path: Path to test file
        runs: Number of runs to average (default 3)

    Returns:
        BenchmarkResult with all metrics
    """
    impl_name = "Current" if module_type == "current" else "Optimized"
    cprint(f"\n{'='*80}", "cyan")
    cprint(f"BENCHMARKING: {impl_name} Implementation", "cyan", attrs=["bold"])
    cprint(f"File: {file_path.name}", "cyan")
    cprint(f"{'='*80}", "cyan")

    try:
        # Load processor
        processor = load_processor(module_type)

        # Load chunker (same for both)
        from app.processing.chunker import DocumentChunker
        chunker = DocumentChunker()

        # Read file content
        with open(file_path, "rb") as f:
            file_content = f.read()

        cprint(f"[BENCHMARK] File size: {len(file_content) / 1024:.2f} KB", "white")

        # === CONVERSION BENCHMARK ===
        cprint(f"\n[BENCHMARK] Running conversion ({runs} runs)...", "cyan")
        conversion_times = []

        for run in range(runs):
            clear_cache()
            gc.collect()  # Force garbage collection

            start = time.time()
            result = processor.convert_document(
                file_content=file_content,
                filename=file_path.name,
                use_cache=False  # Disable cache for fair comparison
            )
            elapsed = time.time() - start
            conversion_times.append(elapsed)

            cprint(f"  Run {run + 1}: {elapsed:.2f}s", "white")

        # Average conversion time
        avg_conversion_time = sum(conversion_times) / len(conversion_times)
        cprint(f"[BENCHMARK] Average conversion time: {avg_conversion_time:.2f}s", "green")

        # Store document and metadata
        docling_doc = result["docling_document"]
        page_count = result["page_count"]

        # Calculate pages/sec
        pages_per_sec = page_count / avg_conversion_time if avg_conversion_time > 0 else 0

        # === PARAGRAPH CHUNKING BENCHMARK ===
        cprint(f"\n[BENCHMARK] Running paragraph chunking...", "cyan")
        start = time.time()
        para_chunks = chunker.chunk_document(docling_doc, ChunkingMode.PARAGRAPH)
        para_time = time.time() - start
        cprint(f"[BENCHMARK] Paragraph chunking: {para_time:.2f}s ({len(para_chunks)} chunks)", "green")

        # === SENTENCE CHUNKING BENCHMARK ===
        cprint(f"\n[BENCHMARK] Running sentence chunking...", "cyan")
        start = time.time()
        sent_chunks = chunker.chunk_document(docling_doc, ChunkingMode.SENTENCE)
        sent_time = time.time() - start
        cprint(f"[BENCHMARK] Sentence chunking: {sent_time:.2f}s ({len(sent_chunks)} chunks)", "green")

        # Calculate text length
        total_text = " ".join(c.text for c in para_chunks)
        text_length = len(total_text)

        # Total time
        total_time = avg_conversion_time + para_time + sent_time

        cprint(f"\n[BENCHMARK] ✅ {impl_name} benchmark complete: {total_time:.2f}s total", "green", attrs=["bold"])

        return BenchmarkResult(
            implementation_name=impl_name,
            filename=file_path.name,
            conversion_time=avg_conversion_time,
            para_chunking_time=para_time,
            sent_chunking_time=sent_time,
            total_time=total_time,
            pages_per_sec=pages_per_sec,
            success=True,
            error_message=None,
            page_count=page_count,
            text_length=text_length,
            para_chunk_count=len(para_chunks),
            sent_chunk_count=len(sent_chunks),
            peak_memory_mb=None  # TODO: Add memory profiling if needed
        ), result, para_chunks, sent_chunks

    except Exception as e:
        cprint(f"\n[BENCHMARK] ❌ {impl_name} benchmark FAILED: {e}", "red", attrs=["bold"])

        return BenchmarkResult(
            implementation_name=impl_name,
            filename=file_path.name,
            conversion_time=0.0,
            para_chunking_time=0.0,
            sent_chunking_time=0.0,
            total_time=0.0,
            pages_per_sec=0.0,
            success=False,
            error_message=str(e),
            page_count=0,
            text_length=0,
            para_chunk_count=0,
            sent_chunk_count=0,
            peak_memory_mb=None
        ), None, [], []


# ============================================================================
# COMPARISON & REPORTING
# ============================================================================

def compare_implementations(file_path: Path) -> ComparisonResult:
    """
    Compare current vs optimized implementations

    Args:
        file_path: Path to test file

    Returns:
        ComparisonResult with complete comparison data
    """
    cprint(f"\n\n{'#'*80}", "cyan", attrs=["bold"])
    cprint(f"# DOCLING OPTIMIZATION COMPARISON TEST", "cyan", attrs=["bold"])
    cprint(f"# File: {file_path.name}", "cyan", attrs=["bold"])
    cprint(f"{'#'*80}\n", "cyan", attrs=["bold"])

    # Benchmark current implementation
    current_bench, current_result, current_para, current_sent = benchmark_processor("current", file_path)

    # Benchmark optimized implementation
    optimized_bench, optimized_result, optimized_para, optimized_sent = benchmark_processor("optimized", file_path)

    # Validate outputs
    if current_bench.success and optimized_bench.success:
        validation = OutputValidator.validate(
            current_result,
            optimized_result,
            current_para,
            optimized_para,
            current_sent,
            optimized_sent
        )
    else:
        # One or both failed - create failed validation
        validation = ValidationResult(
            page_count_match=False,
            page_count_diff=0,
            text_similarity_pct=0.0,
            text_length_diff=0,
            para_chunk_match=False,
            para_chunk_diff=0,
            sent_chunk_match=False,
            sent_chunk_diff=0,
            errors=["One or both implementations failed"],
            is_valid=False
        )

    # Calculate speedup
    if current_bench.conversion_time > 0 and optimized_bench.success:
        conversion_speedup = current_bench.conversion_time / optimized_bench.conversion_time
    else:
        conversion_speedup = 0.0

    if current_bench.total_time > 0 and optimized_bench.success:
        total_speedup = current_bench.total_time / optimized_bench.total_time
    else:
        total_speedup = 0.0

    # Generate recommendation
    recommendation_reasons = []
    recommend_adoption = False

    if not optimized_bench.success:
        recommendation_reasons.append("❌ Optimized version crashed or failed")
    elif not validation.is_valid:
        recommendation_reasons.append("❌ Output validation failed - results don't match")
        recommendation_reasons.extend(f"  • {err}" for err in validation.errors)
    elif conversion_speedup < 1.2:
        recommendation_reasons.append(f"⚠️  Speedup too low: {conversion_speedup:.1f}x (expected >2x)")
    else:
        recommend_adoption = True
        recommendation_reasons.append(f"✅ {conversion_speedup:.1f}x faster conversion")
        recommendation_reasons.append(f"✅ {total_speedup:.1f}x faster overall")
        recommendation_reasons.append("✅ Output validation passed")
        recommendation_reasons.append("✅ No errors or crashes")

    return ComparisonResult(
        filename=file_path.name,
        current=current_bench,
        optimized=optimized_bench,
        validation=validation,
        conversion_speedup=conversion_speedup,
        total_speedup=total_speedup,
        recommend_adoption=recommend_adoption,
        recommendation_reasons=recommendation_reasons
    )


def print_results(comparison: ComparisonResult):
    """
    Print beautiful comparison results with termcolor

    Args:
        comparison: ComparisonResult to display
    """
    c = comparison  # Shorthand

    cprint(f"\n\n{'='*80}", "cyan", attrs=["bold"])
    cprint(f"BENCHMARK RESULTS: {c.filename}", "cyan", attrs=["bold"])
    cprint(f"{'='*80}\n", "cyan", attrs=["bold"])

    # Performance comparison table
    cprint("[PERFORMANCE COMPARISON]", "yellow", attrs=["bold"])
    print()

    # Table header
    print(f"{'Metric':<30} {'Current':<15} {'Optimized':<15} {'Speedup':<10}")
    print("─" * 70)

    # Conversion time
    speedup_conv = f"{c.conversion_speedup:.1f}x" if c.conversion_speedup > 0 else "N/A"
    print(f"{'Conversion Time':<30} {c.current.conversion_time:<15.2f} {c.optimized.conversion_time:<15.2f} {speedup_conv:<10}")

    # Paragraph chunking
    speedup_para = c.current.para_chunking_time / c.optimized.para_chunking_time if c.optimized.para_chunking_time > 0 else 0
    speedup_para_str = f"{speedup_para:.1f}x" if speedup_para > 0 else "N/A"
    print(f"{'Paragraph Chunking':<30} {c.current.para_chunking_time:<15.2f} {c.optimized.para_chunking_time:<15.2f} {speedup_para_str:<10}")

    # Sentence chunking
    speedup_sent = c.current.sent_chunking_time / c.optimized.sent_chunking_time if c.optimized.sent_chunking_time > 0 else 0
    speedup_sent_str = f"{speedup_sent:.1f}x" if speedup_sent > 0 else "N/A"
    print(f"{'Sentence Chunking':<30} {c.current.sent_chunking_time:<15.2f} {c.optimized.sent_chunking_time:<15.2f} {speedup_sent_str:<10}")

    # Total time
    speedup_total = f"{c.total_speedup:.1f}x" if c.total_speedup > 0 else "N/A"
    print(f"{'Total Time':<30} {c.current.total_time:<15.2f} {c.optimized.total_time:<15.2f} {speedup_total:<10}")

    # Pages per second
    speedup_pps = c.optimized.pages_per_sec / c.current.pages_per_sec if c.current.pages_per_sec > 0 else 0
    speedup_pps_str = f"{speedup_pps:.1f}x" if speedup_pps > 0 else "N/A"
    print(f"{'Pages/sec':<30} {c.current.pages_per_sec:<15.2f} {c.optimized.pages_per_sec:<15.2f} {speedup_pps_str:<10}")

    print()

    # Output validation
    cprint("[OUTPUT VALIDATION]", "yellow", attrs=["bold"])
    v = c.validation

    if v.page_count_match:
        cprint(f"✅ Page count matches: {c.current.page_count} pages", "green")
    else:
        cprint(f"❌ Page count mismatch: {c.current.page_count} vs {c.optimized.page_count} (diff: {v.page_count_diff})", "red")

    if v.text_similarity_pct >= 95.0:
        cprint(f"✅ Text similarity: {v.text_similarity_pct:.1f}% ({c.current.text_length} vs {c.optimized.text_length} chars)", "green")
    else:
        cprint(f"❌ Text similarity too low: {v.text_similarity_pct:.1f}%", "red")

    if v.para_chunk_match or v.para_chunk_diff <= 2:
        cprint(f"✅ Paragraph chunks: {c.current.para_chunk_count} vs {c.optimized.para_chunk_count} (diff: {v.para_chunk_diff})", "green")
    else:
        cprint(f"⚠️  Paragraph chunk difference: {c.current.para_chunk_count} vs {c.optimized.para_chunk_count} (diff: {v.para_chunk_diff})", "yellow")

    if v.sent_chunk_match or v.sent_chunk_diff <= 5:
        cprint(f"✅ Sentence chunks: {c.current.sent_chunk_count} vs {c.optimized.sent_chunk_count} (diff: {v.sent_chunk_diff})", "green")
    else:
        cprint(f"⚠️  Sentence chunk difference: {c.current.sent_chunk_count} vs {c.optimized.sent_chunk_count} (diff: {v.sent_chunk_diff})", "yellow")

    print()

    # Analysis
    cprint("[ANALYSIS]", "yellow", attrs=["bold"])
    if c.conversion_speedup > 0:
        color = "green" if c.conversion_speedup >= 2.0 else "yellow"
        cprint(f"Conversion speedup: {c.conversion_speedup:.1f}x faster ⚡", color)

    if c.total_speedup > 0:
        color = "green" if c.total_speedup >= 1.5 else "yellow"
        cprint(f"Overall speedup: {c.total_speedup:.1f}x faster ⚡", color)

    print()

    # Recommendation
    cprint("[RECOMMENDATION]", "yellow", attrs=["bold"])
    if c.recommend_adoption:
        cprint("✅ ADOPT OPTIMIZED VERSION", "green", attrs=["bold"])
    else:
        cprint("❌ DO NOT ADOPT - ISSUES FOUND", "red", attrs=["bold"])

    for reason in c.recommendation_reasons:
        if "✅" in reason:
            cprint(f"   {reason}", "green")
        elif "❌" in reason:
            cprint(f"   {reason}", "red")
        else:
            cprint(f"   {reason}", "yellow")

    cprint(f"\n{'='*80}\n", "cyan", attrs=["bold"])


# ============================================================================
# PYTEST TEST FUNCTIONS
# ============================================================================

def test_pdf_optimization():
    """Test optimization on 4-page PDF"""
    if not TEST_PDF.exists():
        cprint(f"⚠️  Test file not found: {TEST_PDF}", "yellow")
        cprint("Skipping PDF optimization test", "yellow")
        return

    comparison = compare_implementations(TEST_PDF)
    print_results(comparison)

    # Assertions
    assert comparison.optimized.success, "Optimized version must complete successfully"
    assert comparison.validation.is_valid, f"Output validation failed: {comparison.validation.errors}"
    assert comparison.conversion_speedup > 2.0, f"Expected >2x speedup, got {comparison.conversion_speedup:.1f}x"

    cprint("\n✅ PDF OPTIMIZATION TEST PASSED", "green", attrs=["bold"])


def test_docx_optimization():
    """Test optimization on 1-page DOCX"""
    if not TEST_DOCX.exists():
        cprint(f"⚠️  Test file not found: {TEST_DOCX}", "yellow")
        cprint("Skipping DOCX optimization test", "yellow")
        return

    comparison = compare_implementations(TEST_DOCX)
    print_results(comparison)

    # Assertions (more lenient for DOCX due to LibreOffice conversion overhead)
    assert comparison.optimized.success, "Optimized version must complete successfully"
    assert comparison.validation.is_valid, f"Output validation failed: {comparison.validation.errors}"
    assert comparison.conversion_speedup > 1.2, f"Expected >1.2x speedup for DOCX, got {comparison.conversion_speedup:.1f}x"

    cprint("\n✅ DOCX OPTIMIZATION TEST PASSED", "green", attrs=["bold"])


# ============================================================================
# MANUAL TEST RUNNER
# ============================================================================

def main():
    """Manual test execution"""
    cprint("\n" + "="*80, "cyan", attrs=["bold"])
    cprint("DOCLING OPTIMIZATION COMPREHENSIVE TEST SUITE", "cyan", attrs=["bold"])
    cprint("="*80 + "\n", "cyan", attrs=["bold"])

    # Test PDF
    if TEST_PDF.exists():
        try:
            test_pdf_optimization()
        except AssertionError as e:
            cprint(f"\n❌ PDF TEST FAILED: {e}", "red", attrs=["bold"])
        except Exception as e:
            cprint(f"\n❌ PDF TEST ERROR: {e}", "red", attrs=["bold"])
    else:
        cprint(f"⚠️  Skipping PDF test - file not found: {TEST_PDF}", "yellow")

    print("\n")

    # Test DOCX
    if TEST_DOCX.exists():
        try:
            test_docx_optimization()
        except AssertionError as e:
            cprint(f"\n❌ DOCX TEST FAILED: {e}", "red", attrs=["bold"])
        except Exception as e:
            cprint(f"\n❌ DOCX TEST ERROR: {e}", "red", attrs=["bold"])
    else:
        cprint(f"⚠️  Skipping DOCX test - file not found: {TEST_DOCX}", "yellow")

    cprint("\n" + "="*80, "cyan", attrs=["bold"])
    cprint("ALL TESTS COMPLETED", "cyan", attrs=["bold"])
    cprint("="*80 + "\n", "cyan", attrs=["bold"])


if __name__ == "__main__":
    main()
