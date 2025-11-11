"""
Document processing module using Docling for PDF/DOCX conversion
"""
from pathlib import Path
from typing import Dict, Any, Optional
from termcolor import cprint
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

from app.cache import document_cache


# Maximum file size: 100 MB
MAX_FILE_SIZE = 100 * 1024 * 1024

# Supported file extensions
SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


class DocumentProcessor:
    """Handles document conversion using Docling"""

    def __init__(self):
        """Initialize the document processor"""
        cprint("[PROCESSOR] Initializing Docling DocumentConverter...", "cyan")

        # Configure pipeline options for PDF processing
        # Enable table parsing and footnote extraction
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_table_structure = True
        pipeline_options.do_ocr = True

        # Initialize DocumentConverter with format-specific options
        # According to Docling API, pipeline_options must be passed via format_options
        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

        cprint("[PROCESSOR] DocumentConverter initialized successfully", "green")

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

        cprint(f"[PROCESSOR] File validation passed: {filename} ({file_size / 1024:.2f} KB)", "green")

    def convert_document(
        self,
        file_content: bytes,
        filename: str,
        use_cache: bool = True
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
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as tmp_file:
            tmp_path = Path(tmp_file.name)
            tmp_file.write(file_content)

        try:
            # Convert document using Docling
            cprint(f"[PROCESSOR] Running Docling conversion on {tmp_path}...", "cyan")
            result = self.converter.convert(tmp_path)

            # Extract the document
            docling_document = result.document

            # Get page count
            page_count = len(docling_document.pages) if hasattr(docling_document, 'pages') else 0

            cprint(f"[PROCESSOR] Conversion successful: {page_count} pages", "green")

            # Prepare data for caching
            data = {
                "docling_document": docling_document,
                "filename": filename,
                "page_count": page_count,
                "file_size": len(file_content)
            }

            # Cache the result
            if use_cache:
                document_cache.set(file_content, data)

            return data

        except Exception as e:
            cprint(f"[PROCESSOR] Conversion failed: {e}", "red")
            raise Exception(f"Document conversion failed: {str(e)}")

        finally:
            # Clean up temporary file
            if tmp_path.exists():
                tmp_path.unlink()
                cprint(f"[PROCESSOR] Cleaned up temporary file", "cyan")


# Global processor instance
document_processor = DocumentProcessor()
