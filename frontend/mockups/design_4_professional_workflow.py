"""
Design Mockup 4: Professional Workflow
Next-level UX with visual progress tracking, enhanced results, and delightful interactions
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Content Verification Tool",
    page_icon="📋",
    layout="wide",
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Main container padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Progress step styling */
    .step-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 2rem 0;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Card styling */
    .workflow-card {
        padding: 1.5rem;
        border-radius: 8px;
        background: white;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }

    .workflow-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102,126,234,0.2);
    }

    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    .status-active { background: #10b981; color: white; }
    .status-pending { background: #f59e0b; color: white; }
    .status-inactive { background: #6b7280; color: white; }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
    }

    /* Result cards */
    .result-card {
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        background: #f9fafb;
        margin-bottom: 0.5rem;
    }

    .result-card.verified {
        border-left-color: #10b981;
    }

    .result-card.unverified {
        border-left-color: #ef4444;
    }

    .result-card.review {
        border-left-color: #f59e0b;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1 style='text-align: center; color: #667eea;'>📋 Content Verification Tool</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6b7280; font-size: 1.1rem;'>AI-Powered Legal Document Verification Workflow</p>", unsafe_allow_html=True)

st.divider()

# ==================== VISUAL WORKFLOW PROGRESS ====================
st.markdown("### 🎯 Workflow Progress")

# Progress stepper
col1, col2, col3, col4 = st.columns(4)

with col1:
    if True:  # Corpus configured
        st.markdown("✅ **Step 1: Corpus**")
        st.caption("Reference library ready")
    else:
        st.markdown("⚪ **Step 1: Corpus**")
        st.caption("Configure references")

with col2:
    if True:  # Document uploaded
        st.markdown("✅ **Step 2: Upload**")
        st.caption("Document ready")
    else:
        st.markdown("⚪ **Step 2: Upload**")
        st.caption("Upload document")

with col3:
    if True:  # Verification complete
        st.markdown("✅ **Step 3: Verify**")
        st.caption("AI analysis done")
    else:
        st.markdown("🔄 **Step 3: Verify**")
        st.caption("Run verification")

with col4:
    if False:  # Export ready
        st.markdown("⚪ **Step 4: Export**")
        st.caption("Generate output")
    else:
        st.markdown("✅ **Step 4: Export**")
        st.caption("Download results")

st.divider()

# ==================== MAIN TABS ====================
tab1, tab2, tab3 = st.tabs(["📚 Reference Corpus", "✅ Verification Workflow", "📊 Results Dashboard"])

# ==================== TAB 1: REFERENCE CORPUS ====================
with tab1:
    # Status Banner with Metrics
    if True:  # Corpus active
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                label="📦 Status",
                value="Active",
                delta="Ready for verification",
                delta_color="normal"
            )
        with col2:
            st.metric(
                label="📄 Documents",
                value="5",
                delta="+2 this week"
            )
        with col3:
            st.metric(
                label="📑 Total Pages",
                value="127",
                delta="45 from contracts"
            )
        with col4:
            st.metric(
                label="💾 Storage",
                value="23.4 MB",
                delta="8.2 MB free"
            )
    else:
        st.info("⚠️ **No Active Corpus** - Upload reference documents to enable AI verification")

    st.divider()

    # Two-column layout
    col_main, col_side = st.columns([2.5, 1.5])

    with col_main:
        # Document Library with Enhanced Cards
        st.subheader("📚 Document Library")

        # Search and filters
        col_search, col_filter = st.columns([3, 1])
        with col_search:
            st.text_input("🔍 Search documents", placeholder="Type to search...", label_visibility="collapsed")
        with col_filter:
            st.selectbox("Filter", ["All Types", "Contracts", "Regulations", "Case Law"], label_visibility="collapsed")

        st.divider()

        # Document cards with enhanced styling
        for idx, doc in enumerate([
            ("Contract_2024.pdf", "Legal Contract", "45 pages", "5.2 MB", "Nov 10, 2025", "Active", "#10b981"),
            ("Regulations.docx", "Regulatory", "23 pages", "1.8 MB", "Nov 9, 2025", "Active", "#10b981"),
            ("Case_Law.pdf", "Precedent", "59 pages", "7.3 MB", "Nov 8, 2025", "Active", "#10b981"),
            ("Analysis_Draft.pdf", "Analysis", "32 pages", "3.1 MB", "Nov 7, 2025", "Processing", "#f59e0b"),
        ]):
            with st.container():
                col_icon, col_info, col_meta, col_status, col_action = st.columns([0.5, 2, 1.5, 1, 1])

                with col_icon:
                    if doc[1] == "Legal Contract":
                        st.markdown("📄")
                    elif doc[1] == "Regulatory":
                        st.markdown("📋")
                    elif doc[1] == "Precedent":
                        st.markdown("⚖️")
                    else:
                        st.markdown("📊")

                with col_info:
                    st.markdown(f"**{doc[0]}**")
                    st.caption(f"Type: {doc[1]}")

                with col_meta:
                    st.caption(f"📄 {doc[2]} • 💾 {doc[3]}")
                    st.caption(f"📅 {doc[4]}")

                with col_status:
                    if doc[5] == "Active":
                        st.markdown(f"<span class='status-badge status-active'>✅ {doc[5]}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span class='status-badge status-pending'>🔄 {doc[5]}</span>", unsafe_allow_html=True)

                with col_action:
                    if st.button("⚙️", key=f"doc_settings_{idx}", help="Document settings"):
                        pass

                # Expandable details
                with st.expander("View Details", expanded=False):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.caption("**Summary:**")
                        st.info("This contract outlines the terms of service agreement between parties...")
                        st.caption("**Keywords:**")
                        st.markdown("`liability` `indemnification` `termination` `confidentiality`")
                    with col_b:
                        st.caption("**Indexing Status:**")
                        st.success("✅ Fully indexed and searchable")
                        st.caption("**Embedding Model:**")
                        st.code("text-embedding-004", language="text")
                        col_x, col_y = st.columns(2)
                        with col_x:
                            st.button("🔄 Reindex", key=f"reindex_{idx}", use_container_width=True)
                        with col_y:
                            st.button("🗑️ Remove", key=f"remove_{idx}", use_container_width=True, type="secondary")

                st.divider()

    with col_side:
        # Quick Actions Card
        with st.container():
            st.subheader("⚡ Quick Actions")

            # Upload new documents
            st.markdown("**Add Documents**")
            uploaded_files = st.file_uploader(
                "Drop files here",
                type=["pdf", "docx"],
                accept_multiple_files=True,
                key="corpus_upload",
                label_visibility="collapsed"
            )

            if uploaded_files:
                st.success(f"✅ {len(uploaded_files)} file(s) selected")
                st.button("📤 Upload & Process", type="primary", use_container_width=True)

            st.divider()

            # Configuration
            st.markdown("**Configuration**")
            st.selectbox(
                "AI Model",
                ["Gemini 2.5 Flash (Fast)", "Gemini 2.5 Pro (Accurate)", "GPT-4 Turbo"],
                help="Model for verification",
                key="model_select"
            )

            st.slider(
                "Confidence Threshold",
                0.0, 1.0, 0.7, 0.05,
                help="Minimum score for verification"
            )

            st.divider()

            # Bulk actions
            st.markdown("**Bulk Actions**")
            st.button("🔄 Rebuild All Indexes", use_container_width=True)
            st.button("📥 Export Corpus Metadata", use_container_width=True)
            st.button("🗑️ Clear All Documents", use_container_width=True, type="secondary")

        st.divider()

        # Statistics Card
        with st.container():
            st.subheader("📊 Statistics")
            st.metric("Total Chunks", "1,247")
            st.metric("Avg. Chunk Size", "142 words")
            st.metric("Last Indexed", "2 hours ago")
            st.metric("Index Size", "23.4 MB")

# ==================== TAB 2: VERIFICATION WORKFLOW ====================
with tab2:
    st.markdown("### 🔄 Document Verification Workflow")

    # Workflow cards in a cleaner layout
    col1, col2 = st.columns(2)

    with col1:
        # Card 1: Document Upload
        with st.container():
            st.markdown("#### 1️⃣ Upload Document")

            uploaded_doc = st.file_uploader(
                "Select document to verify",
                type=["pdf", "docx"],
                key="doc_verify",
                help="Upload the document you want to verify"
            )

            if uploaded_doc:
                st.success(f"✅ **{uploaded_doc.name}** ready for verification")

                # Show document info
                col_a, col_b = st.columns(2)
                with col_a:
                    st.caption("📄 File type: PDF")
                    st.caption("💾 Size: 2.3 MB")
                with col_b:
                    st.caption("📑 Pages: 15")
                    st.caption("⏱️ Est. time: 45s")

                st.button("🚀 Process Document", type="primary", use_container_width=True)
            else:
                st.info("👆 Upload a document to get started")

        st.divider()

        # Card 3: AI Verification
        with st.container():
            st.markdown("#### 3️⃣ AI Verification")

            if True:  # Corpus active
                st.success("✅ Reference corpus is active")

                # Verification options
                col_a, col_b = st.columns(2)
                with col_a:
                    st.selectbox("Verification Mode", ["Standard", "Detailed", "Quick Scan"], key="verify_mode")
                with col_b:
                    st.selectbox("Citation Format", ["APA", "Bluebook", "Chicago"], key="cite_format")

                # Start verification
                if st.button("▶️ Start Verification", type="primary", use_container_width=True):
                    with st.status("Verifying document...", expanded=True) as status:
                        st.write("🔍 Analyzing document structure...")
                        st.write("📝 Extracting chunks...")
                        st.write("🤖 Running AI verification...")
                        st.write("✅ Generating citations...")
                        status.update(label="Verification complete!", state="complete")
            else:
                st.warning("⚠️ Configure corpus first in the Reference Corpus tab")

    with col2:
        # Card 2: Chunking Configuration
        with st.container():
            st.markdown("#### 2️⃣ Chunking Settings")

            # Chunking mode with visual indicators
            chunking_mode = st.radio(
                "Select chunking strategy",
                options=[
                    ("paragraph", "📝 Paragraph-Level", "Groups related sentences for contextual verification"),
                    ("sentence", "📄 Sentence-Level", "Individual sentence verification for precision")
                ],
                format_func=lambda x: x[1],
                key="chunk_mode_radio"
            )

            # Show selected mode details
            st.info(f"**{chunking_mode[1]}**\n\n{chunking_mode[2]}")

            # Advanced options
            with st.expander("⚙️ Advanced Options"):
                st.slider("Max chunk size (words)", 50, 500, 150)
                st.slider("Chunk overlap (%)", 0, 50, 10)
                st.checkbox("Preserve document structure", value=True)
                st.checkbox("Include footnotes", value=True)

        st.divider()

        # Card 4: Export Configuration
        with st.container():
            st.markdown("#### 4️⃣ Export Results")

            # Output format selection
            output_format = st.selectbox(
                "Select output format",
                options=[
                    ("word_landscape", "📄 Word Document (Landscape)"),
                    ("word_portrait", "📄 Word Document (Portrait)"),
                    ("excel", "📊 Excel Spreadsheet"),
                    ("csv", "📋 CSV File"),
                    ("json", "💾 JSON (with metadata)")
                ],
                format_func=lambda x: x[1],
                key="output_format_select"
            )

            # Export options
            with st.expander("📝 Export Options"):
                st.multiselect(
                    "Include columns",
                    ["Page #", "Item #", "Text", "Verified", "Score", "Source", "Note", "Citations"],
                    default=["Page #", "Item #", "Text", "Verified", "Score", "Source"]
                )
                st.checkbox("Include unverified items", value=True)
                st.checkbox("Include metadata", value=True)
                st.checkbox("Color-code by confidence", value=True)

            # Generate button
            col_a, col_b = st.columns(2)
            with col_a:
                st.button("🎯 Generate", type="primary", use_container_width=True)
            with col_b:
                st.button("⬇️ Download", use_container_width=True, disabled=True)

    st.divider()

    # Live Preview Section
    st.markdown("### 👁️ Live Preview")

    with st.container():
        # Preview of verification results as they come in
        st.markdown("**Recent Verifications:**")

        # Sample preview items
        for i in range(3):
            col_page, col_text, col_status, col_score = st.columns([0.5, 3, 1, 1])

            with col_page:
                st.caption(f"**P{i+1}**")

            with col_text:
                st.caption("The plaintiff alleges that the defendant breached the contract by...")

            with col_status:
                if i == 0:
                    st.success("✅ Verified")
                elif i == 1:
                    st.warning("⚠️ Review")
                else:
                    st.error("❌ Unverified")

            with col_score:
                if i == 0:
                    st.metric("", "9.2/10")
                elif i == 1:
                    st.metric("", "6.5/10")
                else:
                    st.metric("", "2.1/10")

            st.divider()

# ==================== TAB 3: RESULTS DASHBOARD ====================
with tab3:
    st.markdown("### 📊 Verification Results Dashboard")

    # Summary metrics row
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="Total Chunks",
            value="124",
            delta="From 15 pages"
        )

    with col2:
        st.metric(
            label="Verified",
            value="89",
            delta="+71.8%",
            delta_color="normal"
        )

    with col3:
        st.metric(
            label="Avg Confidence",
            value="8.2/10",
            delta="+0.8",
            delta_color="normal"
        )

    with col4:
        st.metric(
            label="Processing Time",
            value="45s",
            delta="-15s",
            delta_color="inverse"
        )

    with col5:
        st.metric(
            label="Status",
            value="Complete",
            delta="100%"
        )

    st.divider()

    # Visual confidence distribution
    col_main, col_side = st.columns([2.5, 1.5])

    with col_main:
        # Interactive results table with filters
        st.markdown("#### 📋 Detailed Results")

        # Filters row
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            filter_status = st.selectbox("Status", ["All", "✅ Verified", "⚠️ Review Needed", "❌ Unverified"], key="filter_status_tab3")
        with col_f2:
            filter_page = st.selectbox("Page", ["All Pages"] + [f"Page {i}" for i in range(1, 16)], key="filter_page_tab3")
        with col_f3:
            filter_confidence = st.selectbox("Confidence", ["All Scores", "High (8-10)", "Medium (5-7)", "Low (<5)"], key="filter_conf_tab3")
        with col_f4:
            st.text_input("🔍 Search", placeholder="Search text...", label_visibility="collapsed", key="search_tab3")

        st.divider()

        # Results as expandable cards (more interactive than table)
        st.markdown("**Results (showing 10 of 124)**")

        for idx in range(5):
            verified_status = idx % 3

            # Determine styling based on verification status
            if verified_status == 0:
                card_class = "verified"
                status_icon = "✅"
                status_text = "Verified"
                score = 9.2 - (idx * 0.3)
                source = "Contract_2024.pdf, Section 2.1"
            elif verified_status == 1:
                card_class = "review"
                status_icon = "⚠️"
                status_text = "Review Needed"
                score = 6.5
                source = "Regulations.docx, Page 12"
            else:
                card_class = "unverified"
                status_icon = "❌"
                status_text = "Unverified"
                score = 2.8
                source = "No match found"

            with st.container():
                col_expand, col_content = st.columns([0.1, 3.9])

                with col_content:
                    # Header row
                    col_h1, col_h2, col_h3 = st.columns([2, 1, 1])
                    with col_h1:
                        st.markdown(f"**Page 2, Item 1.{idx+1}** {status_icon}")
                    with col_h2:
                        st.caption(f"Score: **{score:.1f}/10**")
                    with col_h3:
                        # Confidence bar
                        st.progress(score / 10.0)

                    # Text preview
                    st.caption("The defendant alleges that pursuant to Section 2.1 of the agreement, the plaintiff failed to provide adequate notice of termination...")

                    # Expandable details
                    with st.expander("View Details & Citations"):
                        col_a, col_b = st.columns(2)

                        with col_a:
                            st.markdown("**Verification Source:**")
                            st.info(source)

                            st.markdown("**AI Reasoning:**")
                            st.caption("This statement directly references Section 2.1 of the contract, which outlines the termination notice requirements. The language matches the original contract text with 95% similarity.")

                        with col_b:
                            st.markdown("**Citations:**")
                            st.code('''
Citation 1:
  Document: Contract_2024.pdf
  Section: 2.1
  Page: 8
  Excerpt: "Party B shall provide written notice
  of termination no less than 30 days prior..."
  Confidence: 9.2/10
                            ''', language="text")

                            st.button("📋 Copy Citation", key=f"copy_{idx}", use_container_width=True)

                st.divider()

        # Pagination
        col_p1, col_p2, col_p3 = st.columns([1, 2, 1])
        with col_p2:
            st.selectbox("Items per page", [10, 25, 50, 100], key="items_per_page", label_visibility="collapsed")
        with col_p3:
            st.markdown("**Page 1 of 13**")

    with col_side:
        # Confidence distribution chart
        st.markdown("#### 📈 Confidence Distribution")

        # Visual breakdown
        st.markdown("**By Score Range:**")

        # High confidence
        st.markdown("🟢 **High (8-10)**")
        st.progress(0.54)
        st.caption("67 chunks (54%)")
        st.divider()

        # Medium confidence
        st.markdown("🟡 **Medium (5-7)**")
        st.progress(0.18)
        st.caption("22 chunks (18%)")
        st.divider()

        # Low confidence
        st.markdown("🔴 **Low (<5)**")
        st.progress(0.07)
        st.caption("9 chunks (7%)")
        st.divider()

        # Unverified
        st.markdown("⚪ **Unverified**")
        st.progress(0.21)
        st.caption("26 chunks (21%)")

        st.divider()

        # Top issues requiring review
        st.markdown("#### ⚠️ Priority Review")
        st.caption("Items needing manual attention:")

        for i in range(3):
            with st.container():
                st.markdown(f"**Page {i+3}, Item {i+2}**")
                st.caption("Low confidence (3.2/10)")
                st.button("Review", key=f"review_{i}", use_container_width=True, type="secondary")
                if i < 2:
                    st.divider()

        st.divider()

        # Export summary
        st.markdown("#### 📤 Export Options")
        st.button("📄 Download Full Report", type="primary", use_container_width=True)
        st.button("📊 Export to Excel", use_container_width=True)
        st.button("💾 Save as JSON", use_container_width=True)

# ==================== FOOTER ====================
st.divider()
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.caption("Content Verification Tool v2.0.0 | Powered by Google Gemini AI | Built with ❤️ using Streamlit")
