"""
API Client for Content Verification Tool Backend
"""

import requests
import streamlit as st
import logging
from typing import Optional, Dict, Any
from termcolor import cprint
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import (
    BACKEND_URL,
    MAX_FILE_SIZE_MB,
    UPLOAD_TIMEOUT_BASE,
    EXPORT_TIMEOUT,
    DOWNLOAD_TIMEOUT,
    HEALTH_CHECK_TIMEOUT,
)

logger = logging.getLogger(__name__)


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
            progress_bar.progress(100)
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


def upload_reference_documents(
    reference_files, case_context: str, timeout: int = 300
) -> Optional[Dict[str, Any]]:
    """Upload reference documents to create corpus for AI verification"""
    try:
        # Prepare files for upload
        files = [
            ("files", (file.name, file.getvalue(), file.type))
            for file in reference_files
        ]

        # Call API
        response = API_SESSION.post(
            f"{BACKEND_URL}/api/verify/upload-references",
            data={"case_context": case_context},
            files=files,
            timeout=timeout,
        )

        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        st.error("⚠️ Reference upload timed out. Please try again.")
        logger.error("Reference upload timeout")
        return None

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend server. Please contact support.")
        logger.error("Connection error during reference upload")
        return None

    except requests.exceptions.HTTPError as e:
        st.error(f"❌ Failed to upload references: {e.response.text}")
        logger.error(f"HTTP error during reference upload: {e}")
        return None

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        logger.error(f"Unexpected error during reference upload: {e}")
        return None


def execute_verification(
    document_id: str, store_id: str, case_context: str, chunking_mode: str, timeout: int = 600
) -> Optional[Dict[str, Any]]:
    """Execute AI verification against uploaded corpus"""
    try:
        # Call verification API
        response = API_SESSION.post(
            f"{BACKEND_URL}/api/verify/execute",
            json={
                "document_id": document_id,
                "store_id": store_id,
                "case_context": case_context,
                "chunking_mode": chunking_mode,
            },
            timeout=timeout,
        )

        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        st.error("⚠️ Verification timed out. Please try again.")
        logger.error("Verification timeout")
        return None

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend server. Please contact support.")
        logger.error("Connection error during verification")
        return None

    except requests.exceptions.HTTPError as e:
        st.error(f"❌ Verification failed: {e.response.text}")
        logger.error(f"HTTP error during verification: {e}")
        return None

    except Exception as e:
        st.error(f"❌ Error during verification: {str(e)}")
        logger.error(f"Unexpected error during verification: {e}")
        return None


def reset_verification(document_id: str, timeout: int = 10) -> bool:
    """Reset AI verification results for a document"""
    try:
        cprint(f"[FRONTEND] Resetting verification for document: {document_id}", "cyan")

        response = API_SESSION.delete(
            f"{BACKEND_URL}/api/verify/reset/{document_id}",
            timeout=timeout,
        )

        response.raise_for_status()
        result = response.json()

        cprint(
            f"[FRONTEND] Reset successful: {result.get('chunks_reset', 0)} chunks cleared",
            "green",
        )
        return True

    except requests.exceptions.Timeout:
        st.error("⚠️ Reset timed out. Please try again.")
        logger.error("Reset verification timeout")
        return False

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend server. Please contact support.")
        logger.error("Connection error during reset")
        return False

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            st.error("⚠️ Document not found. Please upload the document again.")
        else:
            st.error(f"❌ Reset failed: {e.response.text}")
        logger.error(f"HTTP error during reset: {e}")
        return False

    except Exception as e:
        st.error(f"❌ Error during reset: {str(e)}")
        logger.error(f"Unexpected error during reset: {e}")
        return False
