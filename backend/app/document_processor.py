"""
Document processing module using Docling for PDF/DOCX conversion
"""

from pathlib import Path
from typing import Dict, Any, Optional
import subprocess
from termcolor import cprint
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

from app.cache import document_cache


# Maximum file size: 10 MB
MAX_FILE_SIZE = 10 * 1024 * 1024

# Supported file extensions
SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


class DocumentProcessor:
    """Handles document conversion using Docling"""

    def __init__(self):
        """Initialize the document processor"""
        cprint("[PROCESSOR] Initializing Docling DocumentConverter...", "cyan")

        # Configure pipeline options for PDF processing with OCR
        # Enable table parsing and footnote extraction
        pipeline_options_ocr = PdfPipelineOptions()
        pipeline_options_ocr.do_table_structure = True
        pipeline_options_ocr.do_ocr = True

        # Configure pipeline options for PDF processing WITHOUT OCR
        # (for DOCX-converted PDFs which are already digital)
        pipeline_options_no_ocr = PdfPipelineOptions()
        pipeline_options_no_ocr.do_table_structure = True
        pipeline_options_no_ocr.do_ocr = False

        # Initialize converter with OCR enabled (for native PDFs)
        self.converter_with_ocr = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options_ocr)
            }
        )

        # Initialize converter without OCR (for DOCX-converted PDFs)
        self.converter_no_ocr = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options_no_ocr
                )
            }
        )

        cprint("[PROCESSOR] DocumentConverter initialized successfully", "green")

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

        # Get output directory (same as input file directory)
        output_dir = docx_path.parent

        # Run LibreOffice conversion
        # --headless: run without GUI
        # --convert-to pdf: convert to PDF format
        # --outdir: output directory
        try:
            result = subprocess.run(
                [
                    "libreoffice",
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
                    f"[PROCESSOR] Native PDF detected, will use OCR for accurate text extraction",
                    "cyan",
                )

            # Convert document using Docling
            # Use OCR for native PDFs (may be scanned), skip OCR for DOCX (already digital)
            converter = self.converter_no_ocr if is_docx else self.converter_with_ocr
            cprint(
                f"[PROCESSOR] Running Docling conversion on {conversion_path.name}...",
                "cyan",
            )
            result = converter.convert(conversion_path)

            # Extract the document
            docling_document = result.document

            # Get page count
            page_count = (
                len(docling_document.pages) if hasattr(docling_document, "pages") else 0
            )

            cprint(f"[PROCESSOR] Conversion successful: {page_count} pages", "green")

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
                cprint(f"[PROCESSOR] Cleaned up temporary DOCX file", "cyan")

            # Clean up converted PDF if it was created
            if pdf_path_to_cleanup and pdf_path_to_cleanup.exists():
                pdf_path_to_cleanup.unlink()
                cprint(f"[PROCESSOR] Cleaned up converted PDF file", "cyan")


# Global processor instance
document_processor = DocumentProcessor()
