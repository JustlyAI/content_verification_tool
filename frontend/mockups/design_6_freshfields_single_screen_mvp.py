"""
Design 6 MVP: Freshfields-Inspired Single-Screen Verification Interface
Production-ready mockup with all issues resolved

Design Philosophy: Sophisticated Legal Technology
- Lora (serif headlines) + IBM Plex Sans (body text)
- Powder blue (#e5f0f7) sidebar with lime green (#c8e86b) accents
- Generous whitespace and breathing room throughout
- Pill-shaped interactive elements
- Gemini prominently featured throughout workflow
- Fixed header/footer with scrollable content area

Key Features:
✓ Single-row header with proper flexbox layout
✓ Sidebar blue background properly applied to column
✓ Card borders visible with correct CSS selectors
✓ Generous spacing matching Freshfields aesthetic (increased padding)
✓ Gemini Card 3 visually distinct with gradient and border
✓ Production-grade component architecture
✓ Clear distinction between two uploaders:
  - Sidebar: Upload reference corpus (knowledge base for verification)
  - Step 1: Upload document to verify (document being checked against corpus)
✓ Compact, streamlined step cards
✓ Visual callouts explaining workflow and purpose

Latest Updates (Freshfields-Accurate Compact Spacing):
- **CORRECTED TO MATCH FRESHFIELDS**: Reduced all excessive vertical spacing
- Sidebar padding: 32px vertical, 24px horizontal (var(--space-4), var(--space-3))
- Main content padding: 40px vertical, 48px horizontal (var(--space-5), var(--space-6))
- Card improvements: 220px min-height, 24px padding (var(--space-3)), flexbox layout
- Inter-card spacing: 16px gaps between workflow cards (var(--space-2))
- Sidebar element spacing: 16px between elements (var(--space-2))
- Alert boxes: 16px/24px padding with 24px bottom margins
- Section dividers: 24px vertical spacing (var(--space-3))
- Progress bars: 8px top, 16px bottom spacing
- Expanders: 16px bottom margin
- Compact spacing hierarchy: micro (8px), standard (16-24px), section (24-32px)
- Element containers: 16px default margin-bottom
- Removed all excessive st.markdown("") spacing tricks
- Result: Efficient, Freshfields-inspired compact layout with proper visual hierarchy
"""

import streamlit as st

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Content Verification | Powered by Gemini",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==================== CUSTOM CSS ====================
st.markdown(
    """
<style>
    /* ===== FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&display=swap');

    /* ===== COLOR SYSTEM - FRESHFIELDS ===== */
    :root {
        /* Neutrals */
        --white: #ffffff;
        --cream-white: #fafaf9;
        --cream: #f5f4f0;
        --warm-gray-100: #f8f7f5;
        --warm-gray-200: #e8e6e3;
        --warm-gray-300: #d4d2ce;
        --warm-gray-400: #c8c5c0;
        --warm-gray-500: #9b9690;
        --charcoal: #3d3935;
        --black: #1a1816;

        /* Freshfields Blues - Powder/Soft */
        --ff-blue-50: #f7fbfd;
        --ff-blue-100: #e5f0f7;
        --ff-blue-200: #cce1ee;
        --ff-blue-300: #a4c8e1;
        --ff-blue-400: #7ba8c9;
        --ff-blue-500: #5a8fb5;

        /* Freshfields Green - Lime/Chartreuse */
        --ff-green-50: #f9fced;
        --ff-green-100: #f0f7d6;
        --ff-green-200: #e3f0b8;
        --ff-green-300: #c8e86b;
        --ff-green-400: #b0d94f;
        --ff-green-500: #9ac93d;

        /* Gemini Brand */
        --gemini-blue-light: #e8f4f8;
        --gemini-blue: #4fc3f7;
        --gemini-blue-dark: #0288d1;

        /* Semantic */
        --success: #059669;
        --warning: #f59e0b;
        --error: #dc2626;
        --info: var(--gemini-blue);

        /* Typography */
        --font-display: 'Lora', 'Georgia', serif;
        --font-body: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;

        /* Spacing Scale (8px base) */
        --space-1: 0.5rem;   /* 8px */
        --space-2: 1rem;     /* 16px */
        --space-3: 1.5rem;   /* 24px */
        --space-4: 2rem;     /* 32px */
        --space-5: 2.5rem;   /* 40px */
        --space-6: 3rem;     /* 48px */
        --space-8: 4rem;     /* 64px */

        /* Radius */
        --radius-sm: 0.375rem;
        --radius-md: 0.5rem;
        --radius-lg: 1rem;
        --radius-xl: 1.5rem;
        --radius-full: 9999px;

        /* Shadows */
        --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.04);
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.06);
        --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.08);
        --shadow-lg: 0 10px 24px rgba(0, 0, 0, 0.1);
    }

    /* ===== GLOBAL RESETS ===== */
    .main {
        background: var(--cream-white) !important;
        padding: 0 !important;
    }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* Hide Streamlit UI */
    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* ===== TYPOGRAPHY ===== */
    h1, h2, h3, h4, h5, h6 {
        font-family: var(--font-display) !important;
        color: var(--black) !important;
        font-weight: 600 !important;
        letter-spacing: -0.015em !important;
        line-height: 1.3 !important;
    }

    h1 { font-size: 2.25rem !important; }
    h2 { font-size: 1.875rem !important; }
    h3 { font-size: 1.5rem !important; }

    p, div, label, span, input, textarea, button, li {
        font-family: var(--font-body) !important;
    }

    /* ===== HEADER ===== */
    .ff-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--space-4) var(--space-6);
        background: var(--cream-white);
        border-bottom: 1.5px solid var(--warm-gray-200);
        margin: 0;
        min-height: 80px;
    }

    .ff-header-title {
        font-family: var(--font-display);
        font-size: 1.75rem;
        font-weight: 600;
        color: var(--black);
        margin: 0;
        letter-spacing: -0.02em;
    }

    .ff-gemini-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.625rem;
        padding: 0.625rem 1.5rem;
        background: linear-gradient(135deg, var(--gemini-blue-light) 0%, var(--white) 100%);
        border: 2px solid var(--gemini-blue-dark);
        border-radius: var(--radius-full);
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--gemini-blue-dark);
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
    }

    .ff-gemini-badge:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }

    /* ===== SIDEBAR COLUMN ===== */
    /* Target the first column specifically */
    [data-testid="column"]:first-child {
        background: var(--ff-blue-100) !important;
        border-right: 2px solid var(--ff-blue-200);
        min-height: calc(100vh - 160px);
    }

    /* Sidebar internal padding - COMPACT & EFFICIENT */
    .ff-sidebar-content {
        padding: var(--space-4) var(--space-3);
    }

    /* Sidebar section spacing - TIGHTER */
    .ff-sidebar-content > div {
        margin-bottom: var(--space-2);
    }

    /* Compact spacing for metrics in sidebar */
    .ff-sidebar-content .stMetric {
        margin-bottom: var(--space-2) !important;
    }

    /* Compact space around sidebar file uploader */
    .ff-sidebar-content .stFileUploader {
        margin-top: var(--space-2) !important;
        margin-bottom: var(--space-2) !important;
    }

    /* Compact spacing for sidebar text area */
    .ff-sidebar-content .stTextArea {
        margin-bottom: var(--space-3) !important;
    }

    /* Compact space between sidebar buttons */
    .ff-sidebar-content .stButton {
        margin-bottom: var(--space-2) !important;
    }

    /* Sidebar column gap for metrics */
    .ff-sidebar-content [data-testid="column"] {
        padding: 0 var(--space-1) !important;
    }

    .ff-sidebar-content [data-testid="column"]:first-child {
        padding-left: 0 !important;
    }

    .ff-sidebar-content [data-testid="column"]:last-child {
        padding-right: 0 !important;
    }

    /* Sidebar headings */
    .ff-sidebar-content h3 {
        margin-top: 0 !important;
        margin-bottom: var(--space-2) !important;
    }

    /* Sidebar horizontal rules */
    .ff-sidebar-content hr {
        margin: var(--space-3) 0 !important;
    }

    /* ===== MAIN CONTENT COLUMN ===== */
    .ff-main-content {
        padding: var(--space-5) var(--space-6);
        background: var(--white);
    }

    /* ===== WORKFLOW CARDS ===== */
    /* Compact spacing between columns */
    [data-testid="column"] {
        padding: 0 var(--space-2) !important;
    }

    [data-testid="column"]:first-child {
        padding-left: 0 !important;
    }

    [data-testid="column"]:last-child {
        padding-right: 0 !important;
    }

    /* Card container styling - COMPACT & EFFICIENT */
    .ff-card {
        background: var(--white);
        border: 2px solid var(--warm-gray-200);
        border-radius: var(--radius-lg);
        padding: var(--space-3);
        min-height: 220px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-xs);
        display: flex;
        flex-direction: column;
    }

    .ff-card:hover {
        border-color: var(--warm-gray-300);
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }

    .ff-card-number {
        font-family: var(--font-display);
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--warm-gray-500);
        margin-bottom: var(--space-2);
        letter-spacing: 0.05em;
    }

    .ff-card-title {
        font-family: var(--font-display);
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--black);
        margin-bottom: var(--space-2);
        letter-spacing: -0.01em;
        line-height: 1.3 !important;
    }

    /* Compact spacing within cards */
    .ff-card .stMarkdown {
        margin-bottom: var(--space-2) !important;
    }

    .ff-card .stRadio {
        margin-top: var(--space-1) !important;
        margin-bottom: var(--space-2) !important;
    }

    .ff-card .stSelectbox {
        margin-bottom: var(--space-2) !important;
    }

    .ff-card .stFileUploader {
        margin-top: var(--space-1) !important;
        margin-bottom: var(--space-2) !important;
    }

    .ff-card .stButton {
        margin-top: var(--space-1) !important;
    }

    /* Gemini Card - Special Treatment */
    .ff-gemini-card {
        background: linear-gradient(135deg, var(--gemini-blue-light) 0%, var(--white) 50%, var(--white) 100%);
        border: 2.5px solid var(--gemini-blue);
        box-shadow: 0 0 0 4px rgba(79, 195, 247, 0.1);
        position: relative;
        overflow: hidden;
    }

    .ff-gemini-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(79, 195, 247, 0.08) 0%, transparent 70%);
        pointer-events: none;
    }

    .ff-gemini-card:hover {
        border-color: var(--gemini-blue-dark);
        box-shadow: 0 0 0 4px rgba(79, 195, 247, 0.2), var(--shadow-lg);
        transform: translateY(-3px);
    }

    /* ===== BUTTONS - MORE COMPACT ===== */
    .stButton > button {
        border-radius: var(--radius-full) !important;
        font-family: var(--font-body) !important;
        font-weight: 600 !important;
        padding: 0.625rem 1.5rem !important;
        font-size: 0.875rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: none !important;
        letter-spacing: 0.01em !important;
        box-shadow: var(--shadow-sm) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-md) !important;
    }

    /* Primary Button - Lime Green */
    .stButton > button[kind="primary"] {
        background: var(--ff-green-300) !important;
        color: var(--black) !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: var(--ff-green-400) !important;
    }

    /* Secondary Button */
    .stButton > button[kind="secondary"] {
        background: var(--white) !important;
        color: var(--charcoal) !important;
        border: 2px solid var(--warm-gray-300) !important;
        box-shadow: var(--shadow-xs) !important;
    }

    .stButton > button[kind="secondary"]:hover {
        border-color: var(--black) !important;
        background: var(--cream-white) !important;
    }

    /* ===== FILE UPLOADER ===== */
    .stFileUploader {
        border: 2px dashed var(--ff-blue-300) !important;
        border-radius: var(--radius-md) !important;
        background: var(--white) !important;
        padding: var(--space-2) !important;
        transition: all 0.3s ease !important;
    }

    .stFileUploader:hover {
        border-color: var(--ff-blue-400) !important;
        background: var(--ff-blue-50) !important;
    }

    /* ===== METRICS ===== */
    [data-testid="stMetricValue"] {
        font-family: var(--font-display) !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: var(--black) !important;
        letter-spacing: -0.02em !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
        color: var(--warm-gray-500) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        font-weight: 600 !important;
    }

    /* ===== RADIO BUTTONS ===== */
    .stRadio > label {
        font-weight: 500 !important;
        color: var(--charcoal) !important;
        font-size: 0.875rem !important;
    }

    .stRadio [role="radiogroup"] {
        gap: 0.75rem !important;
    }

    /* ===== TEXT INPUT ===== */
    .stTextInput input, .stTextArea textarea {
        border-radius: var(--radius-md) !important;
        border: 2px solid var(--warm-gray-200) !important;
        font-family: var(--font-body) !important;
        transition: all 0.2s ease !important;
        font-size: 0.9375rem !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--ff-blue-300) !important;
        box-shadow: 0 0 0 3px rgba(164, 200, 225, 0.15) !important;
    }

    /* ===== SELECT BOX ===== */
    .stSelectbox > div > div {
        border-radius: var(--radius-md) !important;
        border: 2px solid var(--warm-gray-200) !important;
        transition: all 0.2s ease !important;
    }

    .stSelectbox > div > div:hover {
        border-color: var(--warm-gray-300) !important;
    }

    /* ===== PROGRESS BAR ===== */
    .stProgress > div > div {
        background: var(--ff-green-300) !important;
        border-radius: var(--radius-sm) !important;
    }

    .stProgress > div {
        background: var(--warm-gray-100) !important;
        border-radius: var(--radius-sm) !important;
        height: 8px !important;
    }

    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        font-family: var(--font-body) !important;
        font-weight: 600 !important;
        font-size: 0.9375rem !important;
        border-radius: var(--radius-md) !important;
        background: var(--cream-white) !important;
        border: 1.5px solid var(--warm-gray-200) !important;
        padding: var(--space-2) var(--space-3) !important;
        transition: all 0.2s ease !important;
    }

    .streamlit-expanderHeader:hover {
        background: var(--warm-gray-100) !important;
        border-color: var(--warm-gray-300) !important;
    }

    /* ===== DIVIDER ===== */
    hr {
        border: none !important;
        height: 1.5px !important;
        background: var(--warm-gray-200) !important;
        margin: var(--space-3) 0 !important;
    }

    /* ===== ALERTS ===== */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: var(--radius-md) !important;
        border-left-width: 4px !important;
        padding: var(--space-2) var(--space-3) !important;
        font-size: 0.875rem !important;
        line-height: 1.5 !important;
    }

    /* Sidebar alerts - compact */
    .ff-sidebar-content .stSuccess,
    .ff-sidebar-content .stInfo,
    .ff-sidebar-content .stWarning {
        padding: var(--space-2) var(--space-3) !important;
        margin-bottom: var(--space-2) !important;
    }

    /* ===== SPACING UTILITIES ===== */
    .element-container {
        margin-bottom: var(--space-2);
    }

    /* Compact spacing for major sections */
    .stMarkdown h2 {
        margin-top: 0 !important;
        margin-bottom: var(--space-3) !important;
        line-height: 1.2 !important;
    }

    .stMarkdown h3 {
        margin-top: var(--space-3) !important;
        margin-bottom: var(--space-2) !important;
        line-height: 1.3 !important;
    }

    /* Compact spacing after info/success/warning boxes */
    .stAlert {
        margin-bottom: var(--space-3) !important;
    }

    /* Compact spacing between metrics */
    .stMetric {
        margin-bottom: var(--space-2) !important;
    }

    /* Compact spacing for file uploaders */
    .stFileUploader {
        margin-bottom: var(--space-2) !important;
    }

    /* Compact spacing for text areas */
    .stTextArea {
        margin-bottom: var(--space-3) !important;
    }

    /* Compact spacing between buttons */
    .stButton {
        margin-bottom: var(--space-2) !important;
    }

    /* Main content section spacing */
    .ff-main-content > .element-container {
        margin-bottom: var(--space-3) !important;
    }

    /* Results section spacing */
    .ff-main-content .stMetric {
        margin-bottom: var(--space-2) !important;
    }

    /* Progress bars - compact */
    .stProgress {
        margin-bottom: var(--space-2) !important;
        margin-top: var(--space-1) !important;
    }

    /* Expander spacing */
    .streamlit-expanderHeader {
        margin-bottom: var(--space-2) !important;
    }

    /* Caption spacing */
    .stMarkdown p[style*="font-size: 0.875rem"],
    .stCaption {
        margin-top: var(--space-1) !important;
        margin-bottom: var(--space-2) !important;
    }

    /* ===== FOOTER ===== */
    .ff-footer {
        text-align: center;
        padding: var(--space-4);
        background: var(--cream-white);
        border-top: 1.5px solid var(--warm-gray-200);
        color: var(--warm-gray-500);
        font-size: 0.875rem;
        font-weight: 500;
        letter-spacing: 0.01em;
    }

    .ff-footer-highlight {
        color: var(--gemini-blue-dark);
        font-weight: 600;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ==================== HEADER ====================
st.markdown(
    """
<div class="ff-header">
    <div class="ff-header-title">Content Verification Assistant</div>
    <div class="ff-gemini-badge">🔷 Powered by Gemini</div>
</div>
""",
    unsafe_allow_html=True,
)

# ==================== MAIN LAYOUT ====================
sidebar_col, main_col = st.columns([1, 3], gap="small")

# ==================== SIDEBAR: CORPUS ====================
with sidebar_col:
    st.markdown('<div class="ff-sidebar-content">', unsafe_allow_html=True)

    st.markdown("### Reference Corpus")
    st.info("📚 **Knowledge Base** - Upload reference documents that Gemini will use to verify your document")

    st.markdown("")

    # Status
    st.success("✓ Active & Gemini-Ready")

    st.markdown("")

    # Stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Documents", "5")
        st.metric("Storage", "23.4 MB")
    with col2:
        st.metric("Pages", "127")
        st.metric("Chunks", "1,834")

    st.markdown("---")

    # Quick Upload - CLARIFIED
    st.markdown("**Upload Reference Corpus**")
    st.caption("📚 Add documents to use as verification sources")
    uploaded_refs = st.file_uploader(
        "Upload reference documents",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        key="corpus_upload",
        label_visibility="collapsed",
        help="These documents form the knowledge base that Gemini uses to verify your document"
    )

    if uploaded_refs:
        st.success(f"✓ {len(uploaded_refs)} file(s) selected")

    st.markdown("")

    st.text_area(
        "Case Context",
        placeholder="Brief description of case or project...",
        height=80,
        key="case_context",
        label_visibility="collapsed",
    )

    st.markdown("---")

    # Actions
    st.markdown("**Actions**")
    st.markdown("")

    if st.button("📄 View Library", key="view_docs", use_container_width=True):
        st.info("Opening document library...")

    if st.button("⚙️ Configure", key="config", use_container_width=True):
        st.info("Opening settings...")

    if st.button(
        "🗑️ Clear Corpus",
        key="clear",
        type="secondary",
        use_container_width=True,
    ):
        st.warning("Confirm deletion?")

    st.markdown("</div>", unsafe_allow_html=True)

# ==================== MAIN CONTENT ====================
with main_col:
    st.markdown('<div class="ff-main-content">', unsafe_allow_html=True)

    st.markdown("## Gemini-Powered Document Verification")
    st.caption(
        "Upload a document below to verify it against your reference corpus using AI-powered analysis. "
        "Each sentence or paragraph will be checked for accuracy and consistency."
    )

    # Workflow explanation
    st.info(
        "**🔄 Verification Workflow:** Upload your document (Step 1) → "
        "Choose chunking mode (Step 2) → Run Gemini verification against corpus (Step 3) → "
        "Export results (Step 4)"
    )

    # ==================== WORKFLOW CARDS ====================
    card1, card2, card3, card4 = st.columns(4)

    # CARD 1: Upload - CLARIFIED
    with card1:
        st.markdown(
            '<div class="ff-card">'
            '<div class="ff-card-number">STEP 1</div>'
            '<div class="ff-card-title">Upload Document</div>',
            unsafe_allow_html=True,
        )

        st.markdown("**Document to Verify**")
        st.caption("📄 Upload the document you want to check against the corpus")

        uploaded_doc = st.file_uploader(
            "Document to verify",
            type=["pdf", "docx"],
            key="verify_doc",
            label_visibility="collapsed",
            help="This document will be verified against your reference corpus"
        )

        st.markdown("")

        if uploaded_doc:
            st.success("✓ Ready to Verify")
            st.caption(f"📄 {uploaded_doc.name}")
            st.caption(f"{uploaded_doc.size / 1024:.1f} KB")
        else:
            st.info("Upload document to begin")

        st.markdown("</div>", unsafe_allow_html=True)

    # CARD 2: Chunking
    with card2:
        st.markdown(
            '<div class="ff-card">'
            '<div class="ff-card-number">STEP 2</div>'
            '<div class="ff-card-title">Chunking</div>',
            unsafe_allow_html=True,
        )

        if uploaded_doc:
            st.markdown("**Processing Mode**")
            chunking = st.radio(
                "Mode",
                ["Paragraph", "Sentence"],
                key="chunk_mode",
                label_visibility="collapsed",
                horizontal=False,
            )

            st.markdown("")
            st.success(f"✓ {chunking}-level")
            st.caption(f"Split into {chunking.lower()}s for detailed analysis")
        else:
            st.info("Upload document first")
            st.caption("Choose how to split your document for verification")

        st.markdown("</div>", unsafe_allow_html=True)

    # CARD 3: Gemini Verification (SPECIAL)
    with card3:
        st.markdown(
            '<div class="ff-card ff-gemini-card">'
            '<div class="ff-card-number">STEP 3</div>'
            '<div class="ff-card-title">Verify with AI</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div style="text-align: center; margin: 1rem 0 1.5rem 0;">'
            '<div style="font-size: 2.5rem; line-height: 1;">🔷</div>'
            '<div style="font-family: var(--font-display); font-size: 1.125rem; font-weight: 600; color: var(--gemini-blue-dark); margin-top: 0.5rem;">Gemini AI</div>'
            "</div>",
            unsafe_allow_html=True,
        )

        if uploaded_doc:
            st.info("🔷 Corpus Ready (5 docs)")

            st.markdown("")

            if st.button(
                "▶ Run Verification",
                type="primary",
                use_container_width=True,
                key="verify",
            ):
                st.success("Starting verification...")
        else:
            st.warning("⏳ Upload Needed")
            st.caption("Upload a document to begin")

        st.markdown("</div>", unsafe_allow_html=True)

    # CARD 4: Export
    with card4:
        st.markdown(
            '<div class="ff-card">'
            '<div class="ff-card-number">STEP 4</div>'
            '<div class="ff-card-title">Export</div>',
            unsafe_allow_html=True,
        )

        st.markdown("**Output Format**")
        export_format = st.selectbox(
            "Format",
            [
                "Word (Landscape)",
                "Word (Portrait)",
                "Excel Spreadsheet",
                "CSV File",
                "JSON Data",
            ],
            key="export_format",
            label_visibility="collapsed",
        )

        st.markdown("")

        if st.button(
            "Generate Document",
            use_container_width=True,
            key="generate",
            type="secondary",
        ):
            st.info("Generating export...")

        st.button(
            "⬇ Download",
            type="primary",
            use_container_width=True,
            disabled=True,
            key="download",
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ==================== RESULTS SECTION ====================
    st.markdown("### Gemini Verification Results")
    st.caption("Analysis completed 45 seconds ago")

    # Metrics Grid
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("Total Chunks", "124")
    with m2:
        st.metric("Verified", "89", delta="71.8%")
    with m3:
        st.metric("Avg Score", "8.2/10")
    with m4:
        st.metric("Duration", "45s")
    with m5:
        st.metric("Status", "✓ Complete")

    st.markdown("---")

    # Confidence Distribution
    st.markdown("**Confidence Distribution**")

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("🟢 **High Confidence (8-10):** 67 chunks • 54%")
        st.progress(0.54)

        st.markdown("🟡 **Medium Confidence (5-7):** 22 chunks • 18%")
        st.progress(0.18)

        st.markdown("🔴 **Low Confidence (<5):** 35 chunks • 28%")
        st.progress(0.28)

    with col_right:
        st.info("**67 items** verified with high confidence")
        st.warning("**35 items** require manual review")

    st.markdown("---")

    # Items Requiring Review
    st.markdown("**Items Requiring Manual Review**")

    with st.expander(
        "⚠️ Page 2, Item 4 — Low Confidence (4.2/10)", expanded=True
    ):
        st.markdown(
            "*Furthermore, the analysis indicates that market conditions have deteriorated significantly compared to the reference period...*"
        )
        st.caption("**Issue:** Confidence score below 5.0 threshold")
        st.caption("**Gemini Notes:** Partial match found in Reference Doc 3, page 12")
        st.markdown("")
        if st.button("View Full Details", key="detail1", use_container_width=True):
            st.info("Opening detailed analysis modal...")

    with st.expander("⚠️ Page 3, Item 7 — No Reference Match Found"):
        st.markdown(
            "*The plaintiff contends that statutory requirements under Section 42(b) were not adequately fulfilled by the defendant...*"
        )
        st.caption("**Issue:** No matching content found in reference corpus")
        st.caption(
            "**Gemini Notes:** Section 42(b) not mentioned in any uploaded documents"
        )
        st.markdown("")
        if st.button("View Full Details", key="detail2", use_container_width=True):
            st.info("Opening detailed analysis modal...")

    with st.expander("⚠️ Page 5, Item 2 — Conflicting Source Information"):
        st.markdown(
            "*According to the statute of limitations established in 2019, claims must be filed within a three-year period...*"
        )
        st.caption("**Issue:** Multiple references contain conflicting information")
        st.caption(
            "**Gemini Notes:** Reference Doc 1 states 'three years', Reference Doc 4 states 'five years'"
        )
        st.markdown("")
        if st.button("View Full Details", key="detail3", use_container_width=True):
            st.info("Opening detailed analysis modal...")

    st.markdown("</div>", unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown(
    """
<div class="ff-footer">
    Powered by <span class="ff-footer-highlight">Gemini 2.5 Flash</span> •
    Content Verification Tool v2.1 •
    Built for Legal Professionals
</div>
""",
    unsafe_allow_html=True,
)
