"""
Document processing module using Docling for PDF/DOCX conversion
MINIMAL MVP VERSION - simplified configuration
"""

from pathlib import Path
from typing import Dict, Any, Optional
import subprocess
import sys
import shutil
from termcolor import cprint
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

from app.processing.cache import document_cache


# Maximum file size: 10 MB
MAX_FILE_SIZE = 100 * 1024 * 1024

# Supported file extensions
SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


class DocumentProcessor:
    """Handles document conversion using Docling with minimal configuration"""

    def __init__(self):
        """Initialize the document processor with minimal configuration"""
        cprint(
            "[PROCESSOR] Initializing Docling DocumentConverter (minimal configuration)...",
            "cyan",
        )

        # Detect LibreOffice command at initialization
        self.libreoffice_cmd = self._find_libreoffice()
        if self.libreoffice_cmd:
            cprint(f"[PROCESSOR] LibreOffice found at: {self.libreoffice_cmd}", "green")
        else:
            cprint(
                "[PROCESSOR] ⚠️  LibreOffice not found - DOCX conversion will fail",
                "yellow",
            )

        # Minimal pipeline configuration
        # Disable OCR (most expensive operation)
        # Disable table structure detection (removes TableFormer model dependency)
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_table_structure = False  # CHANGED: Disabled to remove model dependency
        pipeline_options.do_ocr = False

        # Initialize single converter with minimal config
        # Uses default PyPdfiumDocumentBackend (no backend parameter needed)
        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options,
                    # No backend parameter - uses default PyPdfiumDocumentBackend
                )
            }
        )

        cprint("[PROCESSOR] DocumentConverter initialized with minimal configuration:", "green")
        cprint("  ✓ Default PyPdfiumDocumentBackend (standard PDF parsing)", "green")
        cprint("  ✓ OCR disabled (already digital PDFs)", "green")
        cprint("  ✓ Table structure detection disabled (no model downloads)", "green")

    def _find_libreoffice(self) -> Optional[str]:
        """
        Find LibreOffice executable across different platforms

        Returns:
            Path to LibreOffice executable, or None if not found
        """
        # Try common paths based on platform
        possible_commands = []

        if sys.platform == "darwin":  # macOS
            possible_commands = [
                "/Applications/LibreOffice.app/Contents/MacOS/soffice",
                "/usr/local/bin/soffice",
                "soffice",
                "libreoffice",
            ]
        elif sys.platform == "win32":  # Windows
            possible_commands = [
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
                "soffice",
                "libreoffice",
            ]
        else:  # Linux and others
            possible_commands = [
                "libreoffice",
                "soffice",
                "/usr/bin/libreoffice",
                "/usr/bin/soffice",
            ]

        # Try each command
        for cmd in possible_commands:
            # Check if it's a full path
            if Path(cmd).exists():
                return cmd

            # Check if it's in PATH
            if shutil.which(cmd):
                return cmd

        return None

    def _convert_docx_to_pdf(self, docx_path: Path) -> Path:
        """
        Convert DOCX to PDF using LibreOffice

        Args:
            docx_path: Path to DOCX file

        Returns:
            Path to generated PDF file

        Raises:
            Exception: If conversion fails
        """
        cprint(f"[PROCESSOR] Converting DOCX to PDF using LibreOffice...", "cyan")

        # Check if LibreOffice is available
        if not self.libreoffice_cmd:
            raise Exception(
                "LibreOffice not found. Please install LibreOffice:\n"
                "  macOS: brew install --cask libreoffice\n"
                "  Ubuntu: sudo apt-get install libreoffice\n"
                "  Windows: Download from https://www.libreoffice.org/download/"
            )

        # Get output directory (same as input file directory)
        output_dir = docx_path.parent

        # Run LibreOffice conversion
        # --headless: run without GUI
        # --convert-to pdf: convert to PDF format
        # --outdir: output directory
        try:
            result = subprocess.run(
                [
                    self.libreoffice_cmd,
                    "--headless",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    str(output_dir),
                    str(docx_path),
                ],
                capture_output=True,
                text=True,
                timeout=60,
                check=True,
            )

            # LibreOffice creates PDF with same name as DOCX but .pdf extension
            pdf_path = output_dir / f"{docx_path.stem}.pdf"

            if not pdf_path.exists():
                raise Exception(
                    f"LibreOffice conversion completed but PDF not found: {pdf_path}"
                )

            cprint(
                f"[PROCESSOR] DOCX→PDF conversion successful: {pdf_path.name}", "green"
            )
            return pdf_path

        except subprocess.TimeoutExpired:
            cprint("[PROCESSOR] LibreOffice conversion timed out", "red")
            raise Exception("DOCX to PDF conversion timed out after 60 seconds")
        except subprocess.CalledProcessError as e:
            cprint(f"[PROCESSOR] LibreOffice conversion failed: {e.stderr}", "red")
            raise Exception(f"DOCX to PDF conversion failed: {e.stderr}")
        except Exception as e:
            cprint(f"[PROCESSOR] Unexpected error during DOCX conversion: {e}", "red")
            raise

    def validate_file(self, file_content: bytes, filename: str) -> None:
        """
        Validate file size and format

        Args:
            file_content: Raw file content
            filename: Original filename

        Raises:
            ValueError: If file is invalid
        """
        # Check file size
        file_size = len(file_content)
        if file_size > MAX_FILE_SIZE:
            raise ValueError(
                f"File size ({file_size / 1024 / 1024:.2f} MB) exceeds "
                f"maximum allowed size ({MAX_FILE_SIZE / 1024 / 1024:.2f} MB)"
            )

        # Check file extension
        ext = Path(filename).suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file format: {ext}. "
                f"Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}"
            )

        cprint(
            f"[PROCESSOR] File validation passed: {filename} ({file_size / 1024:.2f} KB)",
            "green",
        )

    def convert_document(
        self, file_content: bytes, filename: str, use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Convert document to Docling format

        Args:
            file_content: Raw file content
            filename: Original filename
            use_cache: Whether to use cached results

        Returns:
            Dictionary containing:
                - docling_document: The converted Docling document
                - filename: Original filename
                - page_count: Number of pages
                - file_size: File size in bytes

        Raises:
            Exception: If conversion fails
        """
        cprint(f"[PROCESSOR] Converting document: {filename}", "cyan")

        # Validate file
        self.validate_file(file_content, filename)

        # Check cache first
        if use_cache:
            cached_data = document_cache.get(file_content)
            if cached_data is not None:
                cprint("[PROCESSOR] Using cached document", "green")
                return cached_data

        # Create temporary file for conversion
        import tempfile

        file_ext = Path(filename).suffix.lower()

        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            tmp_path = Path(tmp_file.name)
            tmp_file.write(file_content)

        # Track if we need to clean up a converted PDF
        pdf_path_to_cleanup = None

        try:
            # For DOCX files, convert to PDF first using LibreOffice
            # This gives us accurate page numbers
            # IMPORTANT: DOCX files don't need OCR (they're digital text)
            is_docx = file_ext == ".docx"

            if is_docx:
                cprint(
                    f"[PROCESSOR] DOCX file detected, converting to PDF first for accurate pagination...",
                    "yellow",
                )
                pdf_path = self._convert_docx_to_pdf(tmp_path)
                pdf_path_to_cleanup = pdf_path
                conversion_path = pdf_path
                cprint(
                    f"[PROCESSOR] Will process converted PDF (OCR disabled - digital text): {pdf_path.name}",
                    "cyan",
                )
            else:
                conversion_path = tmp_path
                cprint(
                    f"[PROCESSOR] Native PDF detected, processing with OCR disabled",
                    "cyan",
                )

            # Convert document using Docling with minimal configuration
            cprint(
                f"[PROCESSOR] Running Docling conversion on {conversion_path.name}...",
                "cyan",
            )

            import time

            start_time = time.time()

            result = self.converter.convert(conversion_path)

            elapsed_time = time.time() - start_time

            # Extract the document
            docling_document = result.document

            # Get page count
            page_count = (
                len(docling_document.pages) if hasattr(docling_document, "pages") else 0
            )

            avg_pages_per_sec = page_count / elapsed_time if elapsed_time > 0 else 0
            cprint(
                f"[PROCESSOR] Conversion successful: {page_count} pages in {elapsed_time:.2f}s "
                f"({avg_pages_per_sec:.2f} pages/sec)",
                "green",
            )

            # Prepare data for caching
            data = {
                "docling_document": docling_document,
                "filename": filename,
                "page_count": page_count,
                "file_size": len(file_content),
            }

            # Cache the result
            if use_cache:
                document_cache.set(file_content, data)

            return data

        except Exception as e:
            cprint(f"[PROCESSOR] Conversion failed: {e}", "red")
            raise Exception(f"Document conversion failed: {str(e)}")

        finally:
            # Clean up temporary files
            if tmp_path.exists():
                tmp_path.unlink()
                cprint(f"[PROCESSOR] Cleaned up temporary file", "cyan")

            # Clean up converted PDF if it was created
            if pdf_path_to_cleanup and pdf_path_to_cleanup.exists():
                pdf_path_to_cleanup.unlink()
                cprint(f"[PROCESSOR] Cleaned up converted PDF file", "cyan")


# Global processor instance
document_processor = DocumentProcessor()
