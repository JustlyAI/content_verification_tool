"""
Design Mockup 4: Premium Legal Tech Aesthetic
Inspired by Freshfields - refined minimalism with sophisticated details

Color Philosophy: Deep charcoal + warm gold accents + soft neutrals
Typography: Serif headings + clean sans-serif body
Aesthetic: Bloomberg Terminal meets luxury law firm
"""

import streamlit as st
import time

st.set_page_config(
    page_title="Content Verification | Freshfields",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Import sophisticated fonts */
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    /* Color Variables - Premium Legal Palette (Light Mode) */
    :root {
        --primary-dark: #1a1d2e;
        --primary-charcoal: #2d3142;
        --accent-gold: #d4af37;
        --accent-warm: #c9a961;
        --neutral-light: #f8f9fa;
        --neutral-mid: #e4e7eb;
        --text-primary: #1a1d2e;
        --text-secondary: #6b7280;
        --success-green: #059669;
        --warning-amber: #d97706;
        --error-red: #dc2626;
        --border-subtle: #e5e7eb;
        --bg-main: #ffffff;
        --bg-gradient-start: #ffffff;
        --bg-gradient-end: #f8f9fa;
        --card-bg: #ffffff;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-gold: 0 4px 14px 0 rgba(212, 175, 55, 0.15);
    }

    /* Dark Mode Colors */
    @media (prefers-color-scheme: dark) {
        :root {
            --primary-dark: #e8e9ed;
            --primary-charcoal: #f1f2f4;
            --accent-gold: #f4d03f;
            --accent-warm: #e6c766;
            --neutral-light: #1e2128;
            --neutral-mid: #2a2e39;
            --text-primary: #e8e9ed;
            --text-secondary: #a1a5b3;
            --success-green: #10b981;
            --warning-amber: #fbbf24;
            --error-red: #ef4444;
            --border-subtle: #3a3f4f;
            --bg-main: #0d0f14;
            --bg-gradient-start: #0d0f14;
            --bg-gradient-end: #1a1d2e;
            --card-bg: #1a1d2e;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.3);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.4);
            --shadow-gold: 0 4px 14px 0 rgba(244, 208, 63, 0.2);
        }
    }

    /* Global Resets */
    .main {
        background: linear-gradient(to bottom, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
        padding: 2rem 3rem;
    }

    /* Streamlit elements dark mode fix */
    .stMarkdown, .stButton, .stSelectbox, .stTextInput, .stTextArea, .stFileUploader {
        color: var(--text-primary);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Typography System */
    h1, h2, h3 {
        font-family: 'Crimson Pro', serif;
        color: var(--primary-dark);
        letter-spacing: -0.02em;
        font-weight: 600;
    }

    h1 {
        font-size: 3rem;
        line-height: 1.1;
        margin-bottom: 0.5rem;
    }

    h2 {
        font-size: 2rem;
        line-height: 1.2;
        margin-bottom: 1rem;
    }

    h3 {
        font-size: 1.5rem;
        line-height: 1.3;
    }

    p, div, label, span {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
    }

    /* Premium Header */
    .premium-header {
        background: linear-gradient(135deg, #1a1d2e 0%, #2d3142 100%);
        padding: 3rem 2.5rem;
        border-radius: 0.75rem;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-lg);
    }

    @media (prefers-color-scheme: dark) {
        .premium-header {
            background: linear-gradient(135deg, #2d3142 0%, #3a3f4f 100%);
        }
    }

    .premium-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.02'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.4;
    }

    .header-content {
        position: relative;
        z-index: 1;
    }

    .header-title {
        font-family: 'Crimson Pro', serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }

    .header-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.125rem;
        color: rgba(255, 255, 255, 0.85);
        margin-top: 1rem;
        font-weight: 300;
        letter-spacing: 0.01em;
    }

    .header-badge {
        display: inline-block;
        background: var(--accent-gold);
        color: #1a1d2e;
        padding: 0.375rem 1rem;
        border-radius: 2rem;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-top: 1.5rem;
        box-shadow: var(--shadow-gold);
    }

    /* Premium Tabs */
    .stTabs {
        background: transparent;
        padding: 0;
        margin-top: 2rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        border-bottom: 2px solid var(--border-subtle);
        padding: 0 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: var(--text-secondary);
        padding: 1rem 2rem;
        border-radius: 0.5rem 0.5rem 0 0;
        background: transparent;
        border: none;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: var(--neutral-light);
        color: var(--text-primary);
    }

    .stTabs [aria-selected="true"] {
        background: var(--card-bg);
        color: var(--text-primary);
        border-bottom: 3px solid var(--accent-gold);
        font-weight: 600;
        box-shadow: var(--shadow-sm);
    }

    /* Premium Cards */
    .premium-card {
        background: var(--card-bg);
        border: 1px solid var(--border-subtle);
        border-radius: 0.75rem;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }

    .premium-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
        border-color: var(--accent-warm);
    }

    .premium-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--accent-gold);
        border-radius: 0.75rem 0 0 0.75rem;
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .premium-card:hover::before {
        opacity: 1;
    }

    /* Workflow Step Cards */
    .workflow-card {
        background: var(--card-bg);
        border: 1px solid var(--border-subtle);
        border-radius: 0.75rem;
        padding: 1.75rem;
        height: 100%;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .workflow-card::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-gold) 0%, var(--accent-warm) 100%);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }

    .workflow-card:hover::after {
        transform: scaleX(1);
    }

    .step-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 2.5rem;
        height: 2.5rem;
        background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-warm) 100%);
        color: white;
        border-radius: 50%;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.125rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow-gold);
    }

    .step-title {
        font-family: 'Crimson Pro', serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--primary-dark);
        margin-bottom: 1rem;
        letter-spacing: -0.01em;
    }

    /* Status Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        font-size: 0.875rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.01em;
    }

    .status-active {
        background: rgba(5, 150, 105, 0.1);
        color: var(--success-green);
        border: 1px solid rgba(5, 150, 105, 0.2);
    }

    .status-pending {
        background: rgba(217, 119, 6, 0.1);
        color: var(--warning-amber);
        border: 1px solid rgba(217, 119, 6, 0.2);
    }

    .status-inactive {
        background: rgba(107, 114, 128, 0.1);
        color: var(--text-secondary);
        border: 1px solid rgba(107, 114, 128, 0.2);
    }

    /* Premium Buttons */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        border: none;
        transition: all 0.2s ease;
        letter-spacing: 0.01em;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-warm) 100%);
        color: white;
        box-shadow: var(--shadow-gold);
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px 0 rgba(212, 175, 55, 0.25);
    }

    .stButton > button[kind="secondary"] {
        background: var(--card-bg);
        color: var(--text-primary);
        border: 1px solid var(--border-subtle);
    }

    .stButton > button[kind="secondary"]:hover {
        border-color: var(--accent-gold);
        background: var(--neutral-light);
    }

    /* File Uploader */
    .stFileUploader {
        border: 2px dashed var(--border-subtle);
        border-radius: 0.75rem;
        padding: 2rem;
        background: var(--neutral-light);
        transition: all 0.3s ease;
    }

    .stFileUploader:hover {
        border-color: var(--accent-gold);
        background: var(--card-bg);
    }

    /* Progress Metrics */
    .metric-card {
        background: linear-gradient(135deg, var(--card-bg) 0%, var(--neutral-light) 100%);
        border: 1px solid var(--border-subtle);
        border-radius: 0.75rem;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        box-shadow: var(--shadow-md);
        border-color: var(--accent-warm);
    }

    .metric-value {
        font-family: 'Crimson Pro', serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-dark);
        line-height: 1;
        margin-bottom: 0.5rem;
    }

    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }

    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, var(--border-subtle) 50%, transparent 100%);
        margin: 3rem 0;
    }

    /* Confidence Bars */
    .confidence-bar {
        height: 0.5rem;
        background: var(--neutral-mid);
        border-radius: 1rem;
        overflow: hidden;
        margin: 0.5rem 0;
    }

    .confidence-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--accent-gold) 0%, var(--accent-warm) 100%);
        border-radius: 1rem;
        transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Dataframe Styling */
    .stDataFrame {
        border: 1px solid var(--border-subtle);
        border-radius: 0.75rem;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }

    /* Powered By */
    .powered-by {
        text-align: center;
        margin: 2rem 0;
        padding: 1rem;
        background: linear-gradient(135deg, var(--card-bg) 0%, var(--neutral-light) 100%);
        border-radius: 0.75rem;
        border: 1px solid var(--border-subtle);
    }

    .powered-by-text {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 500;
        margin-bottom: 0.75rem;
    }

    /* Connection Status */
    .connection-status {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: var(--card-bg);
        border: 1px solid var(--border-subtle);
        border-radius: 2rem;
        font-size: 0.875rem;
        font-family: 'Inter', sans-serif;
        box-shadow: var(--shadow-sm);
    }

    .status-dot {
        width: 0.5rem;
        height: 0.5rem;
        background: var(--success-green);
        border-radius: 50%;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    /* Smooth Animations */
    * {
        transition-property: background-color, border-color, color, fill, stroke, opacity, box-shadow, transform;
        transition-duration: 0.2s;
        transition-timing-function: ease-in-out;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="premium-header">
    <div class="header-content">
        <h1 class="header-title">Content Verification</h1>
        <p class="header-subtitle">AI-powered legal document verification with systematic precision</p>
        <span class="header-badge">Powered by Google Gemini</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Connection status
col1, col2 = st.columns([6, 1])
with col1:
    st.markdown("""
    <div class="connection-status">
        <span class="status-dot"></span>
        <span>Backend Connected</span>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.button("⟳", help="Refresh")

st.markdown("<br>", unsafe_allow_html=True)

# ==================== TABS ====================
tab1, tab2 = st.tabs(["📚 Reference Corpus", "⚖️ Verification Workflow"])

# ==================== TAB 1: CORPUS ====================
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    # Status banner with premium styling
    status_col1, status_col2, status_col3 = st.columns([3, 1, 1])
    with status_col1:
        st.markdown("""
        <div class="status-badge status-active">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm3.78-9.72a.75.75 0 0 0-1.06-1.06L6.75 9.19 5.28 7.72a.75.75 0 0 0-1.06 1.06l2 2a.75.75 0 0 0 1.06 0l4.5-4.5z"/>
            </svg>
            Corpus Active
        </div>
        <span style="margin-left: 1rem; color: var(--text-secondary); font-size: 0.875rem;">5 documents indexed • 127 pages • Ready for verification</span>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Two-column layout
    col1, col2 = st.columns([2.5, 1.5])

    with col1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top: 0;">Reference Library</h3>', unsafe_allow_html=True)

        # Search
        st.text_input("🔍 Search documents", placeholder="Search by name, type, or keyword...", label_visibility="collapsed", key="corpus_search")

        st.markdown("<br>", unsafe_allow_html=True)

        # Document list - premium styling
        for idx, (name, pages, size, date) in enumerate([
            ("Case Law Analysis 2023.pdf", "45 pages", "5.2 MB", "Nov 10, 2025"),
            ("Regulatory Framework.docx", "23 pages", "1.8 MB", "Nov 9, 2025"),
            ("Precedent Study.pdf", "59 pages", "7.3 MB", "Nov 8, 2025"),
        ]):
            with st.expander(f"📄 {name}", expanded=False):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.caption(f"**Pages:** {pages}")
                    st.caption(f"**Size:** {size}")
                with col_b:
                    st.caption(f"**Added:** {date}")
                    st.caption(f"**Status:** ✓ Indexed")

                st.markdown("<br>", unsafe_allow_html=True)
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    st.button("Reindex", key=f"reindex_{idx}", use_container_width=True)
                with btn_col2:
                    st.button("Remove", key=f"remove_{idx}", type="secondary", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Upload new documents
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top: 0;">Add Reference Documents</h3>', unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Upload documents",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            key="new_corpus_files",
            label_visibility="collapsed"
        )

        if uploaded_files:
            st.info(f"📦 {len(uploaded_files)} file(s) selected")
            st.button("Upload & Index", type="primary", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Corpus statistics
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top: 0;">Statistics</h3>', unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">5</div>
            <div class="metric-label">Documents</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">127</div>
            <div class="metric-label">Total Pages</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">23.4</div>
            <div class="metric-label">MB Storage</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Configuration
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top: 0;">Configuration</h3>', unsafe_allow_html=True)

        st.text_area(
            "Case Context",
            placeholder="Describe the verification context...",
            height=120,
            help="Provides AI with context for better verification",
            key="case_context"
        )

        st.selectbox(
            "AI Model",
            ["Gemini 2.5 Flash", "Gemini 2.5 Pro"],
            key="ai_model"
        )

        st.slider(
            "Confidence Threshold",
            0.0, 1.0, 0.7, 0.05,
            help="Minimum confidence score for verification"
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.button("💾 Save Configuration", type="primary", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 2: VERIFICATION ====================
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    # Workflow steps - 4 cards horizontal
    st.markdown('<h2>Verification Workflow</h2>', unsafe_allow_html=True)
    st.caption("Complete each step to generate your verified document")

    st.markdown("<br>", unsafe_allow_html=True)

    step1, step2, step3, step4 = st.columns(4, gap="medium")

    with step1:
        st.markdown('<div class="workflow-card">', unsafe_allow_html=True)
        st.markdown('<div class="step-number">1</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-title">Upload</div>', unsafe_allow_html=True)

        uploaded_doc = st.file_uploader(
            "Select document",
            type=["pdf", "docx"],
            key="verify_upload",
            label_visibility="collapsed"
        )

        if uploaded_doc:
            st.markdown("""
            <div class="status-badge status-active" style="margin-top: 1rem;">
                ✓ Document Ready
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"📄 {uploaded_doc.name}")
            st.button("Process", type="primary", use_container_width=True, key="process_btn")
        else:
            st.markdown("""
            <div class="status-badge status-pending" style="margin-top: 1rem;">
                ⏳ Waiting
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with step2:
        st.markdown('<div class="workflow-card">', unsafe_allow_html=True)
        st.markdown('<div class="step-number">2</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-title">Chunking</div>', unsafe_allow_html=True)

        chunking_mode = st.radio(
            "Select mode",
            ["Paragraph", "Sentence"],
            key="chunk_radio",
            label_visibility="collapsed"
        )

        st.caption(f"**Selected:** {chunking_mode}-level analysis")

        st.markdown("""
        <div class="status-badge status-active" style="margin-top: 1rem;">
            ✓ Mode Selected
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with step3:
        st.markdown('<div class="workflow-card">', unsafe_allow_html=True)
        st.markdown('<div class="step-number">3</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-title">Verify</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="status-badge status-active" style="margin-bottom: 1rem;">
            ✓ Corpus Ready
        </div>
        """, unsafe_allow_html=True)

        st.caption("AI verification against reference corpus")

        st.button("▶ Run Verification", type="primary", use_container_width=True, key="verify_btn")

        st.markdown('</div>', unsafe_allow_html=True)

    with step4:
        st.markdown('<div class="workflow-card">', unsafe_allow_html=True)
        st.markdown('<div class="step-number">4</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-title">Export</div>', unsafe_allow_html=True)

        export_format = st.selectbox(
            "Output format",
            ["Word (Landscape)", "Word (Portrait)", "Excel", "CSV", "JSON"],
            key="export_format",
            label_visibility="collapsed"
        )

        st.button("Generate", use_container_width=True, key="gen_btn")
        st.button("⬇ Download", type="primary", use_container_width=True, disabled=True, key="dl_btn")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Divider
    st.markdown("<hr>", unsafe_allow_html=True)

    # Results section
    st.markdown('<h2>Verification Results</h2>', unsafe_allow_html=True)

    # Metrics row with premium styling
    metric1, metric2, metric3, metric4, metric5 = st.columns(5)

    with metric1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">124</div>
            <div class="metric-label">Total Chunks</div>
        </div>
        """, unsafe_allow_html=True)

    with metric2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">89</div>
            <div class="metric-label">Verified</div>
        </div>
        """, unsafe_allow_html=True)

    with metric3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">8.2</div>
            <div class="metric-label">Avg Score</div>
        </div>
        """, unsafe_allow_html=True)

    with metric4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">45s</div>
            <div class="metric-label">Process Time</div>
        </div>
        """, unsafe_allow_html=True)

    with metric5:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value" style="color: var(--success-green);">✓</div>
            <div class="metric-label">Complete</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Confidence breakdown with premium bars
    col1, col2 = st.columns([2, 2])

    with col1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top: 0;">Confidence Distribution</h3>', unsafe_allow_html=True)

        st.markdown("""
        <div style="margin: 1.5rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 500; color: var(--success-green);">● High Confidence (8-10)</span>
                <span style="font-weight: 600;">54%</span>
            </div>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: 54%; background: linear-gradient(90deg, #059669 0%, #10b981 100%);"></div>
            </div>
            <span style="font-size: 0.875rem; color: var(--text-secondary);">67 chunks</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin: 1.5rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 500; color: var(--warning-amber);">● Medium Confidence (5-7)</span>
                <span style="font-weight: 600;">18%</span>
            </div>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: 18%; background: linear-gradient(90deg, #d97706 0%, #f59e0b 100%);"></div>
            </div>
            <span style="font-size: 0.875rem; color: var(--text-secondary);">22 chunks</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin: 1.5rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 500; color: var(--error-red);">● Low/Unverified</span>
                <span style="font-weight: 600;">28%</span>
            </div>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: 28%; background: linear-gradient(90deg, #dc2626 0%, #ef4444 100%);"></div>
            </div>
            <span style="font-size: 0.875rem; color: var(--text-secondary);">35 chunks - Manual review needed</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top: 0;">Items Requiring Review</h3>', unsafe_allow_html=True)

        with st.expander("⚠️ Page 2, Item 4 - Low Confidence", expanded=True):
            st.markdown("*Furthermore, the analysis indicates that...*")
            st.caption("**Issue:** Confidence score 4.2/10")
            st.caption("**Recommendation:** Manual verification recommended")
            st.button("View Details", key="detail1", use_container_width=True)

        with st.expander("⚠️ Page 3, Item 7 - No Match"):
            st.markdown("*The plaintiff contends...*")
            st.caption("**Issue:** No reference document match found")
            st.button("View Details", key="detail2", use_container_width=True)

        with st.expander("⚠️ Page 5, Item 2 - Conflicting"):
            st.markdown("*According to the statute...*")
            st.caption("**Issue:** Multiple conflicting sources detected")
            st.button("View Details", key="detail3", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("""
<div class="powered-by">
    <div class="powered-by-text">Powered by</div>
    <img src="https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg"
         alt="Google Gemini"
         style="height: 32px; opacity: 0.8;">
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; color: var(--text-secondary); font-size: 0.875rem; font-family: 'Inter', sans-serif;">
        Content Verification Tool v2.0 • Built for Freshfields
    </div>
    """, unsafe_allow_html=True)
