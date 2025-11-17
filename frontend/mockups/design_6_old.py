"""
Design Mockup 6: Single-Screen Freshfields-Inspired MVP
Gemini-centric verification workflow with sophisticated minimalism

Design Philosophy: Freshfields Aesthetic
- Elegant serif headlines (Lora) with generous line-height
- Clean sans-serif body (Inter)
- Soft powder blues (#A4C8E1) and lime green (#C8E86B) accents
- Cream white backgrounds (#FAFAF9)
- Pill-shaped buttons
- Generous whitespace and breathing room
- Gemini prominently featured throughout
"""

import streamlit as st

st.set_page_config(
    page_title="Content Verification | Powered by Gemini",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==================== FRESHFIELDS-INSPIRED CSS ====================
st.markdown(
    """
<style>
    /* Import Fonts - Freshfields Style */
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Color Variables - Freshfields Palette */
    :root {
        /* Neutrals */
        --white: #ffffff;
        --cream-white: #fafaf9;
        --cream: #f5f4f0;
        --warm-gray-light: #e8e6e3;
        --warm-gray: #c8c5c0;
        --mid-gray: #9b9690;
        --charcoal: #3d3935;
        --black: #000000;

        /* Freshfields Blue - Powder blue */
        --ff-blue-50: #f0f6fa;
        --ff-blue-100: #e5f0f7;
        --ff-blue-200: #c9e1ee;
        --ff-blue-300: #a4c8e1;
        --ff-blue-400: #7ba8c9;

        /* Freshfields Green - Lime/Chartreuse */
        --ff-green-50: #f5f9e8;
        --ff-green-100: #e8f3d6;
        --ff-green-300: #c8e86b;
        --ff-green-400: #b0d94f;

        /* Gemini Brand */
        --gemini-blue-light: #e0f2f7;
        --gemini-blue: #4fc3f7;
        --gemini-blue-dark: #0288d1;

        /* Semantic */
        --success: #059669;
        --warning: #f59e0b;
        --error: #dc2626;

        /* Layout */
        --sidebar-width: 300px;
        --header-height: 72px;
        --footer-height: 48px;

        /* Spacing */
        --space-1: 0.5rem;
        --space-2: 1rem;
        --space-3: 1.5rem;
        --space-4: 2rem;
        --space-6: 3rem;

        /* Border Radius */
        --radius-sm: 0.25rem;
        --radius-md: 0.5rem;
        --radius-lg: 1rem;
        --radius-xl: 1.5rem;
        --radius-full: 9999px;

        /* Shadows */
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.06);
        --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.08);
        --shadow-lg: 0 8px 20px rgba(0, 0, 0, 0.1);
    }

    /* Global Reset */
    .main {
        background: var(--cream-white);
        padding: 0 !important;
        max-width: 100% !important;
    }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Typography - Freshfields Style */
    h1, h2, h3, .serif {
        font-family: 'Lora', 'Georgia', serif;
        color: var(--black);
        font-weight: 600;
        letter-spacing: -0.01em;
        line-height: 1.3;
    }

    h1 { font-size: 2.5rem; }
    h2 { font-size: 1.875rem; }
    h3 { font-size: 1.25rem; }

    p, div, label, span, input, textarea, button {
        font-family: 'Inter', -apple-system, sans-serif;
        color: var(--charcoal);
    }

    /* Header Component */
    .freshfields-header {
        height: var(--header-height);
        background: var(--cream-white);
        border-bottom: 1px solid var(--warm-gray-light);
        padding: 0 var(--space-6);
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: sticky;
        top: 0;
        z-index: 100;
    }

    .header-title {
        font-family: 'Lora', serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--black);
        letter-spacing: -0.01em;
    }

    .gemini-badge {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1.25rem;
        background: var(--white);
        border: 1.5px solid var(--gemini-blue-dark);
        border-radius: var(--radius-full);
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--gemini-blue-dark);
        box-shadow: var(--shadow-sm);
    }

    /* Main Grid Layout */
    .main-grid {
        display: grid;
        grid-template-columns: var(--sidebar-width) 1fr;
        min-height: calc(100vh - var(--header-height) - var(--footer-height));
    }

    /* Corpus Sidebar */
    .corpus-sidebar {
        background: var(--ff-blue-100);
        padding: var(--space-4);
        overflow-y: auto;
        border-right: 1px solid var(--ff-blue-200);
    }

    .sidebar-title {
        font-family: 'Lora', serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--black);
        margin-bottom: var(--space-3);
        letter-spacing: -0.01em;
    }

    .corpus-status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.375rem;
        padding: 0.375rem 0.875rem;
        background: rgba(5, 150, 105, 0.1);
        border: 1px solid var(--success);
        border-radius: var(--radius-full);
        font-size: 0.8125rem;
        font-weight: 600;
        color: var(--success);
        margin-bottom: var(--space-2);
    }

    .corpus-stats-card {
        background: var(--white);
        border: 1px solid var(--ff-blue-200);
        border-radius: var(--radius-lg);
        padding: var(--space-3);
        margin: var(--space-2) 0 var(--space-4) 0;
        box-shadow: var(--shadow-sm);
    }

    .stat-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.625rem 0;
        border-bottom: 1px solid var(--cream);
    }

    .stat-item:last-child {
        border-bottom: none;
    }

    .stat-label {
        font-size: 0.875rem;
        color: var(--mid-gray);
    }

    .stat-value {
        font-weight: 600;
        font-size: 0.9375rem;
        color: var(--black);
    }

    .section-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--mid-gray);
        margin: var(--space-4) 0 var(--space-2) 0;
        display: block;
    }

    /* Pill Buttons - Freshfields Style */
    .pill-button {
        width: 100%;
        padding: 0.75rem 1.5rem;
        background: var(--white);
        border: 1.5px solid var(--warm-gray);
        border-radius: var(--radius-full);
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--charcoal);
        cursor: pointer;
        transition: all 0.25s ease;
        text-align: center;
        margin-bottom: var(--space-2);
    }

    .pill-button:hover {
        border-color: var(--black);
        background: var(--cream-white);
        transform: translateY(-1px);
        box-shadow: var(--shadow-sm);
    }

    .pill-button-primary {
        background: var(--black);
        border-color: var(--black);
        color: var(--white);
        font-weight: 600;
    }

    .pill-button-primary:hover {
        background: var(--charcoal);
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }

    .pill-button-accent {
        background: var(--ff-green-300);
        border-color: var(--ff-green-400);
        color: var(--black);
        font-weight: 600;
    }

    .pill-button-accent:hover {
        background: var(--ff-green-400);
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }

    /* Main Content Area */
    .main-content {
        padding: var(--space-6);
        overflow-y: auto;
        background: var(--white);
    }

    .content-title {
        font-family: 'Lora', serif;
        font-size: 1.875rem;
        font-weight: 600;
        color: var(--black);
        margin-bottom: var(--space-2);
        letter-spacing: -0.01em;
    }

    .content-subtitle {
        font-size: 1rem;
        color: var(--mid-gray);
        margin-bottom: var(--space-6);
        line-height: 1.6;
    }

    /* Workflow Cards Grid */
    .workflow-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: var(--space-3);
        margin-bottom: var(--space-6);
    }

    .workflow-card {
        background: var(--white);
        border: 1.5px solid var(--warm-gray-light);
        border-radius: var(--radius-lg);
        padding: var(--space-4);
        transition: all 0.3s ease;
        position: relative;
    }

    .workflow-card:hover {
        border-color: var(--warm-gray);
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }

    /* Gemini Card Special Treatment */
    .workflow-card-gemini {
        background: linear-gradient(135deg, var(--gemini-blue-light) 0%, var(--white) 100%);
        border: 2px solid var(--gemini-blue);
    }

    .workflow-card-gemini:hover {
        border-color: var(--gemini-blue-dark);
        box-shadow: var(--shadow-lg);
    }

    .card-number {
        position: absolute;
        top: 1rem;
        right: 1rem;
        width: 32px;
        height: 32px;
        background: var(--cream);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Lora', serif;
        font-weight: 700;
        font-size: 0.875rem;
        color: var(--mid-gray);
    }

    .card-title {
        font-family: 'Lora', serif;
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--black);
        margin-bottom: var(--space-3);
        letter-spacing: -0.01em;
    }

    .card-description {
        font-size: 0.875rem;
        color: var(--mid-gray);
        line-height: 1.6;
        margin-bottom: var(--space-3);
    }

    .card-status {
        display: inline-flex;
        align-items: center;
        gap: 0.375rem;
        padding: 0.375rem 0.875rem;
        border-radius: var(--radius-full);
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: var(--space-2);
    }

    .status-ready {
        background: rgba(5, 150, 105, 0.1);
        color: var(--success);
        border: 1px solid rgba(5, 150, 105, 0.3);
    }

    .status-waiting {
        background: rgba(155, 150, 144, 0.1);
        color: var(--mid-gray);
        border: 1px solid var(--warm-gray);
    }

    .status-active {
        background: rgba(79, 195, 247, 0.1);
        color: var(--gemini-blue-dark);
        border: 1px solid var(--gemini-blue);
    }

    /* Gemini Icon Badge */
    .gemini-icon-large {
        font-size: 2.5rem;
        text-align: center;
        margin: var(--space-2) 0;
    }

    /* Results Section */
    .results-container {
        background: var(--cream-white);
        border: 1.5px solid var(--warm-gray-light);
        border-radius: var(--radius-lg);
        padding: var(--space-6);
        margin-top: var(--space-6);
    }

    .results-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: var(--space-4);
        padding-bottom: var(--space-3);
        border-bottom: 1.5px solid var(--warm-gray-light);
    }

    .results-title {
        font-family: 'Lora', serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--black);
        letter-spacing: -0.01em;
    }

    .results-timestamp {
        font-size: 0.875rem;
        color: var(--mid-gray);
    }

    /* Metrics Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: var(--space-3);
        margin-bottom: var(--space-6);
    }

    .metric-box {
        background: var(--white);
        border: 1px solid var(--warm-gray-light);
        border-radius: var(--radius-md);
        padding: var(--space-3);
        text-align: center;
        transition: all 0.2s ease;
    }

    .metric-box:hover {
        border-color: var(--ff-blue-300);
        box-shadow: var(--shadow-sm);
    }

    .metric-value {
        font-family: 'Lora', serif;
        font-size: 2.25rem;
        font-weight: 700;
        color: var(--black);
        line-height: 1;
        margin-bottom: 0.5rem;
    }

    .metric-label {
        font-size: 0.75rem;
        color: var(--mid-gray);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }

    /* Confidence Bars */
    .confidence-section {
        margin-top: var(--space-4);
    }

    .confidence-item {
        margin-bottom: var(--space-3);
    }

    .confidence-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .confidence-label {
        font-size: 0.9375rem;
        font-weight: 500;
        color: var(--charcoal);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .confidence-value {
        font-family: 'Lora', serif;
        font-weight: 700;
        font-size: 1rem;
        color: var(--black);
    }

    .confidence-bar {
        height: 12px;
        background: var(--cream);
        border-radius: var(--radius-sm);
        overflow: hidden;
        position: relative;
    }

    .confidence-fill {
        height: 100%;
        border-radius: var(--radius-sm);
        transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .fill-high {
        background: linear-gradient(90deg, var(--ff-green-300) 0%, var(--ff-green-400) 100%);
    }

    .fill-medium {
        background: linear-gradient(90deg, var(--warning) 0%, #fbbf24 100%);
    }

    .fill-low {
        background: linear-gradient(90deg, var(--error) 0%, #ef4444 100%);
    }

    .confidence-count {
        font-size: 0.8125rem;
        color: var(--mid-gray);
        margin-top: 0.375rem;
    }

    /* Footer */
    .freshfields-footer {
        height: var(--footer-height);
        background: var(--cream-white);
        border-top: 1px solid var(--warm-gray-light);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.875rem;
        color: var(--mid-gray);
    }

    /* Streamlit Overrides */
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        border-radius: var(--radius-full) !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.25s ease !important;
        border: none !important;
    }

    .stButton > button[kind="primary"] {
        background: var(--ff-green-300) !important;
        color: var(--black) !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: var(--ff-green-400) !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-md) !important;
    }

    .stButton > button[kind="secondary"] {
        background: var(--white) !important;
        color: var(--charcoal) !important;
        border: 1.5px solid var(--warm-gray) !important;
    }

    /* File Uploader */
    .stFileUploader {
        border: 2px dashed var(--ff-blue-300) !important;
        border-radius: var(--radius-md) !important;
        background: var(--white) !important;
        padding: var(--space-2) !important;
    }

    .stFileUploader:hover {
        border-color: var(--ff-blue-400) !important;
        background: var(--ff-blue-50) !important;
    }

    /* Text Input */
    .stTextInput input, .stTextArea textarea {
        border-radius: var(--radius-md) !important;
        border: 1.5px solid var(--warm-gray-light) !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--ff-blue-400) !important;
        box-shadow: 0 0 0 2px rgba(164, 200, 225, 0.2) !important;
    }

    /* Radio */
    .stRadio > div {
        gap: var(--space-2) !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: var(--radius-md) !important;
    }

    /* Smooth Transitions */
    * {
        transition-property: background-color, border-color, color, box-shadow, transform;
        transition-duration: 0.25s;
        transition-timing-function: ease;
    }

    /* Divider */
    hr {
        border: none;
        height: 1.5px;
        background: var(--warm-gray-light);
        margin: var(--space-4) 0;
    }

    /* Expander */
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border-radius: var(--radius-md) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ==================== HEADER ====================
st.markdown(
    """
<div class="freshfields-header">
    <div class="header-title">Content Verification</div>
    <div class="gemini-badge">
        <span>🔷</span>
        <span>Powered by Gemini</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ==================== MAIN GRID LAYOUT ====================
# Use Streamlit columns to create the grid layout
sidebar_col, main_col = st.columns([1, 3], gap="small")

# ==================== LEFT: CORPUS SIDEBAR ====================
with sidebar_col:
    st.markdown('<div class="corpus-sidebar">', unsafe_allow_html=True)

    st.markdown(
        '<div class="sidebar-title">Reference Corpus</div>', unsafe_allow_html=True
    )

    # Corpus Status Badge
    st.markdown(
        """
    <div class="corpus-status-badge">
        <span>✓</span>
        <span>Active & Ready</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Corpus Stats Card
    st.markdown(
        """
    <div class="corpus-stats-card">
        <div class="stat-item">
            <span class="stat-label">Documents</span>
            <span class="stat-value">5</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Total Pages</span>
            <span class="stat-value">127</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Storage Size</span>
            <span class="stat-value">23.4 MB</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Quick Upload Section
    st.markdown(
        '<span class="section-label">Quick Upload</span>', unsafe_allow_html=True
    )

    uploaded_refs = st.file_uploader(
        "Upload reference documents",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        key="corpus_upload",
        label_visibility="collapsed",
    )

    if uploaded_refs:
        st.caption(f"📦 {len(uploaded_refs)} file(s) selected")

    st.text_area(
        "Case Context",
        placeholder="Brief description of the case or verification context...",
        height=80,
        key="case_context",
        label_visibility="collapsed",
    )

    # Action Buttons
    st.markdown('<span class="section-label">Actions</span>', unsafe_allow_html=True)

    if st.button("📄 View Documents", key="view_docs", use_container_width=True):
        st.info("Document library modal would open here")

    if st.button("⚙️ Configure Corpus", key="config", use_container_width=True):
        st.info("Configuration modal")

    if st.button(
        "🗑️ Clear Corpus", key="clear", type="secondary", use_container_width=True
    ):
        st.warning("Confirm clear?")

    st.markdown("</div>", unsafe_allow_html=True)  # End sidebar styling

# ==================== RIGHT: MAIN CONTENT ====================
with main_col:
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    st.markdown(
        '<div class="content-title">Gemini-Powered Document Verification</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="content-subtitle">Complete each step to verify your document against the reference corpus using Google Gemini AI</div>',
        unsafe_allow_html=True,
    )

    # Workflow Cards Grid
    st.markdown('<div class="workflow-grid">', unsafe_allow_html=True)

    # Card 1: Upload
    st.markdown(
        """
    <div class="workflow-card">
        <div class="card-number">1</div>
        <div class="card-title">Upload</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Card 2: Chunking
    st.markdown(
        """
    <div class="workflow-card">
        <div class="card-number">2</div>
        <div class="card-title">Chunking</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Card 3: Gemini Verification (SPECIAL)
    st.markdown(
        """
    <div class="workflow-card workflow-card-gemini">
        <div class="card-number">3</div>
        <div class="card-title">Verify</div>
        <div class="gemini-icon-large">🔷</div>
        <div style="text-align: center; font-weight: 600; font-size: 1rem; color: var(--gemini-blue-dark); margin-bottom: 0.75rem;">
            Gemini AI
        </div>
        <div class="card-description" style="text-align: center;">
            Analyzes your content against reference documents using advanced AI verification
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Card 4: Export
    st.markdown(
        """
    <div class="workflow-card">
        <div class="card-number">4</div>
        <div class="card-title">Export</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)  # End workflow grid

    # Now add actual interactive elements in columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        uploaded_doc = st.file_uploader(
            "Document to verify",
            type=["pdf", "docx"],
            key="verify_doc",
            label_visibility="collapsed",
        )
        if uploaded_doc:
            st.markdown(
                '<div class="card-status status-ready">✓ Ready</div>',
                unsafe_allow_html=True,
            )
            st.caption(f"📄 {uploaded_doc.name}")
        else:
            st.markdown(
                '<div class="card-status status-waiting">⏳ Waiting</div>',
                unsafe_allow_html=True,
            )

    with col2:
        chunking = st.radio(
            "Splitting mode",
            ["Paragraph", "Sentence"],
            key="chunk_mode",
            label_visibility="collapsed",
        )
        st.markdown(
            f'<div class="card-status status-ready">✓ {chunking}</div>',
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            '<div class="card-status status-active">🔷 Corpus Ready</div>',
            unsafe_allow_html=True,
        )
        if st.button(
            "▶ Run Verification", type="primary", use_container_width=True, key="verify"
        ):
            st.success("Verification started!")

    with col4:
        export_format = st.selectbox(
            "Format",
            ["Word (Landscape)", "Word (Portrait)", "Excel", "CSV", "JSON"],
            key="export_format",
            label_visibility="collapsed",
        )

        if st.button("Generate", use_container_width=True, key="generate"):
            st.info("Generating document...")

        st.button(
            "⬇ Download",
            type="primary",
            use_container_width=True,
            disabled=True,
            key="download",
        )

    # ==================== RESULTS SECTION ====================
    st.markdown(
        """
    <div class="results-container">
        <div class="results-header">
            <div class="results-title">Gemini Verification Results</div>
            <div class="results-timestamp">Completed 45 seconds ago</div>
        </div>

        <div class="metrics-grid">
            <div class="metric-box">
                <div class="metric-value">124</div>
                <div class="metric-label">Total Chunks</div>
            </div>
            <div class="metric-box">
                <div class="metric-value">89</div>
                <div class="metric-label">Verified</div>
            </div>
            <div class="metric-box">
                <div class="metric-value">8.2</div>
                <div class="metric-label">Avg Score</div>
            </div>
            <div class="metric-box">
                <div class="metric-value">45s</div>
                <div class="metric-label">Time</div>
            </div>
            <div class="metric-box">
                <div class="metric-value" style="color: var(--success);">✓</div>
                <div class="metric-label">Complete</div>
            </div>
        </div>

        <div class="confidence-section">
            <h3 style="font-family: 'Lora', serif; font-size: 1.125rem; margin-bottom: 1.5rem; font-weight: 600;">
                Confidence Distribution
            </h3>

            <div class="confidence-item">
                <div class="confidence-header">
                    <span class="confidence-label">
                        <span style="color: var(--ff-green-400); font-size: 1.25rem;">●</span>
                        High Confidence (8-10)
                    </span>
                    <span class="confidence-value">54%</span>
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill fill-high" style="width: 54%;"></div>
                </div>
                <div class="confidence-count">67 chunks</div>
            </div>

            <div class="confidence-item">
                <div class="confidence-header">
                    <span class="confidence-label">
                        <span style="color: var(--warning); font-size: 1.25rem;">●</span>
                        Medium Confidence (5-7)
                    </span>
                    <span class="confidence-value">18%</span>
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill fill-medium" style="width: 18%;"></div>
                </div>
                <div class="confidence-count">22 chunks</div>
            </div>

            <div class="confidence-item">
                <div class="confidence-header">
                    <span class="confidence-label">
                        <span style="color: var(--error); font-size: 1.25rem;">●</span>
                        Low / Unverified
                    </span>
                    <span class="confidence-value">28%</span>
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill fill-low" style="width: 28%;"></div>
                </div>
                <div class="confidence-count">35 chunks - Review needed</div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Review Items as Expanders
    st.markdown('<div style="margin-top: 2rem;">', unsafe_allow_html=True)
    st.markdown(
        '<h3 style="font-family: Lora, serif; font-size: 1.125rem; margin-bottom: 1rem; font-weight: 600;">Items Requiring Review</h3>',
        unsafe_allow_html=True,
    )

    with st.expander("⚠️ Page 2, Item 4 - Low Confidence (4.2/10)", expanded=True):
        st.markdown("*Furthermore, the analysis indicates that market conditions...*")
        st.caption("**Issue:** Confidence score below threshold")
        st.button("View Full Details", key="detail1", use_container_width=True)

    with st.expander("⚠️ Page 3, Item 7 - No Reference Match"):
        st.markdown("*The plaintiff contends that statutory requirements...*")
        st.caption("**Issue:** No matching content in corpus")
        st.button("View Full Details", key="detail2", use_container_width=True)

    with st.expander("⚠️ Page 5, Item 2 - Conflicting Sources"):
        st.markdown("*According to the statute of limitations...*")
        st.caption("**Issue:** Multiple conflicting references found")
        st.button("View Full Details", key="detail3", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)  # End main content

# ==================== FOOTER ====================
st.markdown(
    """
<div class="freshfields-footer">
    <span>Powered by Gemini 2.5 Flash • Content Verification Tool v2.1 • Built for Demo</span>
</div>
""",
    unsafe_allow_html=True,
)
