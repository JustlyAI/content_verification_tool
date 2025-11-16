"""
Freshfields Design System - CSS injection for Streamlit
Sophisticated legal technology aesthetic with Gemini AI branding

Design Philosophy:
- Lora (serif headlines) + IBM Plex Sans (body text)
- Powder blue (#e5f0f7) sidebar with lime green (#c8e86b) accents
- Compact, efficient spacing (16-24px standard) matching real Freshfields
- Pill-shaped interactive elements
- Gemini prominently featured throughout workflow
- Fixed header/footer with scrollable content area
"""
import streamlit as st


def load_freshfields_css():
    """Load Freshfields-inspired design system CSS"""
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
