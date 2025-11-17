# Frontend Redesign Plan: Single-Screen Gemini Verification Workflow

## Executive Summary

**Transformation**: Tab-based interface → Single-screen command center highlighting Gemini AI as the verification engine

**Core Philosophy**: "Everything visible, Gemini-powered verification at the heart"

**Design Direction**: **Freshfields-Inspired Sophisticated Minimalism** - clean, confident, and contemporary legal technology with Gemini AI prominently featured throughout the verification workflow

**Aesthetic Foundation**: Following Freshfields' design language:

- Elegant serif headlines with generous line-height
- Soft color blocks (powder blues and lime green accents)
- Crisp cream-white backgrounds
- Clean, minimal aesthetic with strong hierarchy
- Pill-shaped buttons and refined UI elements
- Generous whitespace that conveys sophistication

---

## Design Analysis: Freshfields Aesthetic

### Key Visual Elements Observed

1. **Typography**

   - Large, elegant serif for headlines (likely Freight Display, Tiempos, or custom)
   - Clean sans-serif for body text
   - Dramatic scale contrast (headlines 2-3x larger than body)
   - Generous line-height and letter-spacing in display text

2. **Color Strategy**

   - Cream white backgrounds (#FAFAF9)
   - Deep black for text and sections
   - Powder blue (#A4C8E1) for soft accent blocks
   - Lime/chartreuse green (#C8E86B) for CTAs and highlights
   - Minimal palette - no more than 4-5 colors total

3. **Layout Philosophy**

   - Generous breathing room
   - Bold full-width color blocks for section division
   - Clean grid system with clear alignment
   - Asymmetric layouts with purpose
   - Strategic use of empty space

4. **Interactive Elements**

   - Rounded pill-shaped buttons
   - Black primary buttons
   - Lime green accent buttons
   - Simple hover states
   - Minimal borders, emphasis on whitespace

5. **Overall Impression**
   - Modern yet timeless
   - Professional but not stuffy
   - Confident and clean
   - European design sensibility
   - High-end without being ostentatious

---

## Current State vs. Target State

### Current Structure (Post-Minimalist Refactor)

```
┌──────────────────────────────────────────────────────────────┐
│  Header + Backend Status                                     │
├──────────────────────────────────────────────────────────────┤
│  Tab 1: 📚 Corpus        │  Tab 2: ✅ Verification          │
├──────────────────────────┴──────────────────────────────────┤
│  Corpus Upload/Details   │  4 Horizontal Cards              │
│  (Full width when active)│  • Upload                        │
│                          │  • Chunking                      │
│                          │  • Verify (AI)                   │
│                          │  • Export                        │
│                          │                                  │
│                          │  Results Section                 │
└──────────────────────────┴──────────────────────────────────┘
```

**Issues with Current Design:**

- Gemini's role is understated
- Tab switching hides corpus context
- Workflow feels disconnected
- Generic styling doesn't reflect brand sophistication
- User must navigate between tabs

---

### Target State: Single-Screen Gemini-Centric Design

```
┌───────────────────────────────────────────────────────────────────────┐
│  HEADER (Cream white bg, clean nav)                                  │
│  Content Verification                    Powered by Gemini 🔷       │
└───────────────────────────────────────────────────────────────────────┘
┌─────────────────┬─────────────────────────────────────────────────────┐
│                 │                                                     │
│  CORPUS SIDEBAR │  VERIFICATION WORKFLOW                              │
│  (Fixed 300px)  │  (Fluid main area)                                  │
│  Soft blue bg   │                                                     │
│                 │  ┌─────────────────────────────────────────────┐  │
│  ╔═══════════╗  │  │  GEMINI-POWERED VERIFICATION                 │  │
│  ║ Reference ║  │  │  4-step horizontal workflow                  │  │
│  ║ Corpus    ║  │  ├────┬────┬──────┬────┐                       │  │
│  ╚═══════════╝  │  │ 1  │ 2  │  3   │ 4  │                       │  │
│                 │  │Up  │Chk │Gemini│Exp │                       │  │
│  ✓ Active       │  │load│Mode│  AI  │ort │                       │  │
│  5 documents    │  └────┴────┴──────┴────┘                       │  │
│  127 pages      │         ↑                                       │  │
│  23.4 MB        │    Highlighted                                  │  │
│                 │                                                     │
│  Quick Upload   │  ┌─────────────────────────────────────────────┐  │
│  ┌───────────┐  │  │  GEMINI VERIFICATION RESULTS                 │  │
│  │Drop files │  │  │  ┌────┬────┬────┬────┐                      │  │
│  └───────────┘  │  │  │124 │ 89 │8.2 │45s │  ← Metrics          │  │
│                 │  │  └────┴────┴────┴────┘                      │  │
│  [Actions]      │  │                                              │  │
│  • View Docs    │  │  Confidence Distribution                     │  │
│  • Configure    │  │  🟢 High: 67 chunks (54%)                    │  │
│  • Clear Corpus │  │  🟡 Med:  22 chunks (18%)                    │  │
│                 │  │  🔴 Low:  35 chunks (28%)                    │  │
│                 │  │                                              │  │
│                 │  │  [Items Needing Review]                      │  │
└─────────────────┴─────────────────────────────────────────────────────┘
│  FOOTER: Powered by Gemini 2.5 Flash • Content Verification v2.1    │
└───────────────────────────────────────────────────────────────────────┘
```

---

## Design Principles

### 1. Gemini-First Narrative

Gemini should be visible and central throughout:

- **Header Badge**: "Powered by Gemini 🔷" in prominent position
- **Step 3 Branding**: "Gemini AI Verification" with special visual treatment
- **Results Attribution**: "Gemini Verification Results" as section header
- **Footer**: Model information (Gemini 2.5 Flash)
- **Corpus Context**: "AI-Ready Corpus" or "Gemini File Search" references

### 2. Single-Screen Transparency

Everything important visible at once:

- Fixed sidebar shows corpus status always
- Workflow steps always visible horizontally
- Results appear below workflow (no deep scrolling needed)
- No tabs, minimal modals
- Clear visual hierarchy guides the eye

### 3. Freshfields Aesthetic Integration

- **Large serif headlines** for section titles
- **Soft color blocks** to separate sidebar from main content
- **Lime green accents** for primary actions (Gemini verification button)
- **Pill-shaped buttons** following Freshfields pattern
- **Generous whitespace** between elements
- **Minimal borders**, relying on color and space for separation

### 4. Workflow Clarity

Left-to-right mental model:

1. **Corpus (sidebar)** = Knowledge base for Gemini
2. **Upload** = Document to verify
3. **Chunk** = Processing method
4. **Gemini Verify** = AI analysis (HIGHLIGHTED)
5. **Export** = Get results
6. **Results** = Gemini's findings

---

## Visual Design System

### Typography (Freshfields-Inspired)

```css
/* Display/Headings - Elegant Serif */
--font-display: "Freight Display Pro", "Tiempos", "Lora", "Georgia", serif;
/* Fallbacks for web fonts: Lora (Google), Georgia (system) */

/* Body/UI - Clean Sans-Serif */
--font-body: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;

/* Monospace */
--font-mono: "JetBrains Mono", "SF Mono", "Consolas", monospace;

/* Scale - Generous, Freshfields-inspired */
--text-xs: 0.75rem; /* 12px - labels */
--text-sm: 0.875rem; /* 14px - captions */
--text-base: 1rem; /* 16px - body */
--text-lg: 1.25rem; /* 20px - large body */
--text-xl: 1.875rem; /* 30px - section headings */
--text-2xl: 2.5rem; /* 40px - page title */
--text-3xl: 3.5rem; /* 56px - hero (if needed) */

/* Line Heights */
--leading-none: 1;
--leading-tight: 1.25;
--leading-snug: 1.4;
--leading-normal: 1.6;
--leading-relaxed: 1.8;

/* Letter Spacing */
--tracking-tight: -0.02em;
--tracking-normal: 0;
--tracking-wide: 0.025em;
```

### Color Palette (Freshfields-Inspired)

```css
/* Core Palette */

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
--ff-blue-300: #a4c8e1; /* Primary Freshfields blue */
--ff-blue-400: #7ba8c9;
--ff-blue-500: #5a8fb5;
--ff-blue-600: #4d7fa3;

/* Freshfields Green - Lime/Chartreuse */
--ff-green-50: #f5f9e8;
--ff-green-100: #e8f3d6;
--ff-green-200: #ddeeb8;
--ff-green-300: #c8e86b; /* Primary Freshfields green */
--ff-green-400: #b0d94f;
--ff-green-500: #9ac93d;
--ff-green-600: #8fb830;

/* Gemini Brand Colors */
--gemini-blue-light: #e0f2f7;
--gemini-blue: #4fc3f7;
--gemini-blue-dark: #0288d1;

/* Semantic Colors */
--success: #059669;
--warning: #f59e0b;
--error: #dc2626;
--info: var(--gemini-blue);

/* Usage */
--bg-primary: var(--white);
--bg-secondary: var(--cream-white);
--bg-sidebar: var(--ff-blue-100); /* Soft blue for sidebar */
--bg-accent: var(--ff-blue-300);
--bg-dark: var(--black);

--text-primary: var(--black);
--text-secondary: var(--charcoal);
--text-tertiary: var(--mid-gray);
--text-on-dark: var(--white);
--text-on-blue: var(--black);

--border-light: var(--cream);
--border-medium: var(--warm-gray-light);
--border-dark: var(--warm-gray);

--cta-primary: var(--black); /* Black buttons */
--cta-accent: var(--ff-green-300); /* Lime green for highlights */
--cta-gemini: var(--gemini-blue); /* Gemini-specific CTAs */
```

### Spacing & Layout

```css
/* Spacing - 8px base grid */
--space-1: 0.5rem; /* 8px */
--space-2: 1rem; /* 16px */
--space-3: 1.5rem; /* 24px */
--space-4: 2rem; /* 32px */
--space-6: 3rem; /* 48px */
--space-8: 4rem; /* 64px */
--space-12: 6rem; /* 96px */
--space-16: 8rem; /* 128px */

/* Layout Constraints */
--sidebar-width: 300px;
--header-height: 72px;
--footer-height: 48px;
--max-content-width: 1600px;
--workflow-card-min-width: 200px;

/* Border Radius - Freshfields style (rounded pills) */
--radius-sm: 0.25rem; /* 4px */
--radius-md: 0.5rem; /* 8px */
--radius-lg: 1rem; /* 16px */
--radius-xl: 1.5rem; /* 24px */
--radius-2xl: 2rem; /* 32px */
--radius-full: 9999px; /* Full pill */

/* Shadows - Subtle, refined */
--shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.06);
--shadow-md: 0 4px 8px rgba(0, 0, 0, 0.08);
--shadow-lg: 0 8px 20px rgba(0, 0, 0, 0.1);
```

### Animation & Motion

```css
/* Timing Functions */
--ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);

/* Durations */
--duration-fast: 150ms;
--duration-base: 250ms;
--duration-slow: 400ms;
--duration-slower: 600ms;

/* Transitions */
--transition-all: all var(--duration-base) var(--ease-smooth);
--transition-colors: background-color var(--duration-base) var(--ease-smooth), color
    var(--duration-base) var(--ease-smooth),
  border-color var(--duration-base) var(--ease-smooth);
--transition-transform: transform var(--duration-base) var(--ease-out);
```

---

## Component Architecture

### Layout Structure

```
┌─────────────────────────────────────────────────────┐
│ Header (fixed, 72px)                                │
├──────────────┬──────────────────────────────────────┤
│   Sidebar    │    Main Content Area                 │
│   (300px)    │    (Fluid)                           │
│   Fixed      │                                      │
│   Scroll     │    - Workflow Cards (4 horizontal)   │
│              │    - Results Section                 │
│              │    - (Scrollable if needed)          │
├──────────────┴──────────────────────────────────────┤
│ Footer (fixed, 48px)                                │
└─────────────────────────────────────────────────────┘
```

### 1. Header Component

**Design:**

```
┌─────────────────────────────────────────────────────────────────┐
│  Content Verification            🔷 Powered by Gemini  [•]     │
└─────────────────────────────────────────────────────────────────┘
```

**Elements:**

- Left: Title in elegant serif (Freight Display, ~24px)
- Right: "Powered by Gemini" badge with Gemini diamond icon
- Background: Cream white
- Subtle bottom border

**Styling:**

- Height: 72px
- Padding: 0 3rem
- Display: flex, justify-content: space-between
- Position: sticky top

---

### 2. Corpus Sidebar Component

**Design:**

```
┌─────────────────────┐
│ Reference Corpus    │  ← Serif headline
├─────────────────────┤
│                     │
│  ✓ Active           │  ← Status badge
│  Gemini-Ready       │
│                     │
│  ┌───────────────┐  │
│  │ 5 documents   │  │  Stats card
│  │ 127 pages     │  │
│  │ 23.4 MB       │  │
│  └───────────────┘  │
│                     │
│  Quick Upload       │
│  ┌───────────────┐  │
│  │  Drop files   │  │  Upload zone
│  └───────────────┘  │
│                     │
│  [View Details]     │  ← Buttons
│  [Clear Corpus]     │
│                     │
└─────────────────────┘
```

**Styling:**

- Width: 300px fixed
- Background: Soft blue (--ff-blue-100)
- Padding: 2rem
- Scrollable if content overflows
- Serif headline for "Reference Corpus"
- Pill-shaped buttons at bottom

**States:**

- **Empty**: Large upload area, call-to-action
- **Active**: Compact stats + quick actions
- **Loading**: Skeleton state

---

### 3. Workflow Cards (4 Horizontal)

**Layout:**

```
┌─────────────────────────────────────────────────────────────────┐
│  Gemini-Powered Document Verification                          │
├──────────┬──────────┬────────────┬──────────┐                 │
│   Card 1 │  Card 2  │   Card 3   │  Card 4  │                 │
│  Upload  │ Chunking │   GEMINI   │  Export  │                 │
│          │          │     AI     │          │                 │
│          │          │  (Special) │          │                 │
└──────────┴──────────┴────────────┴──────────┘                 │
```

**Card Structure (Standard):**

```
┌──────────────┐
│ 1            │  ← Number (subtle)
│ Upload       │  ← Title (serif)
├──────────────┤
│              │
│  [Content]   │  ← Upload widget, radio, etc.
│              │
│  ✓ Ready     │  ← Status indicator
└──────────────┘
```

**Card 3 (Gemini Verification) - Special Treatment:**

```
┌───────────────────┐
│ 3                 │  ← Number
│ Verify            │  ← Title (serif)
├───────────────────┤
│                   │
│  🔷 Gemini AI     │  ← Gemini badge (prominent)
│                   │
│  Analyzes your    │  ← Description
│  content against  │
│  reference docs   │
│                   │
│  ┌─────────────┐  │
│  │ Run Verify  │  │  ← Lime green CTA button
│  └─────────────┘  │
│                   │
│  ✓ Corpus Ready   │  ← Status
└───────────────────┘
```

**Card Styling:**

- Background: White
- Border: 1px solid --border-light
- Border-radius: --radius-lg (16px)
- Padding: 2rem
- Min-width: 200px
- Shadow: --shadow-sm on hover
- Transition: all 250ms

**Gemini Card Specific:**

- Subtle blue background tint (--gemini-blue-light)
- Lime green button (--ff-green-300)
- Gemini diamond icon 🔷
- Slightly larger than other cards (emphasis)

---

### 4. Results Section Component

**Design:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Gemini Verification Results                                     │
│ Completed 45 seconds ago                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐                 │
│  │ 124 │  │  89 │  │ 8.2 │  │ 45s │  │  ✓  │   ← Metrics    │
│  │Total│  │Vrfd │  │Conf │  │Time │  │Done │                 │
│  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘                 │
│                                                                 │
│  Confidence Distribution                                        │
│  ───────────────────────────────────────────────                │
│  🟢 High (8-10)     67 chunks  ████████████████  54%           │
│  🟡 Medium (5-7)    22 chunks  ██████            18%           │
│  🔴 Low (<5)        35 chunks  ██████████        28%           │
│                                                                 │
│  Items Requiring Review                                         │
│  ───────────────────────────────────────────────                │
│  ▼ Page 2, Item 4 - Low Confidence (4.2/10)                    │
│  ▼ Page 3, Item 7 - No Reference Match                         │
│  ▼ Page 5, Item 2 - Conflicting Sources                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Styling:**

- Background: White
- Border-top: 2px solid --border-medium
- Padding: 3rem
- Metrics: Large serif numbers, small sans labels
- Progress bars: Lime green for high, yellow for med, red for low
- Expandable items for detailed review

---

### 5. Footer Component

**Design:**

```
┌─────────────────────────────────────────────────────────────────┐
│  Powered by Gemini 2.5 Flash • Content Verification v2.1       │
└─────────────────────────────────────────────────────────────────┘
```

**Styling:**

- Height: 48px
- Background: --cream-white
- Text: Small (14px), centered
- Color: --text-tertiary
- Border-top: 1px solid --border-light

---

## Streamlit Implementation Constraints & Technical Guidelines

### Critical Architecture Constraints

Streamlit's rendering model imposes specific constraints that must be understood before implementation:

#### 1. **HTML Containers Cannot Nest Streamlit Widgets**

**The Problem:**
Streamlit widgets (like `st.file_uploader()`, `st.button()`, etc.) **cannot** be rendered inside custom HTML `<div>` containers created with `st.markdown()`. This is a fundamental limitation of how Streamlit processes and renders components.

**What Doesn't Work:**

```python
# WRONG - This creates empty containers
st.markdown('<div class="main-grid">', unsafe_allow_html=True)
st.markdown('<div class="sidebar">', unsafe_allow_html=True)

# These widgets render OUTSIDE the divs, not inside them
uploaded_file = st.file_uploader("Upload")
st.button("Submit")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
```

**Result:** Massive white space where the HTML containers are empty, and all widgets render sequentially after the closing tags.

**Root Cause:** Streamlit's component rendering happens in a separate pass from `st.markdown()` HTML generation. The HTML structure is rendered first, then widgets are appended in document order.

---

#### 2. **Correct Layout Pattern: Use Streamlit Columns**

**The Solution:**
Always use Streamlit's native layout primitives (`st.columns()`, `st.container()`) for structural layout. Use `st.markdown()` HTML **only** for styling wrappers around Streamlit-generated elements.

**What Works:**

```python
# CORRECT - Use Streamlit columns for layout
sidebar, main = st.columns([1, 3], gap="small")

with sidebar:
    # Optional: Add styling wrapper
    st.markdown('<div class="sidebar-panel">', unsafe_allow_html=True)

    # All sidebar widgets inside the 'with' block
    st.markdown("### Reference Corpus")
    st.success("✓ Active & Ready")
    uploaded_refs = st.file_uploader("Upload documents")

    st.markdown('</div>', unsafe_allow_html=True)

with main:
    # Main content widgets inside this 'with' block
    st.markdown("## Gemini-Powered Verification")

    # Nested columns for workflow cards
    card1, card2, card3, card4 = st.columns(4)

    with card1:
        st.markdown("**1. Upload**")
        uploaded_doc = st.file_uploader("Document")
```

**Key Rules:**

- Use `st.columns([1, 3])` for sidebar/main split (ratio-based widths)
- Use `st.columns(4)` for equal-width workflow cards
- All widgets **must** be inside `with` blocks to render in correct columns
- Gap parameter accepts: `"small"`, `"medium"`, or `"large"` only (NOT `"none"`)
- HTML wrappers can add classes but don't control layout structure

---

#### 3. **CSS Targeting Strategy**

Since we can't control HTML structure directly, we must target Streamlit's auto-generated DOM elements:

**Streamlit's Generated Classes & Attributes:**

| Element       | Selector                          | Usage                    |
| ------------- | --------------------------------- | ------------------------ |
| Columns       | `[data-testid="column"]`          | Style individual columns |
| Containers    | `[data-testid="stVerticalBlock"]` | Style container blocks   |
| Metrics       | `[data-testid="stMetricValue"]`   | Large metric numbers     |
| Metrics       | `[data-testid="stMetricLabel"]`   | Metric labels            |
| Buttons       | `.stButton > button`              | Button styling           |
| File Uploader | `.stFileUploader`                 | Upload component         |
| Text Input    | `.stTextInput input`              | Input fields             |
| Text Area     | `.stTextArea textarea`            | Text areas               |
| Radio         | `.stRadio > label`                | Radio buttons            |
| Progress      | `.stProgress > div > div`         | Progress bars            |

**CSS Strategy:**

```css
/* Style Streamlit columns */
[data-testid="column"] {
  padding: 0 0.75rem;
}

[data-testid="column"]:first-child {
  padding-left: 0;
}

/* Style containers as cards */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
  background: white;
  border: 1.5px solid #e8e6e3;
  border-radius: 1rem;
  padding: 1.5rem;
}

/* Style buttons */
.stButton > button {
  border-radius: 9999px !important; /* Pill shape */
  font-weight: 600 !important;
  padding: 0.75rem 1.5rem !important;
}
```

**Important Notes:**

- Use `!important` sparingly, only when overriding Streamlit's default styles
- Test selectors with browser DevTools to ensure they target correctly
- Streamlit's DOM structure may change between versions - prefer data attributes over class names
- Custom classes added via `st.markdown()` only work on wrapper divs, not widgets

---

### Issues Identified in Mockup Review

During testing of `design_6_fixed.py` at `localhost:8504`, the following issues were identified:

#### Issue 1: Card Borders Not Showing

**Problem:** Workflow cards (Cards 1-4) appear as plain containers without borders, shadows, or hover effects.

**Root Cause:** CSS selector `[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"]` is too specific and may not be matching the actual DOM structure generated by nested `st.columns()` and `st.container()`.

**Investigation Needed:**

- Use browser DevTools to inspect actual DOM structure
- Identify correct selector for Streamlit containers inside columns
- Test whether `st.container()` needs to be explicitly used to create card boundaries

**Potential Fix:**

```css
/* More lenient selector for cards */
[data-testid="column"] > div {
  background: white;
  border: 1.5px solid #e8e6e3;
  border-radius: 1rem;
  padding: 1.5rem;
}

/* Or target containers directly */
.element-container {
  background: white;
  border: 1.5px solid #e8e6e3;
  border-radius: 1rem;
}
```

---

#### Issue 2: Sidebar Blue Background Not Applying

**Problem:** Sidebar should have soft powder blue background (`--ff-blue-100: #e5f0f7`) but appears white/default.

**Root Cause:** The `.sidebar-panel` class is applied to a `<div>` wrapper inside the column, but Streamlit's column rendering may override background colors, or the wrapper div doesn't extend full height.

**Potential Fix:**

```css
/* Target the column itself for sidebar */
[data-testid="column"]:first-child {
  background: #e5f0f7 !important;
  padding: 2rem !important;
  border-right: 1px solid #a4c8e1;
  min-height: calc(100vh - 120px);
}

/* Or use more specific wrapper styling */
.sidebar-panel {
  background: #e5f0f7 !important;
  min-height: calc(100vh - 120px);
  margin: -1rem; /* Extend to column edges */
  padding: 2rem;
}
```

---

#### Issue 3: Header Layout Broken Across Two Rows

**Problem:** Header title "Content Verification" and "Powered by Gemini" badge appear on separate rows instead of a single horizontal line.

**Current Code:**

```python
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="custom-header"><span class="header-title">Content Verification</span></div>')
with col2:
    st.markdown('<div class="custom-header"><span class="gemini-badge">🔷 Powered by Gemini</span></div>')
```

**Root Cause:** Each column renders as a block element, and nested divs with `.custom-header` may be forcing full-width behavior.

**Potential Fix:**

```python
# Option A: Use container with flexbox
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 3rem; background: #fafaf9; border-bottom: 1px solid #e8e6e3;">
    <span class="header-title">Content Verification</span>
    <span class="gemini-badge">🔷 Powered by Gemini</span>
</div>
""", unsafe_allow_html=True)

# Option B: Use CSS to style columns as inline-flex
# Apply this CSS:
# [data-testid="column"] { display: inline-flex !important; }
```

---

#### Issue 4: Overall Spacing Too Tight

**Problem:** Elements appear cramped together, lacking the "generous whitespace" that defines Freshfields aesthetic.

**Observations:**

- Insufficient padding between workflow cards
- Vertical spacing between sections too small
- Results section feels compressed

**Recommended Fixes:**

```css
/* Increase base spacing */
.main {
  padding: 3rem !important; /* Increase from default */
}

/* Add vertical spacing between major sections */
.element-container {
  margin-bottom: 2rem !important; /* Increase from 0.5rem */
}

/* Increase column gaps */
[data-testid="column"] {
  padding: 0 1.5rem !important; /* Increase from 0.75rem */
}

/* Add breathing room to cards */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
  padding: 2.5rem !important; /* Increase from 1.5rem */
  margin-bottom: 2rem !important;
}

/* Increase spacing in results section */
.stMetric {
  margin-bottom: 1.5rem !important;
}

hr {
  margin: 3rem 0 !important; /* Increase from 2rem */
}
```

---

#### Issue 5: Gemini Card 3 Not Visually Distinct

**Problem:** Card 3 (Gemini Verification) should have special visual treatment with gradient background and enhanced styling, but appears similar to other cards.

**Current Approach:**

```python
with card3:
    st.markdown('<div class="gemini-card" style="...gradient background...">')
    st.markdown("**3. Verify**")
    # ... content ...
    st.markdown('</div>')
```

**Issue:** The wrapper div with `.gemini-card` class doesn't extend to encompass the Streamlit widgets rendered inside it.

**Potential Fix:**

```python
with card3:
    # Use inline styles on container
    st.markdown("""
    <style>
    [data-testid="column"]:nth-child(3) {
        background: linear-gradient(135deg, #e0f2f7 0%, #ffffff 100%) !important;
        border: 2px solid #4fc3f7 !important;
        border-radius: 1rem !important;
        padding: 1.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("**3. Verify**")
    st.markdown("### 🔷")
    st.markdown("**Gemini AI**")
    # ... rest of content ...
```

**Alternative:** Use `st.container()` with explicit styling:

```python
with card3:
    with st.container():
        st.markdown("**3. Verify**")
        # Add CSS targeting this specific container
```

---

### Implementation Best Practices

#### 1. **Layout Structure Template**

```python
import streamlit as st

# Page config
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# CSS injection
st.markdown("""<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Variables */
    :root {
        --cream-white: #fafaf9;
        --ff-blue-100: #e5f0f7;
        --ff-green-300: #c8e86b;
    }

    /* Global styles */
    h1, h2, h3 { font-family: 'Lora', serif !important; }
    p, div, label { font-family: 'Inter', sans-serif !important; }

    /* Layout styles */
    .block-container { padding: 0 !important; max-width: 100% !important; }

    /* Component styles */
    /* ... */
</style>""", unsafe_allow_html=True)

# Header (single line)
st.markdown("""
<div style="display: flex; justify-content: space-between; padding: 1.5rem 3rem; background: var(--cream-white); border-bottom: 1px solid #e8e6e3;">
    <h1 style="margin: 0;">Content Verification</h1>
    <span>🔷 Powered by Gemini</span>
</div>
""", unsafe_allow_html=True)

# Main layout
sidebar, main = st.columns([1, 3], gap="small")

with sidebar:
    # Sidebar content - all widgets inside this block
    st.markdown("### Reference Corpus")
    # ...

with main:
    # Main content - all widgets inside this block
    st.markdown("## Gemini-Powered Verification")

    # Workflow cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        # Card 1 content
        pass
    with c2:
        # Card 2 content
        pass
    # ...
```

#### 2. **Testing Checklist**

Before finalizing any Streamlit UI implementation:

- [ ] **Browser DevTools Inspection**: Verify DOM structure matches CSS selectors
- [ ] **Responsive Testing**: Check layout at 1280px, 1440px, 1920px widths
- [ ] **Widget Rendering**: Confirm all widgets appear inside intended columns
- [ ] **CSS Application**: Verify fonts, colors, spacing match design spec
- [ ] **Interactive States**: Test hover, focus, active states on buttons
- [ ] **Streamlit Rerun**: Test that layout persists after widget interactions
- [ ] **Performance**: Ensure CSS doesn't cause layout thrashing or reflows

#### 3. **Debugging Tips**

**Common Issues:**

1. **Widgets appearing in wrong column**

   - Check indentation - must be inside `with` block
   - Verify column variables aren't being reused

2. **CSS not applying**

   - Use `!important` to override Streamlit defaults
   - Check selector specificity with DevTools
   - Ensure `unsafe_allow_html=True` is set

3. **Layout breaking on rerun**

   - Avoid conditional column creation
   - Use session state for dynamic layouts
   - Test with `st.experimental_rerun()`

4. **Spacing issues**
   - Streamlit adds default margins - override with negative margins if needed
   - Use `.element-container` to target wrapper elements
   - Check for conflicting padding/margin rules

---

### Mockup Files Reference

**Current Mockups:**

1. **`design_5_single_screen_mvp.py`** - Original vision (Bloomberg Terminal aesthetic)
2. **`design_6_freshfields_single_screen.py`** - First attempt (HTML layout - BROKEN)
   - **Issue:** Used HTML divs for layout, widgets rendered outside containers
   - **Status:** Do not use as reference
3. **`design_6_fixed.py`** - Streamlit-native approach (CURRENT)
   - **Status:** Layout structure correct, styling needs refinement
   - **Known Issues:** Cards, sidebar, header, spacing, Gemini card (see above)

**Next Steps:**

- Fix identified issues in `design_6_fixed.py`
- Create `design_6_final.py` with all corrections
- Use final mockup as implementation reference

---

## Implementation Plan

### Phase 1: Layout Restructure (2-3 hours)

**Objective**: Remove tabs, implement single-screen grid layout

**Tasks:**

1. Remove `st.tabs()` from `main.py`
2. Create fixed sidebar (300px) using Streamlit columns
3. Move corpus components to sidebar
4. Move workflow to main content area
5. Implement responsive grid for workflow cards

**Files Modified:**

- `frontend/main.py`
- `frontend/app/corpus.py`

**Success Criteria:**

- [ ] No tabs visible
- [ ] Sidebar fixed at 300px
- [ ] Workflow cards in main area
- [ ] All functionality preserved

---

### Phase 2: Freshfields Visual Design (3-4 hours)

**Objective**: Apply Freshfields aesthetic throughout

**Tasks:**

1. Create CSS file with design system variables
2. Load Google Fonts (Lora for serif, Inter for sans)
3. Apply typography styles (serif headlines, sans body)
4. Implement color palette (blues, greens, creams)
5. Style buttons as pills (border-radius: full)
6. Add generous spacing throughout
7. Create soft blue sidebar background
8. Apply shadows and subtle borders

**Files Modified:**

- New: `frontend/app/freshfields_styles.py`
- `frontend/main.py` - Import styles
- `frontend/app/ui_components.py`

**Success Criteria:**

- [ ] Fonts loaded and applied correctly
- [ ] Color palette matches Freshfields
- [ ] Buttons are pill-shaped
- [ ] Generous spacing between elements
- [ ] Overall feel matches Freshfields aesthetic

---

### Phase 3: Gemini Branding Integration (1-2 hours)

**Objective**: Make Gemini central and visible

**Tasks:**

1. Add "Powered by Gemini" badge to header
2. Create enhanced Card 3 with Gemini branding
3. Add Gemini diamond icon (🔷 or custom SVG)
4. Style Gemini verification button (lime green)
5. Update results header to "Gemini Verification Results"
6. Add model info to footer

**Files Modified:**

- `frontend/app/ui_components.py` - Header, footer
- `frontend/main.py` - Card 3 enhancement

**Success Criteria:**

- [ ] Gemini badge in header
- [ ] Card 3 visually distinct with Gemini branding
- [ ] Results clearly attributed to Gemini
- [ ] Footer shows model version

---

### Phase 4: Corpus Sidebar Refinement (2 hours)

**Objective**: Create compact, always-visible corpus panel

**Tasks:**

1. Redesign for 300px width constraint
2. Create compact stats display
3. Implement quick upload in sidebar
4. Add action buttons (View Details, Clear)
5. Style with soft blue background
6. Implement empty vs. active states

**Files Modified:**

- `frontend/app/corpus.py`

**Success Criteria:**

- [ ] Corpus status visible at glance
- [ ] Quick upload works without modal
- [ ] Stats displayed compactly
- [ ] Soft blue background applied
- [ ] Actions accessible

---

### Phase 5: Workflow Cards Optimization (2 hours)

**Objective**: Perfect 4-card horizontal layout

**Tasks:**

1. Ensure cards scale properly in grid
2. Add serif titles and subtle numbering
3. Implement status indicators
4. Style Card 3 with special Gemini treatment
5. Test responsive behavior
6. Add tooltips/help text

**Files Modified:**

- `frontend/main.py` - Card rendering

**Success Criteria:**

- [ ] All 4 cards visible without scroll
- [ ] Card 3 stands out visually
- [ ] Status flows naturally
- [ ] Responsive on different widths

---

### Phase 6: Results Enhancement (1-2 hours)

**Objective**: Polished results display

**Tasks:**

1. Create metrics grid with large serif numbers
2. Style confidence distribution bars
3. Add expandable review items
4. Implement smooth scrolling to results
5. Ensure Gemini attribution visible

**Files Modified:**

- `frontend/main.py` - Results rendering
- `frontend/app/ui_components.py`

**Success Criteria:**

- [ ] Metrics are prominent and clear
- [ ] Confidence bars styled correctly
- [ ] Results feel polished and complete
- [ ] Gemini attribution clear

---

### Phase 7: Polish & Testing (2-3 hours)

**Objective**: Final refinements and QA

**Tasks:**

1. Test full workflow end-to-end
2. Check all edge cases (errors, empty states)
3. Verify responsive behavior (min 1280px)
4. Performance testing
5. Cross-browser testing
6. Accessibility check
7. Final design tweaks

**Success Criteria:**

- [ ] Happy path works flawlessly
- [ ] Edge cases handled
- [ ] No console errors
- [ ] Smooth performance
- [ ] Professional appearance

---

## Migration Strategy

### Approach

1. Create feature branch: `single-screen-freshfields-redesign`
2. Implement phases sequentially
3. Test after each phase
4. Keep current tab-based version as fallback
5. Deploy with feature flag if possible

### Rollback Plan

- Maintain tab-based version in `main` until confident
- Document state/data compatibility
- Test migration scenarios
- Prepare rollback script

---

## Success Metrics

### User Experience

- [ ] Entire workflow visible at glance
- [ ] Gemini's role immediately clear
- [ ] Interface feels sophisticated and professional
- [ ] Workflow completion is intuitive

### Technical

- [ ] Page load < 2s
- [ ] No layout shift
- [ ] 60fps animations
- [ ] Works on screens ≥ 1280px

### Aesthetic

- [ ] Freshfields design language captured
- [ ] Typography hierarchy clear
- [ ] Color palette applied consistently
- [ ] Generous whitespace throughout
- [ ] Professional, modern appearance

---

## Design Decisions & Rationale

### Why Sidebar Instead of Tabs?

**Rationale**: Keeps corpus context visible during verification workflow. Users can see corpus status without switching views, making the Gemini verification feel more connected to its knowledge source.

### Why Lime Green for Gemini Button?

**Rationale**: Follows Freshfields' use of lime green (#C8E86B) for primary CTAs. Creates strong visual hierarchy and draws attention to the central verification action.

### Why Soft Blue Sidebar?

**Rationale**: Freshfields uses powder blue (#A4C8E1) for section differentiation. Creates subtle separation without harsh borders while maintaining sophisticated aesthetic.

### Why Large Serif Headlines?

**Rationale**: Freshfields' signature - creates professional, editorial quality that resonates with legal professionals while avoiding generic SaaS aesthetics.

### Why Pill-Shaped Buttons?

**Rationale**: Freshfields pattern - rounded pills (border-radius: 9999px) feel modern, approachable, and confident. More distinctive than standard rectangles.

---

## Future Enhancements (Post-MVP)

1. **Dark Mode**: Freshfields-inspired dark theme
2. **Gemini Model Selection**: Choose between Flash/Pro
3. **Real-time Progress**: Live verification updates
4. **Keyboard Shortcuts**: Power user features
5. **Export Templates**: Customizable outputs
6. **Verification History**: Track past runs
7. **Advanced Analytics**: Corpus insights
8. **Collaboration**: Share results
9. **Batch Processing**: Multiple documents
10. **Custom Branding**: White-label options

---

## Mockup Reference

### Production-Ready MVP: `design_6_freshfields_single_screen_mvp.py`

**Status**: ✅ Complete - All issues resolved (Latest update: **Freshfields-accurate compact spacing**)

> **Critical Update**: After comparing to the actual Freshfields website, all spacing has been corrected to match their efficient, compact aesthetic. The previous version had excessive vertical spacing - this has been fixed to use tight, professional spacing (16-24px standard) that matches real Freshfields design.

This is the **reference implementation** for the frontend refactor. It demonstrates:

1. **Fixed Header Layout** - Single-row flexbox with title and Gemini badge
2. **Working Sidebar Background** - Powder blue (#e5f0f7) properly applied to first column
3. **Visible Card Borders** - Correct CSS selectors with `.ff-card` class
4. **Freshfields-Accurate Spacing** - Compact, efficient spacing (16-24px standard) matching real Freshfields
5. **Distinct Gemini Card** - Gradient background, thicker border, radial glow effect
6. **Production-Grade Code** - Clean architecture, comprehensive CSS system, proper component structure
7. **Clear Uploader Distinction** - Visual callouts and labels distinguish corpus upload from document-to-verify upload
8. **Efficient Workflow Cards** - Streamlined 220px height with tight 24px padding for professional look

**Key Implementation Details:**

- **Fonts**: Lora (serif) for headlines + IBM Plex Sans (body text)
- **Colors**: Powder blue sidebar, lime green CTAs, cream white backgrounds
- **Layout**: `st.columns([1, 3])` for sidebar/main split, `st.columns(4)` for workflow cards
- **CSS Strategy**: Custom classes (`.ff-card`, `.ff-gemini-card`) applied via HTML wrappers, then target Streamlit elements with data attributes
- **Header**: Pure HTML/CSS flexbox (not Streamlit columns) for proper single-row layout
- **Spacing** (Freshfields-accurate compact values):
  - **Sidebar**: 32px vertical, 24px horizontal padding (var(--space-4), var(--space-3))
  - **Main content**: 40px vertical, 48px horizontal (var(--space-5), var(--space-6))
  - **Cards**: 220px min-height, 24px internal padding (var(--space-3))
  - **Column gaps**: 16px between workflow cards (var(--space-2))
  - **Buttons**: Compact (10px vertical, 24px horizontal)
  - **Section dividers**: 24px vertical margin (var(--space-3))
  - **Element containers**: 16px bottom margin (var(--space-2))
  - **Alert boxes**: 16px/24px padding, 24px bottom margin
  - **Progress bars**: 8px top, 16px bottom margin

**Two-Uploader Workflow Clarity:**

The interface uses TWO distinct file uploaders with different purposes:

1. **Sidebar Uploader** (Column A - Reference Corpus)

   - **Purpose**: Upload reference documents that form the knowledge base
   - **Label**: "Upload Reference Corpus"
   - **Caption**: "📚 Add documents to use as verification sources"
   - **Info Box**: Explains these are the documents Gemini uses for verification
   - **Accepts**: Multiple files (PDF, DOCX)
   - **Use Case**: Legal precedents, case files, statutes, regulations, prior work product

2. **Step 1 Uploader** (Column B - Document to Verify)
   - **Purpose**: Upload the document you want to verify against the corpus
   - **Label**: "Upload Document" / "Document to Verify"
   - **Caption**: "📄 Upload the document you want to check against the corpus"
   - **Help Text**: "This document will be verified against your reference corpus"
   - **Accepts**: Single file (PDF, DOCX)
   - **Use Case**: Draft brief, memo, contract, filing that needs fact-checking

**Visual Distinction Strategy:**

- Sidebar uses blue background → "This is the knowledge base"
- Main content uses white background → "This is your active workflow"
- Info boxes explain each uploader's purpose explicitly
- Different icons (📚 for corpus, 📄 for document)
- Different success messages ("X files selected" vs "Ready to Verify")

**Run the mockup:**

```bash
streamlit run frontend/mockups/design_6_freshfields_single_screen_mvp.py
```

**Comprehensive Spacing System:**

The final mockup implements Freshfields-accurate **compact and efficient** spacing:

1. **Sidebar Spacing** (Compact & Efficient)

   - Top/bottom padding: **32px** (var(--space-4))
   - Between-element spacing: **16px** (var(--space-2))
   - Metrics: **16px** bottom margin
   - File uploader: **16px** top/bottom
   - Text area: **24px** bottom margin
   - Buttons: **16px** between each
   - Horizontal rules: **24px** top/bottom

2. **Workflow Cards Spacing** (Tight & Professional)

   - Card padding: **24px** (var(--space-3))
   - Card min-height: **220px**
   - Inter-card gap: **16px** (var(--space-2))
   - Card number → title: **16px**
   - Title → content: **16px**
   - Between form elements: **16px**
   - Flexbox layout ensures efficient vertical distribution

3. **Main Content Spacing** (Balanced & Clean)

   - Section padding: **40px vertical, 48px horizontal**
   - H2 headings: 0 top, **24px** bottom
   - H3 headings: **24px** top, **16px** bottom
   - Alert boxes: **24px** bottom margin
   - Workflow explanation: **24px** bottom margin
   - Between workflow and results: Single hr divider (no excessive gaps)
   - Horizontal dividers: **24px** vertical margin

4. **Results Section Spacing** (Efficient Display)
   - Metrics grid: **16px** bottom margin per metric
   - After metrics grid: **24px** (via hr)
   - Progress bars: **8px** top, **16px** bottom
   - Between distribution items: Natural flow (no forced gaps)
   - Expanders: **16px** bottom margin
   - Section separators: **24px** vertical

**Spacing Philosophy:**

The spacing system follows Freshfields' **actual** principle of **"efficient elegance"**:

- **Micro-spacing** (8px): Tight related elements (card labels, captions)
- **Standard spacing** (16-24px): Between components (metrics, form elements)
- **Section spacing** (24-32px): Major divisions (dividers, section headers)
- **No waste**: Removed all excessive `st.markdown("")` spacing tricks
- **Visual hierarchy**: Clear but compact - proper separation without excess
- **Freshfields-accurate**: Matches the efficient, polished spacing of the real Freshfields site

**Key Differences from Previous Attempts:**

| Issue              | Previous Approach                                                 | Final MVP Solution                                                          |
| ------------------ | ----------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Header layout      | Two st.columns → broken across rows                               | Single HTML flexbox div → proper horizontal layout                          |
| Sidebar background | CSS on wrapper div → didn't fill                                  | `[data-testid="column"]:first-child` → fills entire column                  |
| Card borders       | Generic Streamlit selector → no match                             | Custom `.ff-card` class on HTML wrapper → visible borders                   |
| Spacing            | First: cramped defaults<br>Then: over-corrected to excessive gaps | **Freshfields-accurate compact spacing**: 16-24px standard, no waste        |
| Gemini card        | Plain wrapper div → not distinct                                  | Gradient + pseudo-element glow + special hover → visually striking          |
| Uploader clarity   | Confusing dual uploaders                                          | Clear labels + info boxes + icons distinguish corpus vs. document-to-verify |
| Vertical rhythm    | Multiple `st.markdown("")` tricks                                 | Clean CSS-based spacing system using var(--space-X) scale                   |

---

### Legacy Mockups (Do Not Use)

1. **`design_5_single_screen_mvp.py`** - Bloomberg Terminal aesthetic (superseded)
2. **`design_6_freshfields_single_screen.py`** - First Freshfields attempt (HTML layout issues)
3. **`design_6_fixed.py`** - Partial fix (spacing and styling issues remain)

Use **only** `design_6_freshfields_single_screen_mvp.py` as the reference for the actual frontend refactor.

---

## Component Checklist

### Header

- [ ] Elegant serif title
- [ ] "Powered by Gemini" badge
- [ ] Cream white background
- [ ] Subtle bottom border

### Sidebar (Corpus)

- [ ] Soft blue background
- [ ] Serif "Reference Corpus" headline
- [ ] Compact status display
- [ ] Quick upload zone
- [ ] Pill-shaped action buttons
- [ ] Empty/active states

### Workflow Cards

- [ ] Card 1: Upload
- [ ] Card 2: Splitting mode
- [ ] Card 3: Gemini verification (enhanced)
- [ ] Card 4: Export
- [ ] Serif titles
- [ ] White backgrounds
- [ ] Subtle shadows
- [ ] Status indicators

### Results Section

- [ ] "Gemini Verification Results" header (serif)
- [ ] Large metric numbers (serif)
- [ ] Confidence distribution bars
- [ ] Expandable review items
- [ ] Lime green for high confidence

### Footer

- [ ] Model information
- [ ] Centered text
- [ ] Cream background

### Overall Styling

- [ ] Custom CSS loaded
- [ ] Fonts applied (Lora, Inter)
- [ ] Colors consistent with palette
- [ ] Generous spacing throughout
- [ ] Pill-shaped interactive elements
- [ ] Smooth transitions

---

## Timeline Estimate

| Phase                              | Duration | Cumulative |
| ---------------------------------- | -------- | ---------- |
| Phase 1: Layout Restructure        | 2-3 hrs  | 2-3 hrs    |
| Phase 2: Freshfields Visual Design | 3-4 hrs  | 5-7 hrs    |
| Phase 3: Gemini Branding           | 1-2 hrs  | 6-9 hrs    |
| Phase 4: Corpus Sidebar            | 2 hrs    | 8-11 hrs   |
| Phase 5: Workflow Cards            | 2 hrs    | 10-13 hrs  |
| Phase 6: Results Enhancement       | 1-2 hrs  | 11-15 hrs  |
| Phase 7: Polish & Testing          | 2-3 hrs  | 13-18 hrs  |

**Total Estimated Time**: 13-18 hours (2-3 full development days)

---

## Conclusion

This redesign transforms the Content Verification Tool into a sophisticated, Gemini-centric single-screen experience that embodies Freshfields' design philosophy: clean, confident, contemporary, and professional.

By eliminating tabs and making corpus status always visible, we create transparency. By prominently featuring Gemini throughout, we make the AI verification narrative clear. By applying Freshfields' aesthetic - elegant serifs, soft colors, generous spacing, pill buttons - we create an interface that legal professionals will trust and enjoy using.

The result is a distinctive, memorable interface that stands apart from generic SaaS tools while remaining highly functional and user-friendly.

---

## Implementation Guide: From Mockup to Production

### Step 1: Extract CSS to Separate Module

Create `frontend/app/freshfields_styles.py`:

```python
"""
Freshfields Design System - CSS injection for Streamlit
"""
import streamlit as st

def load_css():
    """Load Freshfields-inspired design system CSS"""
    st.markdown("""<style>
        /* Copy CSS from design_6_freshfields_single_screen_mvp.py */
        /* Import fonts, define variables, component styles */
    </style>""", unsafe_allow_html=True)
```

Usage in `frontend/main.py`:

```python
from app.freshfields_styles import load_css

st.set_page_config(layout="wide", ...)
load_css()
```

### Step 2: Create Reusable UI Components

Create `frontend/app/ui_components.py`:

```python
"""
Reusable UI components with Freshfields styling
"""
import streamlit as st

def render_header():
    """Render fixed header with Gemini badge"""
    st.markdown("""
    <div class="ff-header">
        <div class="ff-header-title">Content Verification Assistant</div>
        <div class="ff-gemini-badge">🔷 Powered by Gemini</div>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Render fixed footer with attribution"""
    st.markdown("""
    <div class="ff-footer">
        Powered by <span class="ff-footer-highlight">Gemini 2.5 Flash</span> •
        Content Verification Tool v2.1
    </div>
    """, unsafe_allow_html=True)

def render_workflow_card(step_num, title, content_fn):
    """
    Render a workflow card with consistent styling

    Args:
        step_num: Card number (1-4)
        title: Card title
        content_fn: Function that renders card content
    """
    st.markdown(
        f'<div class="ff-card">'
        f'<div class="ff-card-number">STEP {step_num}</div>'
        f'<div class="ff-card-title">{title}</div>',
        unsafe_allow_html=True
    )

    content_fn()  # Render card-specific content

    st.markdown('</div>', unsafe_allow_html=True)

def render_gemini_card(step_num, title, content_fn):
    """Render the special Gemini verification card"""
    st.markdown(
        f'<div class="ff-card ff-gemini-card">'
        f'<div class="ff-card-number">STEP {step_num}</div>'
        f'<div class="ff-card-title">{title}</div>',
        unsafe_allow_html=True
    )

    # Gemini branding
    st.markdown(
        '<div style="text-align: center; margin: 1rem 0 1.5rem 0;">'
        '<div style="font-size: 2.5rem; line-height: 1;">🔷</div>'
        '<div style="font-family: var(--font-display); font-size: 1.125rem; '
        'font-weight: 600; color: var(--gemini-blue-dark); margin-top: 0.5rem;">'
        'Gemini AI</div></div>',
        unsafe_allow_html=True
    )

    content_fn()

    st.markdown('</div>', unsafe_allow_html=True)
```

### Step 3: Refactor Main Layout

Update `frontend/main.py`:

```python
import streamlit as st
from app.freshfields_styles import load_css
from app.ui_components import render_header, render_footer, render_workflow_card, render_gemini_card
from app.corpus import render_corpus_sidebar
from app.verification import render_verification_workflow, render_results

# Page config
st.set_page_config(
    page_title="Content Verification | Powered by Gemini",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load styles
load_css()

# Header
render_header()

# Main layout: sidebar + content
sidebar_col, main_col = st.columns([1, 3], gap="small")

# Sidebar: Corpus
with sidebar_col:
    render_corpus_sidebar()

# Main content: Workflow + Results
with main_col:
    st.markdown('<div class="ff-main-content">', unsafe_allow_html=True)

    st.markdown("## Gemini-Powered Document Verification")
    st.caption("Systematically verify your document...")

    # Workflow cards
    render_verification_workflow()

    # Results section (if verification complete)
    if st.session_state.get('verification_complete'):
        render_results(st.session_state.verification_results)

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
render_footer()
```

### Step 4: Migrate Corpus Component

Update `frontend/app/corpus.py`:

```python
"""
Corpus management sidebar component
"""
import streamlit as st

def render_corpus_sidebar():
    """Render the corpus sidebar with Freshfields styling"""
    st.markdown('<div class="ff-sidebar-content">', unsafe_allow_html=True)

    st.markdown("### Reference Corpus")
    st.markdown("")

    # Status
    if st.session_state.get('corpus_active'):
        st.success("✓ Active & Gemini-Ready")
    else:
        st.warning("⏳ No Corpus Loaded")

    # Stats (from session state or API)
    corpus_stats = st.session_state.get('corpus_stats', {})
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Documents", corpus_stats.get('doc_count', 0))
        st.metric("Storage", corpus_stats.get('size', '0 MB'))
    with col2:
        st.metric("Pages", corpus_stats.get('pages', 0))
        st.metric("Chunks", corpus_stats.get('chunks', 0))

    # ... rest of corpus sidebar implementation

    st.markdown('</div>', unsafe_allow_html=True)
```

### Step 5: Testing Checklist

Before deploying the refactored frontend:

- [ ] **Visual Comparison**: Side-by-side with mockup at 1440px, 1920px widths
- [ ] **Header**: Single row, no wrapping, Gemini badge aligned right
- [ ] **Sidebar**: Powder blue background fills entire column height
- [ ] **Cards**: Borders visible, hover effects working, Gemini card distinct
- [ ] **Spacing**: Generous whitespace matching mockup
- [ ] **Fonts**: Lora for headlines, IBM Plex Sans for body text
- [ ] **Colors**: Match Freshfields palette exactly
- [ ] **Interactive States**: All buttons, inputs, uploads functional
- [ ] **Backend Integration**: API calls work, data flows correctly
- [ ] **Error Handling**: Graceful degradation, clear error messages
- [ ] **Performance**: No layout shifts, smooth interactions

### Step 6: Gradual Rollout Strategy

1. **Feature Branch**: Create `frontend-redesign` branch
2. **Parallel Development**: Keep current frontend running
3. **A/B Testing**: Use feature flag to toggle between old/new UI
4. **Feedback Collection**: Gather user feedback on new design
5. **Iterative Refinement**: Make adjustments based on feedback
6. **Full Deployment**: Merge to main once validated

---

**Next Steps**:

1. ✅ Review the MVP mockup (`design_6_freshfields_single_screen_mvp.py`)
2. Run the mockup locally to validate the design
3. Begin implementation following the guide above
4. Test thoroughly before deploying to production
