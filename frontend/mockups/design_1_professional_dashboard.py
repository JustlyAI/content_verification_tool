"""
Design Mockup 1: Professional Dashboard
Two-tab layout with metrics, modern cards, and structured results pane
"""

import streamlit as st

st.set_page_config(
    page_title="Design 1: Professional Dashboard",
    page_icon="📋",
    layout="wide",
)

# Header
st.title("📋 Content Verification Tool")
st.caption("Design 1: Professional Dashboard Style")
st.divider()

# Create tabs
tab1, tab2 = st.tabs(["📚 Corpus Management", "✅ Document Verification"])

# ==================== TAB 1: CORPUS ====================
with tab1:
    st.header("AI Reference Corpus")

    # Metrics row at top
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Documents", "5", delta="2 new")
    with col2:
        st.metric("Total Pages", "127")
    with col3:
        st.metric("Storage Used", "23.4 MB", delta="5.2 MB")
    with col4:
        st.metric("Status", "Active", delta="Ready")

    st.divider()

    # Main content in cards
    col1, col2 = st.columns([2, 1])

    with col1:
        # Upload card
        with st.container():
            st.subheader("📤 Upload Reference Documents")
            st.markdown("Upload documents that will be used for verification")

            uploaded_files = st.file_uploader(
                "Choose files",
                type=["pdf", "docx"],
                accept_multiple_files=True,
                key="corpus_upload",
                label_visibility="collapsed",
            )

            if uploaded_files:
                st.info(f"Selected {len(uploaded_files)} file(s)")
                st.button(
                    "🚀 Process & Add to Corpus",
                    type="primary",
                    use_container_width=True,
                )

        st.divider()

        # Current documents
        with st.container():
            st.subheader("📚 Current Corpus Documents")

            # Sample data in a table
            st.dataframe(
                {
                    "Document": [
                        "Case Law 2023.pdf",
                        "Regulations.docx",
                        "Precedent Analysis.pdf",
                    ],
                    "Pages": [45, 23, 59],
                    "Size": ["5.2 MB", "1.8 MB", "7.3 MB"],
                    "Added": ["2025-11-10", "2025-11-09", "2025-11-08"],
                    "Status": ["✅ Indexed", "✅ Indexed", "✅ Indexed"],
                },
                use_container_width=True,
                hide_index=True,
            )

    with col2:
        # Settings card
        with st.container():
            st.subheader("⚙️ Corpus Settings")

            case_context = st.text_area(
                "Case Context",
                placeholder="Enter relevant case context...",
                height=150,
                help="Provide context to improve verification accuracy",
            )

            st.selectbox(
                "Verification Model",
                ["Gemini 1.5 Pro", "Gemini 1.5 Flash", "GPT-4"],
                help="Select the AI model for verification",
            )

            st.slider(
                "Confidence Threshold",
                0.0,
                1.0,
                0.7,
                help="Minimum confidence score for verification",
            )

            st.divider()

            st.button("💾 Save Settings", type="primary", use_container_width=True)
            st.button("🗑️ Clear Corpus", type="secondary", use_container_width=True)

# ==================== TAB 2: VERIFICATION ====================
with tab2:
    st.header("Document Verification")

    # Two-column layout
    left_col, right_col = st.columns([1, 1])

    with left_col:
        # Upload section
        st.subheader("1️⃣ Upload Document")
        uploaded_doc = st.file_uploader(
            "Choose document to verify", type=["pdf", "docx"], key="doc_upload"
        )

        if uploaded_doc:
            st.success(f"📄 {uploaded_doc.name} ready")
            st.button("🚀 Process Document", type="primary", use_container_width=True)

        st.divider()

        # Splitting mode
        st.subheader("2️⃣ Splitting mode")
        chunking = st.radio(
            "Select mode",
            ["Paragraph", "Sentence"],
            horizontal=True,
            label_visibility="collapsed",
        )

        st.divider()

        # AI Verification
        st.subheader("3️⃣ AI Verification")
        col1, col2 = st.columns(2)
        with col1:
            st.info("Corpus: Active")
        with col2:
            st.button("🤖 Verify Now", type="primary", use_container_width=True)

        st.divider()

        # Output format
        st.subheader("4️⃣ Output Format")
        output_format = st.selectbox(
            "Select format",
            ["Word (Landscape)", "Word (Portrait)", "Excel", "CSV", "JSON"],
            label_visibility="collapsed",
        )

        st.button("📄 Generate Document", type="primary", use_container_width=True)
        st.button(
            "⬇️ Download", type="secondary", use_container_width=True, disabled=True
        )

    with right_col:
        # Results pane
        st.subheader("📊 Verification Results")

        # Tabs for results view
        results_tab1, results_tab2 = st.tabs(["Summary", "Detailed"])

        with results_tab1:
            # Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Chunks", "124")
            with col2:
                st.metric("Verified", "89", delta="71.8%")
            with col3:
                st.metric("Avg Confidence", "8.2/10")

            st.divider()

            # Confidence distribution
            st.markdown("**Confidence Distribution**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🟢 High (8-10)", "67")
            with col2:
                st.metric("🟡 Medium (5-7)", "22")
            with col3:
                st.metric("🔴 Low (<5)", "0")

            st.divider()

            # Recent verifications
            st.markdown("**Recent Verifications**")
            with st.expander("Page 1, Item 3 - Verified ✅", expanded=True):
                st.markdown("**Text:** This provision complies with Section 42...")
                st.markdown("**Source:** Case Law 2023.pdf, Page 12")
                st.markdown("**Confidence:** 9.2/10")

            with st.expander("Page 1, Item 4 - Unverified ⚠️"):
                st.markdown("**Text:** The defendant argues that...")
                st.markdown("**Reason:** No matching reference found")
                st.markdown("**Suggestion:** Review manually")

        with results_tab2:
            # Detailed table view
            st.dataframe(
                {
                    "Page": [1, 1, 1, 2, 2],
                    "Item": [1, 2, 3, 1, 2],
                    "Text": [
                        "In accordance with statute...",
                        "The court held that...",
                        "This provision complies...",
                        "Furthermore, the analysis...",
                        "As stated in precedent...",
                    ],
                    "Verified": ["✅", "✅", "✅", "⚠️", "✅"],
                    "Score": [8.5, 9.1, 9.2, 4.2, 8.8],
                    "Source": [
                        "Regulations.docx:5",
                        "Case Law 2023.pdf:12",
                        "Case Law 2023.pdf:12",
                        "—",
                        "Precedent.pdf:34",
                    ],
                },
                use_container_width=True,
                hide_index=True,
            )

st.divider()
st.caption("Mockup Design 1: Professional Dashboard | Clean metrics-driven interface")
