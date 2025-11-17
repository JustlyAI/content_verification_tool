# Frontend Design Mockups

Three design options for the Content Verification Tool frontend redesign with two-tab layout.

## Running the Mockups

From the `frontend/mockups/` directory, run:

```bash
# Design 1: Professional Dashboard
streamlit run design_1_professional_dashboard.py

# Design 2: Split Screen Workflow
streamlit run design_2_split_screen.py

# Design 3: Minimalist Cards
streamlit run design_3_minimalist_cards.py
```

Or from the project root:

```bash
streamlit run frontend/mockups/design_1_professional_dashboard.py
```

## Design Comparison

### Design 1: Professional Dashboard

**Philosophy:** Metrics-driven, data-rich interface with clear visual hierarchy

**Key Features:**

- Prominent metrics at top of Corpus tab
- Two-column Verification tab (workflow left, results right)
- Results pane with tabs (Summary + Detailed)
- Expandable verification items with full details
- Professional, corporate feel

**Best For:**

- Users who want immediate visibility into corpus stats
- Teams that value data-driven dashboards
- Scenarios with heavy focus on metrics and KPIs

---

### Design 2: Split Screen Workflow

**Philosophy:** Side-by-side workflow with comprehensive results exploration

**Key Features:**

- Full-width Corpus tab with document library and settings side-by-side
- Split Verification tab (workflow 40%, results 60%)
- Multiple result views: Overview, Table, By Confidence, By Page
- Document cards with expandable details
- Emphasizes the results panel

**Best For:**

- Users who need to see results while configuring workflow
- Power users who switch between different result views frequently
- Scenarios requiring detailed result analysis

---

### Design 3: Minimalist Cards

**Philosophy:** Clean, focused, card-based design with minimal clutter

**Key Features:**

- Streamlined horizontal process cards (1-2-3-4 steps)
- Collapsible document details in Corpus tab
- Segmented control for result views (Summary, Table, Analysis, Export)
- Cleaner visual style with less decorative elements
- Export view as dedicated section

**Best For:**

- Users who prefer simplicity and focus
- Teams that value clean, modern UIs
- Scenarios where screen real estate is limited
- Mobile or smaller screen experiences

---

## What Each Tab Contains

### Tab 1: Corpus Management

- Upload reference documents (multi-file)
- View current corpus documents
- Corpus configuration (case context, AI model, settings)
- Document management (delete, reindex)
- Corpus statistics

### Tab 2: Document Verification

**Left Side (Workflow):**

1. Upload document to verify
2. Select splitting mode (paragraph/sentence)
3. Run AI verification
4. Select output format
5. Generate and download

**Right Side (Results Pane):**

- Verification metrics and statistics
- Summary view with flagged items
- Detailed table view with all results
- Confidence distribution
- Source citations
- Review and analysis tools

---

## Design Notes

All mockups are **non-functional** - they demonstrate layout, visual design, and information architecture only. They use:

- Placeholder data
- Disabled buttons where appropriate
- Mock metrics and results
- Sample document lists

No backend integration or actual functionality is implemented in these mockups.

---

## Next Steps

1. Review all 3 designs
2. Choose preferred design (or combine elements)
3. Provide feedback on specific elements
4. Move to implementation phase
