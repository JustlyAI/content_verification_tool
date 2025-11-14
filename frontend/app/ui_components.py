"""
Reusable UI Components for Content Verification Tool
"""

import streamlit as st
from .config import BACKEND_URL, MAX_FILE_SIZE_MB, FEATURES
from .api_client import check_backend_health
from .state import reset_all_state


def render_header() -> None:
    """Render the main header"""
    st.title("📋 Content Verification Tool")
    st.markdown(
        """
    Convert legal documents (PDF/DOCX) into structured verification checklists.
    Upload your document and generate a table for systematic verification of each sentence or paragraph.
    """
    )
    st.divider()


def render_backend_status() -> None:
    """Render backend health status with refresh button"""
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


def render_sidebar() -> None:
    """Render the sidebar with information and controls"""
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown(
            f"""
        ### Features
        - **Document Upload**: PDF or DOCX files (max {MAX_FILE_SIZE_MB} MB)
        - **AI Verification**: Upload reference documents for automated verification
        - **Chunking Modes**:
          - Paragraph-level (default)
          - Sentence-level
        - **Output Formats**:
          - Word (Landscape)
          - Word (Portrait)
          - Excel
          - CSV
          - JSON (with verification metadata)

        ### How It Works
        1. (Optional) Create AI reference corpus
        2. Upload your document
        3. Select chunking mode
        4. Run AI verification (if corpus active)
        5. Choose output format
        6. Generate and download

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
                reset_all_state()
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
                        "corpus_active": st.session_state.reference_docs_uploaded,
                        "store_id": st.session_state.store_id,
                        "verification_complete": st.session_state.verification_complete,
                    }
                )


def render_footer() -> None:
    """Render the footer"""
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.caption("Content Verification Tool v1.0.0 | Built with Streamlit & FastAPI")


def render_verification_results_summary() -> None:
    """Render verification results summary section"""
    if not st.session_state.verification_complete:
        return

    st.divider()
    st.header("📊 Verification Results Summary")

    results = st.session_state.verification_results
    verified_count = results.get("total_verified", 0)
    total_count = results.get("total_chunks", 0)
    unverified_count = total_count - verified_count

    col1, col2 = st.columns(2)
    with col1:
        st.success(f"✅ **Verified:** {verified_count} chunks")
    with col2:
        st.warning(f"⚠️ **Unverified:** {unverified_count} chunks")

    # Show confidence breakdown
    if results.get("verified_chunks"):
        scores = [
            c.get("verification_score", 0)
            for c in results["verified_chunks"]
            if c.get("verified") and c.get("verification_score")
        ]

        if scores:
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
