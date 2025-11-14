"""
Design Mockup 3: Minimalist Cards
Clean card-based design with collapsible results section
"""

import streamlit as st

st.set_page_config(
    page_title="Design 3: Minimalist Cards",
    page_icon="📋",
    layout="wide",
)

# Minimal header
st.title("📋 Content Verification Tool")
st.caption("Design 3: Minimalist Card Layout")
st.divider()

# Main tabs
tab1, tab2 = st.tabs(["📚 Corpus", "✅ Verification"])

# ==================== TAB 1: CORPUS ====================
with tab1:
    st.header("Reference Corpus")

    # Status banner
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.success("✅ Corpus Active | 5 documents | 127 pages")
    with col2:
        st.button("➕ Add Documents", use_container_width=True)
    with col3:
        st.button("⚙️ Settings", use_container_width=True)

    st.divider()

    # Two-section layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Upload card
        with st.container():
            st.subheader("Upload Reference Documents")

            uploaded_files = st.file_uploader(
                "Drop files here or click to browse",
                type=["pdf", "docx"],
                accept_multiple_files=True,
                key="corpus_upload_files",
                help="Supported: PDF, DOCX"
            )

            if uploaded_files:
                st.info(f"📦 {len(uploaded_files)} file(s) selected")
                st.button("Upload & Process", type="primary", use_container_width=True)

        st.divider()

        # Document library
        st.subheader("Document Library")

        # Simple search
        st.text_input("🔍 Search documents", placeholder="Type to search...", label_visibility="collapsed")

        st.divider()

        # Document list - clean card style
        for idx, doc in enumerate([
            ("Case Law 2023.pdf", "45 pages", "5.2 MB", "Nov 10, 2025", "✅"),
            ("Regulations.docx", "23 pages", "1.8 MB", "Nov 9, 2025", "✅"),
            ("Precedent Analysis.pdf", "59 pages", "7.3 MB", "Nov 8, 2025", "✅"),
        ]):
            with st.container():
                col_a, col_b, col_c, col_d = st.columns([3, 2, 2, 1])
                with col_a:
                    st.markdown(f"**{doc[0]}**")
                with col_b:
                    st.caption(f"{doc[1]} • {doc[2]}")
                with col_c:
                    st.caption(f"Added {doc[3]}")
                with col_d:
                    st.markdown(f"{doc[4]}")

                if st.checkbox("Show details", key=f"details_{idx}"):
                    st.caption("Status: Indexed and ready for verification")
                    st.caption("Embedding model: text-embedding-004")
                    col_x, col_y = st.columns(2)
                    with col_x:
                        st.button("🔄 Reindex", key=f"reindex_{idx}", use_container_width=True)
                    with col_y:
                        st.button("🗑️ Remove", key=f"remove_{idx}", use_container_width=True)

            st.divider()

    with col2:
        # Corpus configuration card
        with st.container():
            st.subheader("Configuration")

            st.text_area(
                "Case Context",
                placeholder="Optional: Add case-specific context...",
                height=120,
                help="Helps AI understand the verification context"
            )

            st.divider()

            st.selectbox(
                "AI Model",
                ["Gemini 1.5 Pro", "Gemini 1.5 Flash", "GPT-4"],
                help="Model for verification"
            )

            st.slider(
                "Confidence Threshold",
                0.0, 1.0, 0.7, 0.05,
                help="Minimum score for verification"
            )

            st.divider()

            st.button("💾 Save", type="primary", use_container_width=True)

        st.divider()

        # Quick stats card
        with st.container():
            st.subheader("Statistics")
            st.metric("Total Documents", "5")
            st.metric("Total Pages", "127")
            st.metric("Storage", "23.4 MB")
            st.metric("Last Updated", "2 hours ago")

        st.divider()

        # Actions card
        with st.container():
            st.subheader("Actions")
            st.button("🔄 Rebuild Index", use_container_width=True)
            st.button("📥 Export Corpus", use_container_width=True)
            st.button("🗑️ Clear All", type="secondary", use_container_width=True)

# ==================== TAB 2: VERIFICATION ====================
with tab2:
    st.header("Document Verification")

    # Process cards horizontally
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container():
            st.markdown("### 1️⃣ Upload")
            uploaded_doc = st.file_uploader(
                "Document",
                type=["pdf", "docx"],
                key="doc_verify",
                label_visibility="collapsed"
            )
            if uploaded_doc:
                st.success(f"✅ Ready")
                st.button("Process", type="primary", use_container_width=True, key="proc")

    with col2:
        with st.container():
            st.markdown("### 2️⃣ Chunking")
            chunking = st.radio(
                "Mode",
                ["Paragraph", "Sentence"],
                label_visibility="collapsed",
                key="chunk_mode"
            )
            st.caption("Selected: " + chunking)

    with col3:
        with st.container():
            st.markdown("### 3️⃣ Verify")
            st.info("Corpus: Active")
            st.button("▶️ Verify", type="primary", use_container_width=True, key="run_verify")

    with col4:
        with st.container():
            st.markdown("### 4️⃣ Export")
            output = st.selectbox(
                "Format",
                ["Word (L)", "Word (P)", "Excel", "CSV", "JSON"],
                label_visibility="collapsed"
            )
            st.button("Generate", use_container_width=True, disabled=True)
            st.button("Download", use_container_width=True, disabled=True)

    st.divider()

    # Results section - collapsible and clean
    st.subheader("Results")

    # Results status bar
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Chunks", "124")
    with col2:
        st.metric("Verified", "89")
    with col3:
        st.metric("Confidence", "8.2/10")
    with col4:
        st.metric("Time", "45s")
    with col5:
        st.metric("Status", "✅ Done")

    st.divider()

    # Results view selector
    view_mode = st.segmented_control(
        "View",
        ["Summary", "Table", "Analysis", "Export"],
        default="Summary",
        label_visibility="collapsed"
    )

    st.divider()

    if view_mode == "Summary":
        # Clean summary view
        col1, col2 = st.columns(2)

        with col1:
            # Verification breakdown
            st.markdown("**Verification Status**")

            with st.container():
                st.markdown("🟢 **High Confidence (8-10)**")
                st.progress(0.54)
                st.caption("67 chunks (54%)")

            with st.container():
                st.markdown("🟡 **Medium Confidence (5-7)**")
                st.progress(0.18)
                st.caption("22 chunks (18%)")

            with st.container():
                st.markdown("🔴 **Low/Unverified**")
                st.progress(0.28)
                st.caption("35 chunks (28%) - Review needed")

        with col2:
            # Top issues
            st.markdown("**Items Needing Review (35)**")

            with st.expander("⚠️ Page 2, Item 4", expanded=True):
                st.markdown("*Furthermore, the analysis indicates that...*")
                st.caption("**Issue:** Low confidence (4.2/10)")
                st.caption("**Action:** Manual review recommended")
                st.button("View Details", key="details1", use_container_width=True)

            with st.expander("⚠️ Page 3, Item 7"):
                st.markdown("*The plaintiff contends...*")
                st.caption("**Issue:** No reference match")
                st.button("View Details", key="details2", use_container_width=True)

            with st.expander("⚠️ Page 5, Item 2"):
                st.markdown("*According to the statute...*")
                st.caption("**Issue:** Multiple conflicting sources")
                st.button("View Details", key="details3", use_container_width=True)

    elif view_mode == "Table":
        # Clean table view
        st.markdown("**All Verification Results**")

        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            st.selectbox("Filter by status", ["All", "Verified", "Unverified", "Low Confidence"], key="filter_status")
        with col2:
            st.selectbox("Filter by page", ["All Pages"] + [f"Page {i}" for i in range(1, 11)], key="filter_page")
        with col3:
            st.text_input("Search text", placeholder="🔍 Search...", key="search_text")

        st.divider()

        # Data table
        st.dataframe(
            {
                "Page": [1, 1, 1, 2, 2, 2, 3, 3, 3, 4],
                "Item": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1],
                "Text": [
                    "In accordance with statute...",
                    "The court held that...",
                    "This provision complies...",
                    "Furthermore, the analysis...",
                    "As stated in precedent...",
                    "The defendant argues...",
                    "Section 42 provides...",
                    "Historical context shows...",
                    "The ruling established...",
                    "Pursuant to regulations..."
                ],
                "Status": ["✅", "✅", "✅", "⚠️", "✅", "⚠️", "✅", "✅", "✅", "✅"],
                "Score": [8.5, 9.1, 9.2, 4.2, 8.8, 3.9, 9.4, 8.7, 8.9, 9.0],
                "Source": [
                    "Regulations.docx:5",
                    "Case Law 2023.pdf:12",
                    "Case Law 2023.pdf:12",
                    "—",
                    "Precedent.pdf:34",
                    "—",
                    "Regulations.docx:8",
                    "Precedent.pdf:67",
                    "Case Law 2023.pdf:45",
                    "Regulations.docx:12"
                ]
            },
            use_container_width=True,
            hide_index=True,
            height=500
        )

        st.caption("Click any row for detailed verification information")

    elif view_mode == "Analysis":
        # Analysis view
        st.markdown("**Verification Analysis**")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Coverage by Page**")
            st.bar_chart({
                "Page 1": 92,
                "Page 2": 67,
                "Page 3": 89,
                "Page 4": 95,
                "Page 5": 71
            })

        with col2:
            st.markdown("**Confidence Distribution**")
            st.bar_chart({
                "High (8-10)": 67,
                "Medium (5-7)": 22,
                "Low (<5)": 0,
                "Unverified": 35
            })

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Top Sources**")
            st.dataframe(
                {
                    "Source": [
                        "Case Law 2023.pdf",
                        "Regulations.docx",
                        "Precedent.pdf"
                    ],
                    "Citations": [45, 32, 12],
                    "Avg Score": [8.9, 9.2, 8.5]
                },
                hide_index=True,
                use_container_width=True
            )

        with col2:
            st.markdown("**Processing Stats**")
            st.dataframe(
                {
                    "Metric": ["Total Time", "Avg per Chunk", "API Calls", "Cache Hits"],
                    "Value": ["45s", "0.36s", "124", "89"]
                },
                hide_index=True,
                use_container_width=True
            )

    elif view_mode == "Export":
        # Export options
        st.markdown("**Export Verification Results**")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("Select export format and options:")

            export_format = st.selectbox(
                "Format",
                ["Word Document (Landscape)", "Word Document (Portrait)", "Excel Spreadsheet", "CSV File", "JSON Data"]
            )

            st.markdown("**Include:**")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.checkbox("Verified items", value=True)
            with col_b:
                st.checkbox("Unverified items", value=True)
            with col_c:
                st.checkbox("Metadata", value=True)

            col_a, col_b = st.columns(2)
            with col_a:
                st.checkbox("Confidence scores", value=True)
            with col_b:
                st.checkbox("Source citations", value=True)

            st.divider()

            st.button("📄 Generate Export", type="primary", use_container_width=True)

        with col2:
            st.markdown("**Export Preview**")
            st.info("Format: " + export_format)
            st.metric("Total Items", "124")
            st.metric("File Size", "~2.3 MB")

st.divider()
st.caption("Mockup Design 3: Minimalist Cards | Clean and focused interface")
