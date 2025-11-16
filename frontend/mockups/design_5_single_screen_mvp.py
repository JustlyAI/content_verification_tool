"""
Design Mockup 5: Single-Screen MVP - Command Center Aesthetic
No tabs, everything visible, streamlined workflow

Design Philosophy: Bloomberg Terminal meets Luxury Control Panel
- Efficient single-screen layout
- Corpus as compact sidebar component
- Details in modals (not cluttering main view)
- Clear left-to-right workflow
"""

import streamlit as st

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
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:wght@300;400;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

    /* Color Variables - Premium Legal Palette */
    :root {
        --header-height: 80px;
        --sidebar-width: 320px;

        /* Light mode */
        --bg-main: #fafbfc;
        --bg-card: #ffffff;
        --bg-sidebar: #f5f6f8;
        --text-primary: #0f1419;
        --text-secondary: #536471;
        --text-muted: #8b98a5;
        --accent-gold: #c9a961;
        --accent-dark: #8b7243;
        --border-color: #e7e9eb;
        --border-light: #f0f2f4;
        --success: #059669;
        --warning: #f59e0b;
        --error: #dc2626;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07);
        --shadow-lg: 0 10px 24px -4px rgba(0, 0, 0, 0.08);
    }

    /* Dark mode */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-main: #15202b;
            --bg-card: #1e2732;
            --bg-sidebar: #192734;
            --text-primary: #e7e9ea;
            --text-secondary: #a1a8b0;
            --text-muted: #6e7681;
            --accent-gold: #f4d03f;
            --accent-dark: #c9a961;
            --border-color: #2f3b47;
            --border-light: #263340;
            --success: #10b981;
            --warning: #fbbf24;
            --error: #ef4444;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
            --shadow-lg: 0 10px 24px -4px rgba(0, 0, 0, 0.5);
        }
    }

    /* Global Reset */
    .main {
        background: var(--bg-main);
        padding: 0 !important;
        max-width: 100% !important;
    }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Typography */
    h1, h2, h3, h4 {
        font-family: 'IBM Plex Serif', serif;
        color: var(--text-primary);
        font-weight: 600;
        letter-spacing: -0.02em;
    }

    p, div, label, span, input, textarea {
        font-family: 'DM Sans', -apple-system, system-ui, sans-serif;
        color: var(--text-primary);
    }

    /* Compact Header */
    .compact-header {
        height: var(--header-height);
        background: var(--bg-card);
        border-bottom: 1px solid var(--border-color);
        padding: 0 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: sticky;
        top: 0;
        z-index: 100;
        box-shadow: var(--shadow-sm);
    }

    .header-left {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }

    .header-title {
        font-family: 'IBM Plex Serif', serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
        letter-spacing: -0.02em;
    }

    .header-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.375rem 0.875rem;
        background: rgba(5, 150, 105, 0.1);
        border: 1px solid rgba(5, 150, 105, 0.2);
        border-radius: 1.5rem;
        font-size: 0.8125rem;
        font-weight: 500;
        color: var(--success);
    }

    .status-dot {
        width: 6px;
        height: 6px;
        background: var(--success);
        border-radius: 50%;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(0.95); }
    }

    .header-badge {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.375rem 0.875rem;
        background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-dark) 100%);
        border-radius: 1.5rem;
        font-size: 0.6875rem;
        font-weight: 600;
        color: #000;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Layout Grid */
    .main-grid {
        display: grid;
        grid-template-columns: var(--sidebar-width) 1fr;
        min-height: calc(100vh - var(--header-height));
    }

    /* Sidebar - Corpus Component */
    .corpus-sidebar {
        background: var(--bg-sidebar);
        border-right: 1px solid var(--border-color);
        padding: 2rem 1.5rem;
        overflow-y: auto;
        height: calc(100vh - var(--header-height));
    }

    .sidebar-section {
        margin-bottom: 2rem;
    }

    .sidebar-label {
        font-size: 0.6875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-muted);
        margin-bottom: 0.75rem;
        display: block;
    }

    .corpus-status-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .corpus-status-active {
        border-left: 3px solid var(--success);
    }

    .corpus-status-inactive {
        border-left: 3px solid var(--text-muted);
    }

    .corpus-metric {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid var(--border-light);
    }

    .corpus-metric:last-child {
        border-bottom: none;
    }

    .corpus-metric-label {
        font-size: 0.8125rem;
        color: var(--text-secondary);
    }

    .corpus-metric-value {
        font-weight: 600;
        font-size: 0.875rem;
        color: var(--text-primary);
    }

    .mini-button {
        width: 100%;
        padding: 0.625rem 1rem;
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 0.375rem;
        font-size: 0.8125rem;
        font-weight: 500;
        color: var(--text-primary);
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: center;
        font-family: 'DM Sans', sans-serif;
    }

    .mini-button:hover {
        border-color: var(--accent-gold);
        background: var(--bg-main);
    }

    .mini-button-primary {
        background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-dark) 100%);
        border: none;
        color: #000;
        font-weight: 600;
    }

    .mini-button-primary:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }

    /* Main Content Area */
    .main-content {
        padding: 2rem;
        overflow-y: auto;
        height: calc(100vh - var(--header-height));
    }

    .section-title {
        font-family: 'IBM Plex Serif', serif;
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.01em;
    }

    .section-subtitle {
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin: 0 0 2rem 0;
    }

    /* Workflow Cards - Horizontal */
    .workflow-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.25rem;
        margin-bottom: 3rem;
    }

    .workflow-step {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 0.625rem;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .workflow-step:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }

    .workflow-step::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-gold) 0%, var(--accent-dark) 100%);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }

    .workflow-step:hover::before {
        transform: scaleX(1);
    }

    .step-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
    }

    .step-number {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-dark) 100%);
        color: #000;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.875rem;
        flex-shrink: 0;
    }

    .step-title {
        font-family: 'IBM Plex Serif', serif;
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }

    .step-status {
        display: inline-flex;
        align-items: center;
        gap: 0.375rem;
        padding: 0.25rem 0.625rem;
        border-radius: 1rem;
        font-size: 0.6875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-top: 0.75rem;
    }

    .status-ready {
        background: rgba(5, 150, 105, 0.1);
        color: var(--success);
        border: 1px solid rgba(5, 150, 105, 0.2);
    }

    .status-pending {
        background: rgba(245, 158, 11, 0.1);
        color: var(--warning);
        border: 1px solid rgba(245, 158, 11, 0.2);
    }

    .status-waiting {
        background: rgba(107, 114, 128, 0.1);
        color: var(--text-muted);
        border: 1px solid rgba(107, 114, 128, 0.2);
    }

    /* Buttons */
    .stButton > button {
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        border-radius: 0.375rem;
        transition: all 0.2s ease;
        border: none;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-dark) 100%);
        color: #000;
        font-weight: 600;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }

    .stButton > button[kind="secondary"] {
        background: var(--bg-card);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }

    /* Results Section */
    .results-container {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 0.75rem;
        padding: 2rem;
        margin-top: 2rem;
    }

    .results-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border-color);
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 1.25rem;
        margin-bottom: 2rem;
    }

    .metric-box {
        text-align: center;
        padding: 1.25rem 1rem;
        background: var(--bg-main);
        border: 1px solid var(--border-light);
        border-radius: 0.5rem;
        transition: all 0.2s ease;
    }

    .metric-box:hover {
        border-color: var(--accent-gold);
        box-shadow: var(--shadow-sm);
    }

    .metric-value {
        font-family: 'IBM Plex Serif', serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
        margin-bottom: 0.375rem;
    }

    .metric-label {
        font-size: 0.75rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }

    /* Confidence Bars */
    .confidence-section {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
    }

    .confidence-item {
        margin-bottom: 1.5rem;
    }

    .confidence-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .confidence-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--text-primary);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .confidence-value {
        font-weight: 700;
        font-size: 0.875rem;
    }

    .confidence-bar {
        height: 8px;
        background: var(--border-light);
        border-radius: 4px;
        overflow: hidden;
    }

    .confidence-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .fill-success { background: linear-gradient(90deg, var(--success) 0%, #10b981 100%); }
    .fill-warning { background: linear-gradient(90deg, var(--warning) 0%, #fbbf24 100%); }
    .fill-error { background: linear-gradient(90deg, var(--error) 0%, #ef4444 100%); }

    .confidence-count {
        font-size: 0.75rem;
        color: var(--text-secondary);
        margin-top: 0.25rem;
    }

    /* File Uploader */
    .stFileUploader {
        border: 2px dashed var(--border-color);
        border-radius: 0.5rem;
        background: var(--bg-main);
        padding: 1rem;
    }

    .stFileUploader:hover {
        border-color: var(--accent-gold);
    }

    /* Modal styles */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        backdrop-filter: blur(4px);
    }

    .modal-content {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 0.75rem;
        max-width: 600px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
        box-shadow: var(--shadow-lg);
    }

    .modal-header {
        padding: 1.5rem;
        border-bottom: 1px solid var(--border-color);
    }

    .modal-body {
        padding: 1.5rem;
    }

    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: var(--border-color);
        margin: 2rem 0;
    }

    /* Smooth transitions */
    * {
        transition-property: background-color, border-color, color, box-shadow, transform;
        transition-duration: 0.2s;
        transition-timing-function: ease-in-out;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="compact-header">
    <div class="header-left">
        <div class="header-title">Content Verification</div>
        <div class="header-status">
            <span class="status-dot"></span>
            <span>Connected</span>
        </div>
    </div>
    <div class="header-badge">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
        </svg>
        Powered by Gemini
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== MAIN LAYOUT ====================
st.markdown('<div class="main-grid">', unsafe_allow_html=True)

# LEFT SIDEBAR - CORPUS
st.markdown('<div class="corpus-sidebar">', unsafe_allow_html=True)

st.markdown('<span class="sidebar-label">Reference Corpus</span>', unsafe_allow_html=True)

# Corpus status
st.markdown("""
<div class="corpus-status-card corpus-status-active">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
        <span style="font-weight: 600; font-size: 0.875rem; color: var(--text-primary);">Active Corpus</span>
        <span style="font-size: 0.75rem; color: var(--success); font-weight: 600;">✓ READY</span>
    </div>
    <div class="corpus-metric">
        <span class="corpus-metric-label">Documents</span>
        <span class="corpus-metric-value">5</span>
    </div>
    <div class="corpus-metric">
        <span class="corpus-metric-label">Pages</span>
        <span class="corpus-metric-value">127</span>
    </div>
    <div class="corpus-metric">
        <span class="corpus-metric-label">Storage</span>
        <span class="corpus-metric-value">23.4 MB</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Actions
st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)

if st.button("📄 View Documents", key="view_docs", use_container_width=True):
    st.info("Modal would open here showing document list")

if st.button("➕ Add Documents", key="add_docs", type="primary", use_container_width=True):
    st.info("Upload interface")

st.markdown('</div>', unsafe_allow_html=True)

# Quick upload section
st.markdown('<span class="sidebar-label" style="margin-top: 1.5rem; display: block;">Quick Upload</span>', unsafe_allow_html=True)

uploaded_corpus = st.file_uploader(
    "Upload references",
    type=["pdf", "docx"],
    accept_multiple_files=True,
    key="corpus_upload",
    label_visibility="collapsed"
)

if uploaded_corpus:
    st.caption(f"📦 {len(uploaded_corpus)} file(s) selected")

st.text_area(
    "Case Context",
    placeholder="Brief context...",
    height=80,
    key="case_context",
    label_visibility="collapsed"
)

if st.button("Upload & Index", key="upload_corpus", use_container_width=True):
    st.success("Processing...")

st.markdown('</div>', unsafe_allow_html=True)  # End sidebar

# RIGHT CONTENT - VERIFICATION WORKFLOW
st.markdown('<div class="main-content">', unsafe_allow_html=True)

st.markdown('<h2 class="section-title">Verification Workflow</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">Complete each step to verify your document against the reference corpus</p>', unsafe_allow_html=True)

# Workflow steps
st.markdown('<div class="workflow-grid">', unsafe_allow_html=True)

# Step 1: Upload
st.markdown("""
<div class="workflow-step">
    <div class="step-header">
        <div class="step-number">1</div>
        <div class="step-title">Upload</div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    uploaded_doc = st.file_uploader(
        "Document",
        type=["pdf", "docx"],
        key="verify_upload",
        label_visibility="collapsed"
    )
    if uploaded_doc:
        st.markdown('<div class="step-status status-ready">✓ Ready</div>', unsafe_allow_html=True)
        st.caption(f"📄 {uploaded_doc.name}")
        st.button("Process", type="primary", use_container_width=True, key="process")
    else:
        st.markdown('<div class="step-status status-waiting">⏳ Waiting</div>', unsafe_allow_html=True)

# Step 2: Chunking
with col2:
    st.markdown("""
    <div class="step-header" style="margin-top: 1.5rem;">
        <div class="step-number">2</div>
        <div class="step-title">Chunking</div>
    </div>
    """, unsafe_allow_html=True)

    chunking = st.radio(
        "Mode",
        ["Paragraph", "Sentence"],
        key="chunk_mode",
        label_visibility="collapsed"
    )
    st.markdown(f'<div class="step-status status-ready">✓ {chunking}</div>', unsafe_allow_html=True)

# Step 3: Verify
with col3:
    st.markdown("""
    <div class="step-header" style="margin-top: 1.5rem;">
        <div class="step-number">3</div>
        <div class="step-title">Verify</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="step-status status-ready">✓ Corpus Ready</div>', unsafe_allow_html=True)
    st.caption("AI verification enabled")
    st.button("▶ Run Verification", type="primary", use_container_width=True, key="verify")

# Step 4: Export
with col4:
    st.markdown("""
    <div class="step-header" style="margin-top: 1.5rem;">
        <div class="step-number">4</div>
        <div class="step-title">Export</div>
    </div>
    """, unsafe_allow_html=True)

    export_format = st.selectbox(
        "Format",
        ["Word (L)", "Word (P)", "Excel", "CSV", "JSON"],
        key="export",
        label_visibility="collapsed"
    )
    st.button("Generate", use_container_width=True, key="gen")
    st.button("⬇ Download", type="primary", use_container_width=True, disabled=True, key="dl")

st.markdown('</div>', unsafe_allow_html=True)  # End workflow grid

# Results Section
st.markdown("""
<div class="results-container">
    <div class="results-header">
        <h3 class="section-title" style="margin: 0;">Verification Results</h3>
        <span style="font-size: 0.875rem; color: var(--text-secondary);">Completed 45 seconds ago</span>
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
        <div>
            <h4 style="font-size: 1rem; margin-bottom: 1.25rem; font-weight: 600;">Confidence Distribution</h4>

            <div class="confidence-item">
                <div class="confidence-header">
                    <span class="confidence-label">
                        <span style="color: var(--success);">●</span> High Confidence (8-10)
                    </span>
                    <span class="confidence-value">54%</span>
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill fill-success" style="width: 54%;"></div>
                </div>
                <div class="confidence-count">67 chunks</div>
            </div>

            <div class="confidence-item">
                <div class="confidence-header">
                    <span class="confidence-label">
                        <span style="color: var(--warning);">●</span> Medium Confidence (5-7)
                    </span>
                    <span class="confidence-value">18%</span>
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill fill-warning" style="width: 18%;"></div>
                </div>
                <div class="confidence-count">22 chunks</div>
            </div>

            <div class="confidence-item">
                <div class="confidence-header">
                    <span class="confidence-label">
                        <span style="color: var(--error);">●</span> Low/Unverified
                    </span>
                    <span class="confidence-value">28%</span>
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill fill-error" style="width: 28%;"></div>
                </div>
                <div class="confidence-count">35 chunks - Review needed</div>
            </div>
        </div>

        <div>
            <h4 style="font-size: 1rem; margin-bottom: 1.25rem; font-weight: 600;">Items Requiring Review</h4>
""", unsafe_allow_html=True)

# Review items as expanders
with st.expander("⚠️ Page 2, Item 4 - Low Confidence", expanded=True):
    st.markdown("*Furthermore, the analysis indicates that...*")
    st.caption("**Issue:** Confidence score 4.2/10")
    st.button("View Details", key="d1", use_container_width=True)

with st.expander("⚠️ Page 3, Item 7 - No Match"):
    st.markdown("*The plaintiff contends...*")
    st.caption("**Issue:** No reference match")
    st.button("View Details", key="d2", use_container_width=True)

with st.expander("⚠️ Page 5, Item 2 - Conflicting"):
    st.markdown("*According to the statute...*")
    st.caption("**Issue:** Multiple conflicting sources")
    st.button("View Details", key="d3", use_container_width=True)

st.markdown("""
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # End main content
st.markdown('</div>', unsafe_allow_html=True)  # End main grid

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; color: var(--text-muted); font-size: 0.8125rem;">
    Content Verification Tool v2.0 • Built for Freshfields
</div>
""", unsafe_allow_html=True)
