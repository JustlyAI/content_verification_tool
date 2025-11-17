"""
Session State Management for Content Verification Tool
"""

import streamlit as st


def init_session_state() -> None:
    """Initialize all session state variables"""

    # Document upload state
    if "document_id" not in st.session_state:
        st.session_state.document_id = None
    if "document_info" not in st.session_state:
        st.session_state.document_info = None
    if "upload_in_progress" not in st.session_state:
        st.session_state.upload_in_progress = False
    if "last_generated" not in st.session_state:
        st.session_state.last_generated = None

    # AI Verification state
    if "store_id" not in st.session_state:
        st.session_state.store_id = None
    if "reference_docs_uploaded" not in st.session_state:
        st.session_state.reference_docs_uploaded = False
    if "case_context" not in st.session_state:
        st.session_state.case_context = None
    if "corpus_metadata" not in st.session_state:
        st.session_state.corpus_metadata = None
    if "corpus_creation_in_progress" not in st.session_state:
        st.session_state.corpus_creation_in_progress = False
    if "verification_complete" not in st.session_state:
        st.session_state.verification_complete = False
    if "verification_results" not in st.session_state:
        st.session_state.verification_results = None
    if "verification_in_progress" not in st.session_state:
        st.session_state.verification_in_progress = False

    # Processing state
    if "splitting_mode" not in st.session_state:
        st.session_state.splitting_mode = "paragraph"


def reset_document_state() -> None:
    """Reset document-related session state"""
    st.session_state.document_id = None
    st.session_state.document_info = None
    st.session_state.last_generated = None
    st.session_state.upload_in_progress = False


def reset_corpus_state() -> None:
    """Reset corpus-related session state"""
    st.session_state.store_id = None
    st.session_state.reference_docs_uploaded = False
    st.session_state.case_context = None
    st.session_state.corpus_metadata = None
    st.session_state.corpus_creation_in_progress = False


def reset_verification_state() -> None:
    """Reset verification-related session state"""
    st.session_state.verification_complete = False
    st.session_state.verification_results = None
    st.session_state.verification_in_progress = False
    st.session_state.splitting_mode = "paragraph"


def reset_all_state() -> None:
    """Reset all session state (for Start Over button)"""
    reset_document_state()
    reset_corpus_state()
    reset_verification_state()
