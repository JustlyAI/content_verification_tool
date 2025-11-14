"""
Design Mockup 2: Split Screen Workflow
Side-by-side tabs with expandable results panel on right
"""

import streamlit as st

st.set_page_config(
    page_title="Design 2: Split Screen",
    page_icon="📋",
    layout="wide",
)

# Header
st.title("📋 Content Verification Tool")
st.caption("Design 2: Split Screen Workflow")
st.divider()

# Create main tabs
tab1, tab2 = st.tabs(["📚 Corpus", "✅ Verification"])

# ==================== TAB 1: CORPUS ====================
with tab1:
    # Full-width layout for corpus
    col1, col2 = st.columns([3, 2])

    with col1:
        st.header("📚 Reference Document Library")

        # Upload section
        with st.expander("➕ Add New Documents", expanded=True):
            st.markdown("Upload reference documents for AI verification")

            uploaded_files = st.file_uploader(
                "Drag and drop files here",
                type=["pdf", "docx"],
                accept_multiple_files=True,
                key="corpus_files"
            )

            if uploaded_files:
                for file in uploaded_files:
                    st.text(f"📄 {file.name} ({file.size / 1024:.1f} KB)")

            col_a, col_b = st.columns(2)
            with col_a:
                st.button("🚀 Upload All", type="primary", use_container_width=True)
            with col_b:
                st.button("🗑️ Clear Selection", use_container_width=True)

        st.divider()

        # Document list
        st.subheader("Current Documents (5)")

        # Filters
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.selectbox("Sort by", ["Date Added", "Name", "Size"], key="sort")
        with col_b:
            st.text_input("Search", placeholder="🔍 Search documents...")
        with col_c:
            st.selectbox("Filter", ["All", "Indexed", "Processing"], key="filter")

        st.divider()

        # Document cards
        for i, doc in enumerate([
            ("Case Law 2023.pdf", "45 pages", "5.2 MB", "2025-11-10"),
            ("Regulations.docx", "23 pages", "1.8 MB", "2025-11-09"),
            ("Precedent Analysis.pdf", "59 pages", "7.3 MB", "2025-11-08")
        ]):
            with st.container():
                col_a, col_b, col_c = st.columns([3, 2, 1])
                with col_a:
                    st.markdown(f"**📄 {doc[0]}**")
                with col_b:
                    st.text(f"{doc[1]} | {doc[2]}")
                with col_c:
                    st.button("🗑️", key=f"delete_{i}", help="Delete document")
                st.caption(f"Added: {doc[3]} | Status: ✅ Indexed")
            st.divider()

    with col2:
        st.header("⚙️ Configuration")

        # Corpus status
        st.success("✅ **Corpus Active**")

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Total Documents", "5")
        with col_b:
            st.metric("Total Pages", "127")

        st.divider()

        # Case context
        st.subheader("Case Context")
        case_context = st.text_area(
            "Provide context for better verification",
            placeholder="Enter case background, relevant statutes, key arguments...",
            height=150,
            label_visibility="collapsed"
        )
        st.caption("Optional: Helps AI understand verification context")

        st.divider()

        # Model settings
        st.subheader("Model Configuration")
        st.selectbox("AI Model", ["Gemini 1.5 Pro", "Gemini 1.5 Flash", "GPT-4"])
        st.slider("Min Confidence", 0.0, 1.0, 0.7, 0.05)
        st.number_input("Max Results per Chunk", 1, 10, 3)

        st.divider()

        # Action buttons
        st.button("💾 Save Configuration", type="primary", use_container_width=True)
        st.button("🔄 Rebuild Index", use_container_width=True)
        st.button("🗑️ Clear All Documents", type="secondary", use_container_width=True)

# ==================== TAB 2: VERIFICATION ====================
with tab2:
    # Split into workflow (left) and results (right)
    workflow_col, results_col = st.columns([2, 3])

    with workflow_col:
        st.header("Verification Workflow")

        # Step 1: Upload
        with st.container():
            st.markdown("### Step 1: Upload Document")
            uploaded_doc = st.file_uploader(
                "Document to verify",
                type=["pdf", "docx"],
                key="verify_doc",
                label_visibility="collapsed"
            )
            if uploaded_doc:
                st.success(f"✅ {uploaded_doc.name}")
                st.button("📤 Process", type="primary", use_container_width=True, key="process_btn")

        st.divider()

        # Step 2: Chunking
        with st.container():
            st.markdown("### Step 2: Chunking Mode")
            chunking = st.radio(
                "Mode",
                ["📝 Paragraph-level", "📄 Sentence-level"],
                label_visibility="collapsed"
            )
            st.caption("Paragraph mode groups related content; Sentence mode provides granular verification")

        st.divider()

        # Step 3: Verify
        with st.container():
            st.markdown("### Step 3: AI Verification")

            if True:  # Mock corpus active
                st.info("🤖 Corpus ready for verification")
                st.button("▶️ Run Verification", type="primary", use_container_width=True, key="verify_btn")
            else:
                st.warning("⚠️ No corpus available. Upload reference documents first.")

        st.divider()

        # Step 4: Export
        with st.container():
            st.markdown("### Step 4: Export Results")
            output = st.selectbox(
                "Output format",
                ["Word (Landscape)", "Word (Portrait)", "Excel", "CSV", "JSON"],
                label_visibility="collapsed"
            )
            st.button("📄 Generate", type="primary", use_container_width=True, key="generate_btn", disabled=True)
            st.button("⬇️ Download", use_container_width=True, key="download_btn", disabled=True)

        st.divider()

        # Quick actions
        st.markdown("### Quick Actions")
        st.button("🔄 Reset Workflow", use_container_width=True)
        st.button("📋 Copy Settings", use_container_width=True)

    with results_col:
        st.header("📊 Results Panel")

        # Results tabs
        result_view = st.radio(
            "View",
            ["📈 Overview", "📋 Detailed Table", "🔍 By Confidence", "📄 By Page"],
            horizontal=True,
            label_visibility="collapsed"
        )

        st.divider()

        if result_view == "📈 Overview":
            # Overview metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Chunks", "124")
            with col2:
                st.metric("Verified", "89", delta="71.8%")
            with col3:
                st.metric("Confidence", "8.2", delta="High")
            with col4:
                st.metric("Time", "45s")

            st.divider()

            # Distribution chart
            st.markdown("**Verification Distribution**")
            st.bar_chart({"High (8-10)": 67, "Medium (5-7)": 22, "Low (<5)": 0})

            st.divider()

            # Flagged items
            st.markdown("**Items Requiring Review (35)**")

            with st.expander("⚠️ Page 2, Item 4 - Low confidence (4.2)", expanded=True):
                st.markdown("> Furthermore, the analysis indicates that...")
                st.markdown("**Issue:** No strong reference match found")
                st.markdown("**Suggestion:** Manual review recommended")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.button("✅ Mark Verified", key="mark1", use_container_width=True)
                with col_b:
                    st.button("🔍 Show Sources", key="sources1", use_container_width=True)

            with st.expander("⚠️ Page 3, Item 7 - Unverified"):
                st.markdown("> The plaintiff contends...")
                st.markdown("**Issue:** No reference match")
                st.markdown("**Action:** Add to manual review list")

        elif result_view == "📋 Detailed Table":
            # Full table view
            st.dataframe(
                {
                    "Page": [1, 1, 1, 2, 2, 2, 3, 3],
                    "Item": [1, 2, 3, 1, 2, 3, 1, 2],
                    "Text": [
                        "In accordance with statute...",
                        "The court held that...",
                        "This provision complies...",
                        "Furthermore, the analysis...",
                        "As stated in precedent...",
                        "The defendant argues...",
                        "Section 42 provides...",
                        "Historical context shows..."
                    ],
                    "Status": ["✅", "✅", "✅", "⚠️", "✅", "⚠️", "✅", "✅"],
                    "Score": [8.5, 9.1, 9.2, 4.2, 8.8, 3.9, 9.4, 8.7],
                    "Source": [
                        "Regulations.docx:5",
                        "Case Law 2023.pdf:12",
                        "Case Law 2023.pdf:12",
                        "—",
                        "Precedent.pdf:34",
                        "—",
                        "Regulations.docx:8",
                        "Precedent.pdf:67"
                    ]
                },
                use_container_width=True,
                hide_index=True,
                height=400
            )

            st.caption("Click any row to see detailed verification information")

        elif result_view == "🔍 By Confidence":
            # Group by confidence levels
            st.markdown("### 🟢 High Confidence (67 chunks)")
            st.progress(0.54)
            with st.expander("View high confidence items"):
                st.markdown("Chunks with scores 8.0-10.0")

            st.markdown("### 🟡 Medium Confidence (22 chunks)")
            st.progress(0.18)
            with st.expander("View medium confidence items"):
                st.markdown("Chunks with scores 5.0-7.9")

            st.markdown("### 🔴 Low Confidence (0 chunks)")
            st.progress(0.0)

            st.markdown("### ⚪ Unverified (35 chunks)")
            st.progress(0.28)
            with st.expander("View unverified items", expanded=True):
                st.markdown("No reference match found - requires manual review")

        elif result_view == "📄 By Page":
            # Group by page
            for page in range(1, 4):
                with st.expander(f"Page {page} (12 chunks)", expanded=(page == 1)):
                    st.markdown(f"**Verification:** 9/12 verified")
                    st.progress(0.75)
                    st.caption("3 items need review")

st.divider()
st.caption("Mockup Design 2: Split Screen | Workflow + Results side-by-side")
