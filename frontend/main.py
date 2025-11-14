"""
Streamlit Frontend for Content Verification Tool
Main application entry point with modular architecture
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
import os
import logging
from termcolor import cprint

# Import application modules
from app.config import (
    validate_backend_url,
    SUPPORTED_FILE_TYPES,
    MAX_FILE_SIZE_MB,
    OUTPUT_FORMAT_LABELS,
    FORMAT_DESCRIPTIONS,
    MIME_TYPES,
)
from app.state import init_session_state
from app.api_client import (
    upload_document,
    export_document,
    download_document,
    execute_verification,
    validate_upload_response,
    validate_export_response,
)
from app.ui_components import (
    render_header,
    render_backend_status,
    render_sidebar,
    render_footer,
    render_verification_results_summary,
)
from app.corpus import render_corpus_management

# Configure logging
logging.basicConfig(
    level=logging.INFO if os.getenv("DEBUG") != "true" else logging.DEBUG,
    format="[%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def render_document_upload() -> None:
    """Render Step 1: Document Upload section"""
    st.header("Step 1: Upload Document To Verify")
    st.markdown(f"Upload a PDF or DOCX file (maximum {MAX_FILE_SIZE_MB} MB)")

    # Tip about corpus if not configured
    if not st.session_state.reference_docs_uploaded:
        st.info(
            "💡 **Tip**: Expand 'AI Reference Corpus' above to enable automated verification"
        )

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

        # Handle upload after button click
        if upload_button:
            st.session_state.upload_in_progress = True

            # Create progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Upload the document
            file_content = uploaded_file.getvalue()
            filename = uploaded_file.name

            result = upload_document(file_content, filename, progress_bar, status_text)

            # Clear only the progress bar
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


def render_chunking_selection() -> str:
    """Render Step 2: Chunking Mode Selection and return selected mode"""
    st.divider()
    st.header("Step 2: Select Chunking Mode")
    st.markdown("Choose how to split the document for verification")

    # Tip about AI verification if corpus is active
    if st.session_state.reference_docs_uploaded:
        st.success(
            "🤖 AI Verification is enabled - you'll be able to run verification after selecting chunking mode"
        )

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

    return chunking_mode


def render_ai_verification(chunking_mode: str) -> None:
    """Render Step 2.5: AI Verification section (if corpus is active)"""
    if (
        not st.session_state.reference_docs_uploaded
        or st.session_state.verification_complete
    ):
        return

    st.divider()
    st.header("✨ Step 2.5: Run AI Verification")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.info("📊 Ready to verify chunks against reference documents")
    with col2:
        if st.button("🚀 Verify Now", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.text("Starting verification...")

            result = execute_verification(
                document_id=st.session_state.document_id,
                store_id=st.session_state.store_id,
                case_context=st.session_state.case_context,
                chunking_mode=chunking_mode,
            )

            if result:
                progress_bar.progress(50)
                status_text.text("Processing verification results...")

                st.session_state.verification_complete = True
                st.session_state.verification_results = result
                st.session_state.chunking_mode = chunking_mode

                progress_bar.progress(100)
                status_text.text("Verification complete!")

                # Show statistics
                st.success("✅ AI Verification Complete!")

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Chunks", result["total_chunks"])
                with col2:
                    verified_count = result["total_verified"]
                    verified_pct = (
                        (verified_count / result["total_chunks"] * 100)
                        if result["total_chunks"] > 0
                        else 0
                    )
                    st.metric(
                        "Verified",
                        f"{verified_count}",
                        f"{verified_pct:.1f}%",
                    )
                with col3:
                    st.metric(
                        "Processing Time",
                        f"{result['processing_time_seconds']:.1f}s",
                    )
                with col4:
                    # Calculate average confidence
                    scores = [
                        c.get("verification_score", 0)
                        for c in result["verified_chunks"]
                        if c.get("verified") and c.get("verification_score")
                    ]
                    avg_score = sum(scores) / len(scores) if scores else 0
                    st.metric("Avg Confidence", f"{avg_score:.1f}/10")

                st.rerun()
            else:
                progress_bar.empty()
                status_text.empty()


def render_output_format_selection() -> str:
    """Render Step 3: Output Format Selection and return selected format"""
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
    st.info(f"ℹ️ {FORMAT_DESCRIPTIONS[output_format]}")

    return output_format


def render_generate_document(chunking_mode: str, output_format: str) -> None:
    """Render Step 4: Generate Document section"""
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
            with st.spinner("Generating verification document... This may take a moment."):
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


def render_download_section() -> None:
    """Render download section (when document is ready)"""
    if not st.session_state.last_generated:
        return

    st.header("Step 4: Download Your Document")
    st.success("🎉 Document ready for download!")

    # Show verification status if available
    if st.session_state.verification_complete:
        st.info(
            "📊 This document includes AI verification results with confidence scores and citations"
        )

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


def main() -> None:
    """Main Streamlit application"""

    # Validate configuration
    validate_backend_url()

    # Initialize session state
    init_session_state()

    # Render header and check backend
    render_header()
    render_backend_status()

    # Render sidebar
    render_sidebar()

    # CORPUS MANAGEMENT PANEL (NEW - Always at top)
    render_corpus_management()

    st.divider()

    # Step 1: Document Upload
    render_document_upload()

    # Show remaining steps only if document is uploaded
    if st.session_state.document_info:
        # Step 2: Chunking Mode Selection
        chunking_mode = render_chunking_selection()

        # Step 2.5: Run AI Verification (if corpus active and not complete)
        render_ai_verification(chunking_mode)

        # Show verification results summary if complete
        render_verification_results_summary()

        # Step 3: Output Format Selection
        output_format = render_output_format_selection()

        # Step 4: Generate Document
        render_generate_document(chunking_mode, output_format)

        # Download section (if generated)
        render_download_section()

    # Footer
    render_footer()


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
