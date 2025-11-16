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
)

# Configure logging
logging.basicConfig(
    level=logging.INFO if os.getenv("DEBUG") != "true" else logging.DEBUG,
    format="[%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def render_corpus_tab() -> None:
    """Render Corpus Management tab with enhanced layout"""
    st.header("Reference Corpus")

    # Status banner
    if st.session_state.reference_docs_uploaded:
        st.success("✅ Corpus Active | Ready for verification")
    else:
        st.warning("⚠️ Corpus Not Configured | Upload reference documents to enable AI verification")

    st.divider()

    # Two-column layout for better organization
    if st.session_state.reference_docs_uploaded:
        # Active corpus: show details in two columns
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📚 Corpus Details")
            from app.corpus import render_active_corpus
            render_active_corpus()

        with col2:
            st.subheader("📊 Statistics")
            # Show corpus statistics
            if st.session_state.corpus_metadata:
                st.metric("Documents", len(st.session_state.corpus_metadata))

            if st.session_state.store_id:
                st.caption("**Store ID:**")
                st.code(st.session_state.store_id, language="text")

            if st.session_state.case_context:
                st.caption("**Case Context:**")
                st.info(st.session_state.case_context)
    else:
        # Corpus creation: full width for form
        from app.corpus import render_corpus_creation
        render_corpus_creation()


def render_upload_card() -> None:
    """Render Card 1: Upload document section"""
    st.markdown("Upload your document to verify")

    # Tip about corpus if not configured
    if not st.session_state.reference_docs_uploaded:
        st.caption("💡 Configure corpus first for AI verification")

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
            st.error(f"⚠️ File too large: {file_size_mb:.2f} MB")
            return
        else:
            st.caption(f"📄 {uploaded_file.name} ({file_size_mb:.2f} MB)")

        # Upload button
        if st.button(
            "🚀 Upload",
            type="primary",
            use_container_width=True,
            disabled=st.session_state.upload_in_progress,
        ):
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
                status_text.success(f"✅ {result['message']}")
            elif result:
                st.session_state.upload_in_progress = False
                status_text.error("⚠️ Invalid response from server")
            else:
                st.session_state.upload_in_progress = False
    elif st.session_state.document_info:
        st.success(f"✅ {st.session_state.document_info.get('filename', 'Document uploaded')}")


def render_chunking_card() -> str:
    """Render Card 2: Chunking mode selection"""
    if not st.session_state.document_info:
        st.caption("Upload a document first")
        return "paragraph"

    st.markdown("Select chunking mode")

    chunking_mode = st.radio(
        "Chunking Mode",
        options=["paragraph", "sentence"],
        index=0,
        format_func=lambda x: {
            "paragraph": "📝 Paragraph",
            "sentence": "📄 Sentence",
        }[x],
        help="Paragraph groups content, Sentence provides finer detail",
        label_visibility="collapsed",
    )

    return chunking_mode


def render_verify_card(chunking_mode: str) -> None:
    """Render Card 3: AI Verification"""
    if not st.session_state.document_info:
        st.caption("Upload a document first")
        return

    if not st.session_state.reference_docs_uploaded:
        st.caption("⚠️ Corpus not active")
        return

    if st.session_state.verification_complete:
        st.success("✅ Verification complete")
        return

    st.markdown("Run AI verification")

    if st.button("🚀 Verify", type="primary", use_container_width=True):
        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.text("Verifying...")

        result = execute_verification(
            document_id=st.session_state.document_id,
            store_id=st.session_state.store_id,
            case_context=st.session_state.case_context,
            chunking_mode=chunking_mode,
        )

        if result:
            st.session_state.verification_complete = True
            st.session_state.verification_results = result
            st.session_state.chunking_mode = chunking_mode

            progress_bar.progress(100)
            status_text.success("✅ Done!")
            st.rerun()
        else:
            progress_bar.empty()
            status_text.empty()


def render_export_card(chunking_mode: str) -> None:
    """Render Card 4: Output format and export"""
    if not st.session_state.document_info:
        st.caption("Upload a document first")
        return

    st.markdown("Select format & export")

    output_format = st.selectbox(
        "Output Format",
        options=list(OUTPUT_FORMAT_LABELS.keys()),
        format_func=lambda x: OUTPUT_FORMAT_LABELS[x].split(" - ")[0],  # Shorter labels
        help="Select output format",
        label_visibility="collapsed",
    )

    # Show download if already generated
    if st.session_state.last_generated:
        st.download_button(
            label="⬇️ Download",
            data=st.session_state.last_generated["content"],
            file_name=st.session_state.last_generated["filename"],
            mime=st.session_state.last_generated["mime_type"],
            type="primary",
            use_container_width=True,
        )

        if st.button("🔄 New Format", use_container_width=True):
            st.session_state.last_generated = None
            st.rerun()
    else:
        # Generate button
        if st.button(
            "🎯 Generate",
            type="primary",
            use_container_width=True,
        ):
            with st.spinner("Generating..."):
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
                    st.error("⚠️ Export failed")


def render_results_section() -> None:
    """Render results section below verification cards"""
    if not st.session_state.verification_complete:
        return

    st.divider()
    st.subheader("📊 Verification Results")

    results = st.session_state.verification_results

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Chunks", results.get("total_chunks", 0))
    with col2:
        verified_count = results.get("total_verified", 0)
        total_count = results.get("total_chunks", 0)
        verified_pct = (verified_count / total_count * 100) if total_count > 0 else 0
        st.metric("Verified", f"{verified_count}", f"{verified_pct:.1f}%")
    with col3:
        # Calculate average confidence
        scores = [
            c.get("verification_score", 0)
            for c in results.get("verified_chunks", [])
            if c.get("verified") and c.get("verification_score")
        ]
        avg_score = sum(scores) / len(scores) if scores else 0
        st.metric("Avg Confidence", f"{avg_score:.1f}/10")
    with col4:
        st.metric("Time", f"{results.get('processing_time_seconds', 0):.1f}s")

    st.divider()

    # Confidence breakdown
    scores_exist = bool(scores)
    if scores_exist:
        low_confidence = sum(1 for s in scores if s < 5)
        medium_confidence = sum(1 for s in scores if 5 <= s < 8)
        high_confidence = sum(1 for s in scores if s >= 8)

        st.markdown("**Confidence Distribution:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔴 Low (<5)", low_confidence)
        with col2:
            st.metric("🟡 Medium (5-7)", medium_confidence)
        with col3:
            st.metric("🟢 High (8-10)", high_confidence)

    # Reset verification button
    st.divider()
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        from app.api_client import reset_verification
        from app.state import reset_verification_state

        if st.button(
            "🔄 Reset Verification",
            type="secondary",
            use_container_width=True,
            help="Clear verification results and re-verify",
        ):
            if st.session_state.document_id:
                with st.spinner("Clearing verification results..."):
                    success = reset_verification(st.session_state.document_id)
                    if success:
                        reset_verification_state()
                        st.success("✅ Verification cleared!")
                        st.rerun()


def render_verification_tab() -> None:
    """Render Verification tab with horizontal cards"""
    st.header("Document Verification")

    # Create 4 horizontal cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container():
            st.markdown("### 1️⃣ Upload")
            render_upload_card()

    with col2:
        with st.container():
            st.markdown("### 2️⃣ Chunking")
            chunking_mode = render_chunking_card()

    with col3:
        with st.container():
            st.markdown("### 3️⃣ Verify")
            render_verify_card(chunking_mode)

    with col4:
        with st.container():
            st.markdown("### 4️⃣ Export")
            render_export_card(chunking_mode)

    # Results section below cards
    render_results_section()


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

    st.divider()

    # Tab-based navigation
    tab1, tab2 = st.tabs(["📚 Corpus", "✅ Verification"])

    with tab1:
        render_corpus_tab()

    with tab2:
        render_verification_tab()

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
