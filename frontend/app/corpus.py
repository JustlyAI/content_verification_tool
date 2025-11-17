"""
Corpus Management UI Components for AI Verification
Firm-inspired compact sidebar design
"""

import streamlit as st
from .api_client import upload_reference_documents, delete_corpus
from .state import reset_corpus_state


def render_corpus_creation() -> None:
    """Render corpus creation form (when no active corpus)"""
    st.markdown("Upload reference documents to enable AI verification")

    # Show clearer instructions
    st.info("📝 **Instructions:** Upload reference documents to enable the button")

    case_context = st.text_area(
        "Case Context (Optional)",
        placeholder="Describe what you're verifying (e.g., 'Contract verification for Project X')",
        max_chars=500,
        help="Provide context to help AI understand the verification case (optional but recommended)",
        key="case_context_input",
    )

    reference_files = st.file_uploader(
        "Select Reference Documents *",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        help="Upload documents as grounding for verification (PDF or DOCX)",
        key="reference_uploader",
    )

    # Show status of required fields
    if not reference_files:
        st.warning("⚠️ Please provide: Reference Documents")

    if st.button(
        "Create Reference Library",
        disabled=not reference_files,
        type="primary",
        use_container_width=True,
    ):
        with st.spinner("Creating reference library..."):
            result = upload_reference_documents(reference_files, case_context)

            if result:
                # Store corpus information in session state
                st.session_state.store_id = result["store_id"]
                st.session_state.reference_docs_uploaded = True
                st.session_state.case_context = case_context
                st.session_state.corpus_metadata = result.get("metadata", [])
                st.session_state.corpus_just_created = True
                # Force rerun to update sidebar status immediately
                st.rerun()


def render_active_corpus() -> None:
    """Render active corpus information and management"""
    # Show one-time success message if corpus was just created
    if st.session_state.get("corpus_just_created", False):
        doc_count = (
            len(st.session_state.corpus_metadata)
            if st.session_state.corpus_metadata
            else 0
        )
        st.success(f"✅ Uploaded {doc_count} reference document(s) successfully!")
        st.session_state.corpus_just_created = False

    st.success("✅ Corpus is active and ready for verification")

    # Display corpus information
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"📦 **Store ID:** `{st.session_state.store_id}`")
    with col2:
        if st.session_state.case_context:
            st.info(f"📝 **Context:** {st.session_state.case_context[:50]}...")

    # Display metadata if available
    if st.session_state.corpus_metadata:
        with st.expander("📄 View Document Metadata", expanded=False):
            for meta in st.session_state.corpus_metadata:
                st.markdown(f"**{meta['filename']}**")
                st.caption(f"Type: {meta.get('document_type', 'N/A')}")
                st.caption(f"Summary: {meta.get('summary', 'N/A')}")
                st.divider()

    st.divider()

    # Clear corpus button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("🗑️ Clear Corpus", type="secondary", use_container_width=True):
            reset_corpus_state()
            # Streamlit will automatically rerun when session state changes


def render_corpus_sidebar() -> None:
    """
    Render the corpus sidebar with Firm styling
    Compact design for always-visible sidebar
    """
    st.markdown('<div class="fm-sidebar-content">', unsafe_allow_html=True)

    st.markdown("## Reference Corpus")
    st.info(
        "📚 **Knowledge Base** - Upload reference documents as grounding for verification"
    )

    # Status
    if st.session_state.reference_docs_uploaded:
        st.success("✓ Active & Verification-Ready")
    else:
        st.warning("⏳ No Corpus Loaded")

    # Stats (if corpus is active)
    if st.session_state.reference_docs_uploaded:
        col1, col2 = st.columns(2)
        with col1:
            doc_count = (
                len(st.session_state.corpus_metadata)
                if st.session_state.corpus_metadata
                else 0
            )
            st.metric("Documents", doc_count)

            # Calculate total storage from metadata
            total_bytes = 0
            if st.session_state.corpus_metadata:
                for doc_meta in st.session_state.corpus_metadata:
                    # Access file_size_bytes attribute
                    if hasattr(doc_meta, "file_size_bytes"):
                        total_bytes += doc_meta.file_size_bytes
                    elif isinstance(doc_meta, dict) and "file_size_bytes" in doc_meta:
                        total_bytes += doc_meta["file_size_bytes"]

            total_mb = total_bytes / (1024 * 1024)
            st.metric("Storage", f"{total_mb:.1f} MB")

        with col2:
            # Calculate total pages from metadata
            total_pages = 0
            if st.session_state.corpus_metadata:
                for doc_meta in st.session_state.corpus_metadata:
                    # Access page_count attribute
                    if hasattr(doc_meta, "page_count"):
                        total_pages += doc_meta.page_count
                    elif isinstance(doc_meta, dict) and "page_count" in doc_meta:
                        total_pages += doc_meta["page_count"]

            st.metric("Pages", total_pages)
            st.metric("Chunks", "N/A")  # Not available from File Search

    # Quick Upload / Corpus Creation
    if not st.session_state.reference_docs_uploaded:
        case_context = st.text_area(
            "Case Context",
            placeholder="Brief description of case or project...",
            height=120,
            key="case_context_sidebar",
            label_visibility="collapsed",
        )

        uploaded_refs = st.file_uploader(
            "Upload reference documents",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            key="corpus_upload_sidebar",
            label_visibility="collapsed",
            help="These documents form the knowledge base that Gemini uses to verify your document",
        )

        if uploaded_refs:
            if st.button(
                "Create Corpus",
                type="primary",
                use_container_width=True,
                key="create_corpus",
            ):
                with st.spinner("Creating reference library..."):
                    result = upload_reference_documents(uploaded_refs, case_context)

                    if result:
                        # Store corpus information in session state
                        st.session_state.store_id = result["store_id"]
                        st.session_state.reference_docs_uploaded = True
                        st.session_state.case_context = case_context
                        st.session_state.corpus_metadata = result.get("metadata", [])
                        st.session_state.corpus_just_created = True
                        # Force rerun to update sidebar status immediately
                        st.rerun()

    # Actions (if corpus is active)
    if st.session_state.reference_docs_uploaded:
        # Show one-time success message if corpus was just created
        if st.session_state.get("corpus_just_created", False):
            doc_count = (
                len(st.session_state.corpus_metadata)
                if st.session_state.corpus_metadata
                else 0
            )
            st.success(f"✅ Created! {doc_count} document(s) uploaded")
            st.session_state.corpus_just_created = False

        st.markdown("**Actions**")

        if st.button(
            "📄 View Library", key="view_docs_sidebar", use_container_width=True
        ):
            # Toggle the view library expanded state
            if "view_library_expanded" not in st.session_state:
                st.session_state.view_library_expanded = True
            else:
                st.session_state.view_library_expanded = (
                    not st.session_state.view_library_expanded
                )
            # Streamlit will automatically rerun when session state changes

        if st.button(
            "⚙️ Configure",
            key="config_sidebar",
            use_container_width=True,
            disabled=True,
            help="Configuration coming soon",
        ):
            # Show configuration options (disabled for now)
            pass

        if st.button(
            "🗑️ Clear Corpus",
            key="clear_sidebar",
            type="secondary",
            use_container_width=True,
        ):
            # Delete corpus from backend first
            if st.session_state.store_id:
                with st.spinner("Deleting corpus..."):
                    success = delete_corpus(st.session_state.store_id)
                    if success:
                        reset_corpus_state()
                        # Streamlit will automatically rerun when session state changes
                    else:
                        st.error(
                            "❌ Failed to delete corpus. Clearing local state only."
                        )
                        reset_corpus_state()
                        # Streamlit will automatically rerun when session state changes
            else:
                # No store_id, just reset state
                reset_corpus_state()
                # Streamlit will automatically rerun when session state changes

    # View Library Expander (show when toggled)
    if st.session_state.reference_docs_uploaded and st.session_state.get(
        "view_library_expanded", False
    ):
        st.markdown("---")
        with st.expander("Library Contents", expanded=True):
            if st.session_state.corpus_metadata:
                for idx, meta in enumerate(st.session_state.corpus_metadata):
                    # Handle both dict and object formats
                    filename = (
                        meta.get("filename")
                        if isinstance(meta, dict)
                        else getattr(meta, "filename", "Unknown")
                    )
                    doc_type = (
                        meta.get("document_type", "N/A")
                        if isinstance(meta, dict)
                        else getattr(meta, "document_type", "N/A")
                    )
                    summary = (
                        meta.get("summary", "N/A")
                        if isinstance(meta, dict)
                        else getattr(meta, "summary", "N/A")
                    )
                    file_size = (
                        meta.get("file_size_bytes", 0)
                        if isinstance(meta, dict)
                        else getattr(meta, "file_size_bytes", 0)
                    )
                    page_count = (
                        meta.get("page_count", 0)
                        if isinstance(meta, dict)
                        else getattr(meta, "page_count", 0)
                    )
                    keywords = (
                        meta.get("keywords", [])
                        if isinstance(meta, dict)
                        else getattr(meta, "keywords", [])
                    )

                    st.markdown(f"**{idx + 1}. {filename}**")
                    st.caption(f"📑 Type: {doc_type}")
                    st.caption(
                        f"📄 Pages: {page_count} | 💾 Size: {file_size / 1024:.1f} KB"
                    )
                    st.caption(f"📝 {summary}")
                    if keywords:
                        st.caption(f"🏷️ Keywords: {', '.join(keywords[:5])}")
                    if idx < len(st.session_state.corpus_metadata) - 1:
                        st.divider()
            else:
                st.info("No metadata available")

    st.markdown("</div>", unsafe_allow_html=True)


def render_corpus_management() -> None:
    """
    Render the corpus management expander panel.
    This is the main entry point for corpus UI, always visible at top of page.
    """

    # Dynamic label based on corpus status
    if st.session_state.reference_docs_uploaded:
        label = "🤖 AI Reference Corpus - ✅ Active"
        expanded_default = False  # Collapsed when active
    else:
        label = "🤖 AI Reference Corpus - ⚠️ Not Configured"
        expanded_default = False  # Let user expand when needed

    with st.expander(label, expanded=expanded_default):
        if st.session_state.reference_docs_uploaded:
            # Show active corpus UI
            render_active_corpus()
        else:
            # Show corpus creation form
            render_corpus_creation()
