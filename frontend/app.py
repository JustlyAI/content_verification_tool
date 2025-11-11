"""
Streamlit Frontend for Content Verification Tool
"""

import streamlit as st
import requests
from pathlib import Path
from typing import Optional
import os
from termcolor import cprint


# Backend API URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Configure Streamlit page
st.set_page_config(
    page_title="Content Verification Tool",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)


def check_backend_health() -> bool:
    """Check if backend is available"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def upload_document(file_content: bytes, filename: str) -> Optional[dict]:
    """
    Upload document to backend

    Args:
        file_content: File content bytes
        filename: Original filename

    Returns:
        Response data or None if error
    """
    try:
        cprint(f"[FRONTEND] Uploading document: {filename}", "cyan")
        files = {"file": (filename, file_content)}
        response = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=180)
        response.raise_for_status()
        cprint(f"[FRONTEND] Upload successful", "green")
        return response.json()
    except Exception as e:
        cprint(f"[FRONTEND] Upload error: {e}", "red")
        st.error(f"Error uploading document: {str(e)}")
        return None


def export_document(
    document_id: str, chunking_mode: str, output_format: str
) -> Optional[dict]:
    """
    Request document export from backend

    Args:
        document_id: Document identifier
        chunking_mode: Chunking mode (paragraph or sentence)
        output_format: Output format

    Returns:
        Response data or None if error
    """
    try:
        cprint(
            f"[FRONTEND] Exporting document: {document_id} ({chunking_mode} -> {output_format})",
            "cyan",
        )
        payload = {
            "document_id": document_id,
            "chunking_mode": chunking_mode,
            "output_format": output_format,
        }
        response = requests.post(f"{BACKEND_URL}/export", json=payload, timeout=300)
        response.raise_for_status()
        cprint(f"[FRONTEND] Export successful", "green")
        return response.json()
    except Exception as e:
        cprint(f"[FRONTEND] Export error: {e}", "red")
        st.error(f"Error exporting document: {str(e)}")
        return None


def download_file(document_id: str, filename: str) -> Optional[bytes]:
    """
    Download exported file from backend

    Args:
        document_id: Document identifier
        filename: Expected filename

    Returns:
        File content bytes or None if error
    """
    try:
        cprint(f"[FRONTEND] Downloading file: {filename}", "cyan")
        response = requests.get(f"{BACKEND_URL}/download/{document_id}", timeout=60)
        response.raise_for_status()
        cprint(f"[FRONTEND] Download successful", "green")
        return response.content
    except Exception as e:
        cprint(f"[FRONTEND] Download error: {e}", "red")
        st.error(f"Error downloading file: {str(e)}")
        return None


def main():
    """Main Streamlit application"""

    # Header
    st.title("📋 Content Verification Tool")
    st.markdown(
        """
    Convert legal documents (PDF/DOCX) into structured verification checklists.
    Upload your document and generate a table for systematic verification of each sentence or paragraph.
    """
    )

    st.divider()

    # Check backend health
    with st.spinner("Checking backend connection..."):
        if not check_backend_health():
            st.error(
                "⚠️ Backend API is not available. Please ensure the backend server is running."
            )
            st.info(f"Backend URL: {BACKEND_URL}")
            st.stop()

    st.success("✅ Connected to backend API")

    # Sidebar for information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown(
            """
        ### Features
        - **Document Upload**: PDF or DOCX files (max 10 MB)
        - **Chunking Modes**:
          - Paragraph-level
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

    # Initialize session state
    if "document_id" not in st.session_state:
        st.session_state.document_id = None
    if "document_info" not in st.session_state:
        st.session_state.document_info = None

    # Step 1: Document Upload
    st.header("Step 1: Upload Document")
    st.markdown("Upload a PDF or DOCX file (maximum 10 MB)")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx"],
        help="Supported formats: PDF, DOCX",
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        # Show file info
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        st.info(f"📄 **File**: {uploaded_file.name} ({file_size_mb:.2f} MB)")

        # Upload button
        if st.button("🚀 Upload and Process", type="primary", use_container_width=True):
            with st.spinner("Uploading and converting document..."):
                # Upload document
                result = upload_document(uploaded_file.getvalue(), uploaded_file.name)

                if result:
                    st.session_state.document_id = result["document_id"]
                    st.session_state.document_info = result
                    st.success(f"✅ {result['message']}")

    # Show document info if available
    if st.session_state.document_info:
        # Step 2: Chunking Mode Selection
        st.divider()
        st.header("Step 2: Select Chunking Mode")
        st.markdown("Choose how to split the document for verification")

        chunking_mode = st.radio(
            "Chunking Mode",
            options=["paragraph", "sentence"],
            format_func=lambda x: {
                "paragraph": "📝 Paragraph-level chunking (groups related sentences)",
                "sentence": "📄 Sentence-level chunking (individual sentences)",
            }[x],
            help="Paragraph mode groups related content, while sentence mode provides finer granularity",
            label_visibility="collapsed",
        )

        # Show mode description
        if chunking_mode == "paragraph":
            st.info(
                """
            **Paragraph Mode**: Groups related sentences together for verification.
            Best for documents where context matters and sentences are interconnected.
            """
            )
        else:
            st.info(
                """
            **Sentence Mode**: Splits text into individual sentences for detailed verification.
            Best for documents requiring precise, sentence-by-sentence review.
            """
            )

        # Step 3: Output Format Selection
        st.divider()
        st.header("Step 3: Select Output Format")
        st.markdown("Choose your preferred output format")

        output_format = st.selectbox(
            "Output Format",
            options=["word_landscape", "word_portrait", "excel", "csv"],
            format_func=lambda x: {
                "word_landscape": "📄 Word Document (Landscape) - More space for text and notes",
                "word_portrait": "📄 Word Document (Portrait) - Standard layout",
                "excel": "📊 Excel Spreadsheet - Compatible with Excel and Google Sheets",
                "csv": "📋 CSV File - Universal compatibility",
            }[x],
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

        # Step 4: Generate and Download
        st.divider()
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
                # Export document
                export_result = export_document(
                    st.session_state.document_id, chunking_mode, output_format
                )

                if export_result:
                    st.success(f"✅ {export_result['message']}")

                    # Download file
                    with st.spinner("Preparing download..."):
                        file_content = download_file(
                            st.session_state.document_id, export_result["filename"]
                        )

                        if file_content:
                            # Determine MIME type
                            if output_format in ["word_landscape", "word_portrait"]:
                                mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            elif output_format == "excel":
                                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            else:
                                mime_type = "text/csv"

                            # Offer download
                            st.download_button(
                                label="⬇️ Download Verification Document",
                                data=file_content,
                                file_name=export_result["filename"],
                                mime=mime_type,
                                type="primary",
                                use_container_width=True,
                            )

                            st.success("🎉 Document ready for download!")

    # Footer
    st.divider()
    st.markdown(
        """
    <div style='text-align: center; color: #666; padding: 20px;'>
    <small>Content Verification Tool v1.0.0 | Built with Streamlit & FastAPI</small>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
