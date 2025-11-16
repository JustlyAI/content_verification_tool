"""
Corpus Management UI Components for AI Verification
Freshfields-inspired compact sidebar design
"""

import streamlit as st
from .api_client import upload_reference_documents
from .state import reset_corpus_state


def render_corpus_creation() -> None:
    """Render corpus creation form (when no active corpus)"""
    st.markdown("Upload reference documents to enable AI verification")

    # Show clearer instructions
    st.info("📝 **Instructions:** Fill in both fields below to enable the button")

    case_context = st.text_area(
        "Case Context *",
        placeholder="Describe what you're verifying (e.g., 'Contract verification for Project X')",
        max_chars=500,
        help="Provide context to help AI understand the verification case",
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
    if not case_context or not reference_files:
        missing = []
        if not case_context:
            missing.append("Case Context")
        if not reference_files:
            missing.append("Reference Documents")
        st.warning(f"⚠️ Please provide: {', '.join(missing)}")

    if st.button(
        "Create Reference Library",
        disabled=not reference_files or not case_context,
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

                st.success(
                    f"✅ Uploaded {result['documents_uploaded']} reference documents"
                )
                st.info(f"📦 Store ID: `{result['store_id']}`")

                # Show metadata
                if result.get("metadata"):
                    with st.expander("View Document Metadata"):
                        for meta in result["metadata"]:
                            st.markdown(f"**{meta['filename']}**")
                            st.caption(f"Type: {meta['document_type']}")
                            st.caption(f"Summary: {meta['summary']}")

                st.rerun()


def render_active_corpus() -> None:
    """Render active corpus information and management"""
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
            st.rerun()


def render_corpus_sidebar() -> None:
    """
    Render the corpus sidebar with Freshfields styling
    Compact design for always-visible sidebar
    """
    st.markdown('<div class="ff-sidebar-content">', unsafe_allow_html=True)

    st.markdown("## Reference Corpus")
    st.info(
        "📚 **Knowledge Base** - Upload reference documents as grounding for verification"
    )

    # Status
    if st.session_state.reference_docs_uploaded:
        st.success("✓ Active & Gemini-Ready")
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
            st.metric("Storage", "0 MB")  # TODO: Calculate from metadata
        with col2:
            st.metric("Pages", "0")  # TODO: Calculate from metadata
            st.metric("Chunks", "0")  # TODO: Get from backend

        st.markdown("---")

    # Quick Upload / Corpus Creation
    if not st.session_state.reference_docs_uploaded:
        case_context = st.text_area(
            "Case Context",
            placeholder="Brief description of case or project...",
            height=80,
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

        if uploaded_refs and case_context:
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
                        st.success(f"✅ {len(uploaded_refs)} file(s) uploaded")
                        st.rerun()
        elif uploaded_refs:
            st.caption("⚠️ Add case context to continue")

        st.markdown("---")

    # Actions (if corpus is active)
    if st.session_state.reference_docs_uploaded:
        st.markdown("**Actions**")

        if st.button(
            "📄 View Library", key="view_docs_sidebar", use_container_width=True
        ):
            # Show modal or expander with corpus details
            pass

        if st.button("⚙️ Configure", key="config_sidebar", use_container_width=True):
            # Show configuration options
            pass

        if st.button(
            "🗑️ Clear Corpus",
            key="clear_sidebar",
            type="secondary",
            use_container_width=True,
        ):
            reset_corpus_state()
            st.rerun()

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
