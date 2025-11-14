"""
Configuration and constants for the Content Verification Tool
"""

import os
from urllib.parse import urlparse
import streamlit as st

# Backend Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# File Upload Limits
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))

# Timeout Configuration
UPLOAD_TIMEOUT_BASE = int(os.getenv("UPLOAD_TIMEOUT_BASE", "180"))
EXPORT_TIMEOUT = int(os.getenv("EXPORT_TIMEOUT", "300"))
DOWNLOAD_TIMEOUT = int(os.getenv("DOWNLOAD_TIMEOUT", "60"))
HEALTH_CHECK_TIMEOUT = int(os.getenv("HEALTH_CHECK_TIMEOUT", "5"))

# Supported File Types
SUPPORTED_FILE_TYPES = ["pdf", "docx"]

# Output Format Configuration
OUTPUT_FORMAT_LABELS = {
    "word_landscape": "📄 Word Document (Landscape) - More space for text and notes",
    "word_portrait": "📄 Word Document (Portrait) - Standard layout",
    "excel": "📊 Excel Spreadsheet - Compatible with Excel and Google Sheets",
    "csv": "📋 CSV File - Universal compatibility",
    "json": "📊 JSON File - Full verification metadata with citations",
}

MIME_TYPES = {
    "word_landscape": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "word_portrait": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "csv": "text/csv",
    "json": "application/json",
}

FORMAT_DESCRIPTIONS = {
    "word_landscape": "Landscape orientation provides more horizontal space for longer text and detailed notes.",
    "word_portrait": "Portrait orientation offers a standard page layout suitable for printing.",
    "excel": "Excel format allows for advanced filtering, sorting, and formula capabilities.",
    "csv": "CSV format ensures maximum compatibility with all spreadsheet applications.",
    "json": "JSON format provides complete verification data with metadata and citations.",
}

# Feature Flags
FEATURES = {
    "show_debug_info": os.getenv("DEBUG", "false").lower() == "true",
    "show_advanced_options": os.getenv("SHOW_ADVANCED", "false").lower() == "true",
}


def validate_backend_url() -> None:
    """Validate BACKEND_URL format and show error if invalid"""
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
