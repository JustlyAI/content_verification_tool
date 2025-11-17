"""
Streamlit Frontend for Content Verification Tool
Main application entry point with modular architecture
"""

import streamlit as st

# Configure Streamlit page FIRST (before any other st.* commands)
st.set_page_config(
    page_title="Content Verification | Powered by Gemini",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed",  # Firm single-screen design
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
from app.styles import load_css
from app.corpus import render_corpus_sidebar

# Configure logging
logging.basicConfig(
    level=logging.INFO if os.getenv("DEBUG") != "true" else logging.DEBUG,
    format="[%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


# Removed render_corpus_tab() - using single-screen layout now


def render_upload_card() -> None:
    """Render Card 1: Upload document section"""
    uploaded_file = st.file_uploader(
        "Document to verify",
        type=SUPPORTED_FILE_TYPES,
        key="uploaded_file",
        label_visibility="collapsed",
        help="This document will be verified against your reference corpus",
    )

    if uploaded_file is not None:
        # Validate file size
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)

        if file_size_mb > MAX_FILE_SIZE_MB:
            st.error(f"⚠️ File too large: {file_size_mb:.2f} MB")
            return

        # Upload button
        if not st.session_state.document_info:
            if st.button(
                "🚀 Upload",
                type="primary",
                use_container_width=True,
                disabled=st.session_state.upload_in_progress,
                key="upload_btn",
            ):
                st.session_state.upload_in_progress = True

                # Create progress indicators
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Upload the document
                file_content = uploaded_file.getvalue()
                filename = uploaded_file.name

                result = upload_document(
                    file_content, filename, progress_bar, status_text
                )

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
        else:
            st.success("✓ Ready to Verify")
            st.caption(
                f"📄 {st.session_state.document_info.get('filename', 'Document uploaded')}"
            )
            file_size = (
                st.session_state.document_info.get("size", 0) / 1024
                if st.session_state.document_info.get("size")
                else file_size_mb
            )
            st.caption(f"{file_size:.1f} KB")
    elif st.session_state.document_info:
        st.success("✓ Ready to Verify")
        st.caption(
            f"📄 {st.session_state.document_info.get('filename', 'Document uploaded')}"
        )
    else:
        st.info("Upload document to begin")
        st.caption("Supported: PDF, DOCX")


def render_chunking_card() -> None:
    """Render Card 2: Splitting mode selection"""
    if not st.session_state.document_info:
        st.caption("Choose how to split your document")
        return

    st.markdown("**Processing Mode**")

    # If verification is complete, show locked selection
    if st.session_state.verification_complete:
        mode_display = st.session_state.splitting_mode.capitalize()
        st.info(f"🔒 {mode_display}-level (locked)")
        st.caption(f"Selected for verification")
        return

    # Otherwise, show radio button and update session state
    # Get the current index based on session state
    current_index = 0 if st.session_state.splitting_mode == "paragraph" else 1

    splitting_mode = st.radio(
        "Mode",
        options=["paragraph", "sentence"],
        index=current_index,
        format_func=lambda x: {
            "paragraph": "Paragraph",
            "sentence": "Sentence",
        }[x],
        key="chunk_mode_radio",
        label_visibility="collapsed",
        horizontal=False,
    )

    # Update session state with selected value
    st.session_state.splitting_mode = splitting_mode

    st.success(f"✓ {splitting_mode.capitalize()}-level")
    st.caption(f"Split into {splitting_mode}s for detailed analysis")


def render_verify_card() -> None:
    """Render Card 3: AI Verification with Gemini branding"""
    if st.session_state.verification_complete:
        st.success("✅ Verification complete")
        st.caption("Results displayed below")
        return

    if not st.session_state.document_info:
        st.caption("Verify split content against the corpus")
        return

    if not st.session_state.reference_docs_uploaded:
        st.warning("⏳ Corpus Needed")
        st.caption("Create a corpus first")
        return

    # Show corpus ready status
    doc_count = (
        len(st.session_state.corpus_metadata) if st.session_state.corpus_metadata else 0
    )
    st.info(f"🔷 Corpus Ready ({doc_count} docs)")

    # Check if we're already processing
    is_processing = st.session_state.get("verification_in_progress", False)

    # Use button with key to track clicks (no callback needed)
    verify_clicked = st.button(
        "▶ Run Verification",
        type="primary",
        use_container_width=True,
        disabled=is_processing,
        key="verify_gemini",
    )

    # Process verification when button is clicked (only once per click)
    if verify_clicked and not is_processing:
        # Set processing flag immediately to prevent double-execution
        st.session_state.verification_in_progress = True

        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.text("Gemini is verifying...")

        result = execute_verification(
            document_id=st.session_state.document_id,
            store_id=st.session_state.store_id,
            case_context=st.session_state.case_context,
            splitting_mode=st.session_state.splitting_mode,
        )

        if result:
            st.session_state.verification_complete = True
            st.session_state.verification_results = result

            progress_bar.progress(100)
            status_text.success("✅ Verification complete!")
        else:
            progress_bar.empty()
            status_text.empty()

        # Clear processing flag
        st.session_state.verification_in_progress = False
        # Streamlit will automatically rerun when session state changes


def render_export_card() -> None:
    """Render Card 4: Output format and export"""
    if not st.session_state.document_info:
        st.caption("Export split and verified content")
        return

    st.markdown("Select format & export")

    output_format = st.selectbox(
        "Output Format",
        options=list(OUTPUT_FORMAT_LABELS.keys()),
        format_func=lambda x: OUTPUT_FORMAT_LABELS[x].split(" - ")[0],  # Shorter labels
        help="Select output format",
        label_visibility="collapsed",
        disabled=st.session_state.verification_in_progress,
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
            disabled=st.session_state.verification_in_progress,
        )

        if st.button(
            "🔄 New Format",
            use_container_width=True,
            disabled=st.session_state.verification_in_progress,
        ):
            st.session_state.last_generated = None
            # Streamlit will automatically rerun when session state changes
    else:
        # Generate button
        button_disabled = st.session_state.verification_in_progress
        if st.button(
            "🎯 Generate",
            type="primary",
            use_container_width=True,
            disabled=button_disabled,
        ):
            with st.spinner("Generating..."):
                payload = {
                    "document_id": st.session_state.document_id,
                    "output_format": output_format,
                    "splitting_mode": st.session_state.splitting_mode,
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


# Removed render_verification_tab() - using render_verification_workflow() now


def main() -> None:
    """Main Streamlit application - Firm single-screen design"""

    # Validate configuration
    validate_backend_url()

    # Initialize session state
    init_session_state()

    # Load Firm CSS
    load_css()

    # Render header
    render_header()

    # Check backend (only show if unhealthy)
    from app.api_client import check_backend_health

    if not check_backend_health():
        st.error(
            "⚠️ Backend API is not available. Please ensure the backend is running."
        )
        from app.config import BACKEND_URL

        st.code(f"Expected backend at: {BACKEND_URL}", language="text")
        st.stop()

    # Main layout: sidebar + content (Firm single-screen)
    sidebar_col, main_col = st.columns([1, 3], gap="small")

    # SIDEBAR: Corpus
    with sidebar_col:
        render_corpus_sidebar()

    # MAIN CONTENT: Workflow + Results
    with main_col:
        st.markdown('<div class="fm-main-content">', unsafe_allow_html=True)

        # Header
        st.markdown("## AI-Powered Content Verification")

        # Workflow explanation
        st.info(
            "**🔄 Verification Workflow:** (1) Upload your document → "
            "(2) Choose splitting mode → (3) Run AI verification against corpus → "
            "(4) Export results"
        )

        # Render verification workflow (4 horizontal cards)
        render_verification_workflow()

        st.markdown("</div>", unsafe_allow_html=True)

    # Render legacy sidebar for info (optional, can be removed)
    render_sidebar()

    # Footer
    render_footer()


def render_verification_workflow() -> None:
    """Render the 4-card verification workflow"""
    # Create 4 horizontal cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            '<div class="fm-card">'
            '<div class="fm-card-number">STEP 1</div>'
            '<div class="fm-card-title">Upload</div>',
            unsafe_allow_html=True,
        )
        render_upload_card()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            '<div class="fm-card">'
            '<div class="fm-card-number">STEP 2</div>'
            '<div class="fm-card-title">Split</div>',
            unsafe_allow_html=True,
        )
        render_chunking_card()
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        # Gemini card with special styling
        st.markdown(
            '<div class="fm-card fm-gemini-card">'
            '<div class="fm-card-number">STEP 3</div>'
            '<div class="fm-card-title">Verify with AI</div>',
            unsafe_allow_html=True,
        )

        render_verify_card()
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown(
            '<div class="fm-card">'
            '<div class="fm-card-number">STEP 4</div>'
            '<div class="fm-card-title">Export</div>',
            unsafe_allow_html=True,
        )
        render_export_card()
        st.markdown("</div>", unsafe_allow_html=True)

    # Results section below cards
    render_results_section()


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
