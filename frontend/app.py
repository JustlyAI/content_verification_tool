"""
Streamlit Frontend for Content Verification Tool
"""

import streamlit as st

# Configure Streamlit page FIRST (before any other st.* commands)
st.set_page_config(
    page_title="Content Verification Tool",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Then other imports
import requests
from pathlib import Path
from typing import Optional, Dict, Any
import os
from termcolor import cprint
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO if os.getenv("DEBUG") != "true" else logging.DEBUG,
    format="[%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Configuration Constants
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
UPLOAD_TIMEOUT_BASE = int(os.getenv("UPLOAD_TIMEOUT_BASE", "180"))
EXPORT_TIMEOUT = int(os.getenv("EXPORT_TIMEOUT", "300"))
DOWNLOAD_TIMEOUT = int(os.getenv("DOWNLOAD_TIMEOUT", "60"))
HEALTH_CHECK_TIMEOUT = int(os.getenv("HEALTH_CHECK_TIMEOUT", "5"))
SUPPORTED_FILE_TYPES = ["pdf", "docx"]

# Output format mappings
OUTPUT_FORMAT_LABELS = {
    "word_landscape": "📄 Word Document (Landscape) - More space for text and notes",
    "word_portrait": "📄 Word Document (Portrait) - Standard layout",
    "excel": "📊 Excel Spreadsheet - Compatible with Excel and Google Sheets",
    "csv": "📋 CSV File - Universal compatibility",
}

MIME_TYPES = {
    "word_landscape": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "word_portrait": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "csv": "text/csv",
}

# Feature flags
FEATURES = {
    "show_debug_info": os.getenv("DEBUG", "false").lower() == "true",
    "show_advanced_options": os.getenv("SHOW_ADVANCED", "false").lower() == "true",
}

# Validate BACKEND_URL format
try:
    parsed = urlparse(BACKEND_URL)
    if not all([parsed.scheme, parsed.netloc]):
        raise ValueError("Invalid BACKEND_URL format")
except Exception as e:
    st.error(f"❌ Configuration error: Invalid BACKEND_URL - {BACKEND_URL}")
    st.info(
        "Please set a valid BACKEND_URL environment variable (e.g., http://localhost:8000)"
    )
    st.stop()


def get_session_with_retries() -> requests.Session:
    """Create requests session with retry strategy"""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "POST"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


# Create API session at module level
API_SESSION = get_session_with_retries()


def calculate_upload_timeout(file_size_mb: float) -> int:
    """Calculate appropriate timeout based on file size (10s per MB minimum)"""
    size_based_timeout = int(file_size_mb * 10)
    return max(UPLOAD_TIMEOUT_BASE, size_based_timeout)


def validate_upload_response(result: dict) -> bool:
    """Validate upload response has required fields"""
    required_fields = ["document_id", "filename", "page_count", "file_size", "message"]
    return all(field in result for field in required_fields)


def validate_export_response(result: dict) -> bool:
    """Validate export response has required fields"""
    required_fields = ["document_id", "filename", "message"]
    return all(field in result for field in required_fields)


@st.cache_data(ttl=30)  # Cache for 30 seconds
def check_backend_health() -> bool:
    """Check if backend is available (cached)"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=HEALTH_CHECK_TIMEOUT)
        return response.status_code == 200
    except Exception:
        return False


def upload_document(
    file_content: bytes, filename: str, progress_bar=None, status_text=None
) -> Optional[Dict[str, Any]]:
    """Upload document to backend API with comprehensive error handling"""
    try:
        if status_text:
            status_text.text("Preparing upload...")
        if progress_bar:
            progress_bar.progress(10)
        logger.info(
            f"User uploaded file: {filename}, size: {len(file_content) / (1024 * 1024):.2f} MB"
        )

        if status_text:
            status_text.text("Uploading document to server...")
        if progress_bar:
            progress_bar.progress(30)

        files = {"file": (filename, file_content)}
        file_size_mb = len(file_content) / (1024 * 1024)
        timeout = calculate_upload_timeout(file_size_mb)

        cprint(f"[FRONTEND] Uploading document: {filename}", "cyan")
        response = API_SESSION.post(
            f"{BACKEND_URL}/upload", files=files, timeout=timeout
        )

        if progress_bar:
            progress_bar.progress(70)
        if status_text:
            status_text.text("Processing document with Docling...")

        response.raise_for_status()
        result = response.json()

        if progress_bar:
            progress_bar.progress(10)
        if status_text:
            status_text.text("✅ Upload complete!")

        cprint(f"[FRONTEND] Upload successful: {filename}", "green")
        return result

    except requests.exceptions.Timeout:
        st.error(
            "⚠️ Upload timed out. Please try again with a smaller file or check your connection."
        )
        cprint(f"[FRONTEND] Upload timeout for {filename}", "red")
        logger.error(f"Upload timeout for {filename}")
        return None

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend server. Please contact support.")
        cprint(f"[FRONTEND] Connection error", "red")
        logger.error("Connection error to backend")
        return None

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            error_detail = e.response.json().get("detail", "Unknown error")
            st.error(f"⚠️ Invalid file: {error_detail}")
        elif e.response.status_code == 413:
            st.error(f"⚠️ File too large. Maximum size is {MAX_FILE_SIZE_MB} MB.")
        else:
            st.error("⚠️ An error occurred processing your file. Please try again.")
        cprint(f"[FRONTEND] HTTP error: {e}", "red")
        logger.error(f"HTTP error during upload: {e}")
        return None

    except Exception as e:
        st.error("⚠️ An unexpected error occurred. Please try again or contact support.")
        cprint(f"[FRONTEND] Unexpected error: {e}", "red")
        logger.error(f"Unexpected error during upload: {e}")
        return None


def export_document(payload: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """Export document to specified format with comprehensive error handling"""
    try:
        logger.info(f"User selected chunking mode: {payload.get('chunking_mode')}")
        logger.info(f"User generated export: {payload.get('output_format')}")

        cprint(
            f"[FRONTEND] Exporting document: {payload['document_id']} ({payload['chunking_mode']} -> {payload['output_format']})",
            "cyan",
        )

        response = API_SESSION.post(
            f"{BACKEND_URL}/export", json=payload, timeout=EXPORT_TIMEOUT
        )
        response.raise_for_status()

        cprint(f"[FRONTEND] Export successful", "green")
        return response.json()

    except requests.exceptions.Timeout:
        st.error("⚠️ Export timed out. Please try again.")
        cprint(f"[FRONTEND] Export timeout", "red")
        logger.error("Export timeout")
        return None

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend server. Please contact support.")
        cprint(f"[FRONTEND] Connection error", "red")
        logger.error("Connection error during export")
        return None

    except requests.exceptions.HTTPError as e:
        st.error(f"⚠️ Export failed: {e.response.status_code}")
        cprint(f"[FRONTEND] Export error: {e}", "red")
        logger.error(f"HTTP error during export: {e}")
        return None

    except Exception as e:
        st.error("⚠️ An unexpected error occurred. Please try again or contact support.")
        cprint(f"[FRONTEND] Unexpected error: {e}", "red")
        logger.error(f"Unexpected error during export: {e}")
        return None


def download_document(document_id: str) -> Optional[bytes]:
    """Download generated verification document with comprehensive error handling"""
    try:
        cprint(f"[FRONTEND] Downloading file for document: {document_id}", "cyan")

        response = API_SESSION.get(
            f"{BACKEND_URL}/download/{document_id}", timeout=DOWNLOAD_TIMEOUT
        )
        response.raise_for_status()

        cprint(f"[FRONTEND] Download successful", "green")
        return response.content

    except requests.exceptions.Timeout:
        st.error("⚠️ Download timed out. Please try again.")
        cprint(f"[FRONTEND] Download timeout", "red")
        logger.error("Download timeout")
        return None

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend server. Please contact support.")
        cprint(f"[FRONTEND] Connection error", "red")
        logger.error("Connection error during download")
        return None

    except requests.exceptions.HTTPError as e:
        st.error(f"⚠️ Download failed: {e.response.status_code}")
        cprint(f"[FRONTEND] Download error: {e}", "red")
        logger.error(f"HTTP error during download: {e}")
        return None

    except Exception as e:
        st.error("⚠️ An unexpected error occurred. Please try again or contact support.")
        cprint(f"[FRONTEND] Unexpected error: {e}", "red")
        logger.error(f"Unexpected error during download: {e}")
        return None


def init_session_state():
    """Initialize session state variables"""
    if "document_id" not in st.session_state:
        st.session_state.document_id = None
    if "document_info" not in st.session_state:
        st.session_state.document_info = None
    if "upload_in_progress" not in st.session_state:
        st.session_state.upload_in_progress = False
    if "last_generated" not in st.session_state:
        st.session_state.last_generated = None


def main() -> None:
    """Main Streamlit application"""

    # Initialize session state
    init_session_state()

    # Header
    st.title("📋 Content Verification Tool")
    st.markdown(
        """
    Convert legal documents (PDF/DOCX) into structured verification checklists.
    Upload your document and generate a table for systematic verification of each sentence or paragraph.
    """
    )

    st.divider()

    # Check backend health with refresh button
    col1, col2 = st.columns([6, 1])
    with col1:
        if not check_backend_health():
            st.error(
                "⚠️ Backend API is not available. Please ensure the backend is running."
            )
            st.code(f"Expected backend at: {BACKEND_URL}", language="text")
            st.stop()
        st.success("✅ Connected to backend")
    with col2:
        if st.button("🔄", help="Refresh connection status"):
            check_backend_health.clear()
            st.rerun()

    # Sidebar for information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown(
            f"""
        ### Features
        - **Document Upload**: PDF or DOCX files (max {MAX_FILE_SIZE_MB} MB)
        - **Chunking Modes**:
          - Paragraph-level (default)
          - Sentence-level
        - **Output Formats**:
          - Word (Landscape)
          - Word (Portrait)
          - Excel
          - CSV

        ### How It Works
        1. Upload your document
        2. Select chunking mode
        3. Choose output format
        4. Generate and download

        ### Output Structure
        Each verification table contains:
        - Page #
        - Item #
        - Text
        - Verified ☑
        - Verification Source
        - Verification Note
        """
        )

        # Reset functionality
        st.divider()
        if st.session_state.document_info or st.session_state.last_generated:
            if st.button("🔄 Start Over", use_container_width=True, type="secondary"):
                st.session_state.document_id = None
                st.session_state.document_info = None
                st.session_state.last_generated = None
                st.session_state.upload_in_progress = False
                check_backend_health.clear()
                st.rerun()

        # Debug info (if enabled)
        if FEATURES["show_debug_info"]:
            st.divider()
            with st.expander("🔍 Debug Information"):
                st.json(
                    {
                        "document_id": st.session_state.document_id,
                        "document_info": st.session_state.document_info,
                        "upload_in_progress": st.session_state.upload_in_progress,
                        "has_generated": st.session_state.last_generated is not None,
                    }
                )

    # Step 1: Document Upload
    st.header("Step 1: Upload Document")
    st.markdown(f"Upload a PDF or DOCX file (maximum {MAX_FILE_SIZE_MB} MB)")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=SUPPORTED_FILE_TYPES,
        help="Supported formats: PDF, DOCX",
        label_visibility="collapsed",
        key="uploaded_file",
    )

    if uploaded_file is not None:
        # Validate file size
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)

        if file_size_mb > MAX_FILE_SIZE_MB:
            st.error(
                f"⚠️ File too large: {file_size_mb:.2f} MB. Maximum allowed size is {MAX_FILE_SIZE_MB} MB."
            )
            st.stop()
        else:
            st.info(f"📄 **File**: {uploaded_file.name} ({file_size_mb:.2f} MB)")

        # Upload button
        upload_button = st.button(
            "🚀 Upload and Process",
            type="primary",
            use_container_width=True,
            disabled=st.session_state.upload_in_progress,
        )

        # Handle upload after button click (progress indicators appear below)
        if upload_button:
            st.session_state.upload_in_progress = True

            # Create progress indicators below the button
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Upload the document
            file_content = uploaded_file.getvalue()
            filename = uploaded_file.name

            result = upload_document(file_content, filename, progress_bar, status_text)

            # Clear only the progress bar, keep status_text for final message
            progress_bar.empty()

            # Handle result
            if result and validate_upload_response(result):
                st.session_state.document_id = result["document_id"]
                st.session_state.document_info = result
                st.session_state.upload_in_progress = False
                # Show success message in place of progress bar
                status_text.success(f"✅ {result['message']}")
            elif result:
                st.session_state.upload_in_progress = False
                status_text.error("⚠️ Invalid response from server. Please try again.")
            else:
                st.session_state.upload_in_progress = False

    # Show document info and processing options if available
    if st.session_state.document_info:
        # Step 2: Chunking Mode Selection
        st.divider()
        st.header("Step 2: Select Chunking Mode")
        st.markdown("Choose how to split the document for verification")

        chunking_mode = st.radio(
            "Chunking Mode",
            options=["paragraph", "sentence"],
            index=0,  # Explicit default to paragraph
            format_func=lambda x: {
                "paragraph": "📝 Paragraph-level chunking",
                "sentence": "📄 Sentence-level chunking",
            }[x],
            help="Paragraph mode groups related content (recommended for most documents). Sentence mode provides finer granularity.",
            label_visibility="collapsed",
        )

        st.caption(
            "**Paragraph mode** (default): Groups related sentences together for coherent verification."
        )
        st.caption(
            "**Sentence mode**: Individual sentences for detailed line-by-line verification."
        )

        # Step 3: Output Format Selection
        st.divider()
        st.header("Step 3: Select Output Format")
        st.markdown("Choose your preferred output format")

        output_format = st.selectbox(
            "Output Format",
            options=list(OUTPUT_FORMAT_LABELS.keys()),
            format_func=lambda x: OUTPUT_FORMAT_LABELS[x],
            help="Select the format that best suits your workflow",
            label_visibility="collapsed",
        )

        # Show format description
        format_descriptions = {
            "word_landscape": "Landscape orientation provides more horizontal space for longer text and detailed notes.",
            "word_portrait": "Portrait orientation offers a standard page layout suitable for printing.",
            "excel": "Excel format allows for advanced filtering, sorting, and formula capabilities.",
            "csv": "CSV format ensures maximum compatibility with all spreadsheet applications.",
        }
        st.info(f"ℹ️ {format_descriptions[output_format]}")

        # Step 4: Generate Document (only if not already generated)
        st.divider()
        if st.session_state.last_generated is None:
            st.header("Step 4: Generate Verification Document")

            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(
                    f"""
                **Ready to generate!**
                - Chunking Mode: **{chunking_mode.title()}**
                - Output Format: **{output_format.replace('_', ' ').title()}**
                """
                )

            with col2:
                generate_button = st.button(
                    "🎯 Generate Document",
                    type="primary",
                    use_container_width=True,
                    help="Click to generate the verification document",
                )

            if generate_button:
                with st.spinner(
                    "Generating verification document... This may take a moment."
                ):
                    payload = {
                        "document_id": st.session_state.document_id,
                        "output_format": output_format,
                        "chunking_mode": chunking_mode,
                    }

                    export_result = export_document(payload)

                    if export_result and validate_export_response(export_result):
                        file_content = download_document(st.session_state.document_id)

                        if file_content:
                            st.session_state.last_generated = {
                                "filename": export_result["filename"],
                                "content": file_content,
                                "mime_type": MIME_TYPES[output_format],
                                "format": output_format,
                            }
                            st.rerun()
                    elif export_result:
                        st.error("⚠️ Invalid export response. Please try again.")

        # Download section (separate from generation)
        if st.session_state.last_generated:
            st.header("Step 4: Download Your Document")
            st.success("🎉 Document ready for download!")

            st.download_button(
                label="⬇️ Download Verification Document",
                data=st.session_state.last_generated["content"],
                file_name=st.session_state.last_generated["filename"],
                mime=st.session_state.last_generated["mime_type"],
                type="primary",
                use_container_width=True,
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("📝 Generate Different Format", use_container_width=True):
                    st.session_state.last_generated = None
                    st.rerun()
            with col2:
                if st.button("📄 Upload New Document", use_container_width=True):
                    st.session_state.document_id = None
                    st.session_state.document_info = None
                    st.session_state.last_generated = None
                    st.rerun()

    # Footer
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.caption("Content Verification Tool v1.0.0 | Built with Streamlit & FastAPI")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error("⚠️ A critical error occurred. Please refresh the page.")
        cprint(f"[FRONTEND] Uncaught exception in main: {e}", "red")
        logger.error(f"Uncaught exception in main: {e}")

        # Show details in debug mode
        if os.getenv("DEBUG", "false").lower() == "true":
            st.exception(e)
