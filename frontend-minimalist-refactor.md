# Frontend Minimalist Card Refactor - Product Requirements Document

## Feature Overview

**Purpose**: Refactor the Content Verification Tool frontend from a sequential step-based layout to a clean, card-based design with tab navigation.

**Context**: The current UI uses a linear step-by-step wizard (Steps 1-4) with corpus management in an expander. The new design adopts a tab-based layout with two main sections: "📚 Corpus" and "✅ Verification", featuring card-based components and horizontal workflow visualization.

**Value Proposition**:

- **Cleaner UX**: Tab-based navigation separates concerns (corpus management vs document verification)
- **Better visual hierarchy**: Card-based layout with clear containers and dividers
- **Improved workflow visibility**: Horizontal process cards show all verification steps at once
- **Enhanced professionalism**: Minimalist design following modern UI patterns

**Constraints**:

- **NO new functionality** - only UI reorganization
- **Minimal placeholders** - keep existing features working
- **MVP approach** - only essential changes to achieve design direction

---

## Requirements Analysis

### Core Requirements

1. **Tab-based navigation**: Two main tabs - "📚 Corpus" and "✅ Verification"
2. **Card-based layout**: Use `st.container()` to create visual card groupings
3. **Horizontal workflow**: Display verification steps as 4 horizontal cards
4. **Corpus tab**: Dedicated space for corpus management (expanded from current expander)
5. **All existing functionality preserved**: No features removed or broken
6. **Existing API integration unchanged**: All backend calls remain identical

### Success Criteria

- [ ] Application loads without errors
- [ ] Users can navigate between Corpus and Verification tabs
- [ ] All existing features work identically (upload, chunking, verification, export)
- [ ] UI follows card-based design patterns from mockup
- [ ] Corpus management has dedicated tab space
- [ ] Verification workflow displays as horizontal cards
- [ ] No console errors or warnings

### Dependencies

- Existing modules: `app/main.py`, `app/ui_components.py`, `app/corpus.py`, `app/state.py`
- Streamlit version: 1.28+ (supports `st.tabs()`)
- All backend APIs remain unchanged

### Constraints

- Cannot break existing functionality
- Must preserve all session state management
- Keep existing file structure (no major reorganization)
- Avoid adding placeholder features that don't exist yet

---

## Technical Architecture

### UI Structure Changes

**Current Structure:**

```
Header
Backend Status
Sidebar
Corpus Expander (collapsed)
────────────
Step 1: Upload
Step 2: Chunking
Step 2.5: AI Verification
Step 3: Output Format
Step 4: Generate
────────────
Footer
```

**New Structure:**

```
Header
Backend Status
Sidebar
────────────
Tab 1: 📚 Corpus          Tab 2: ✅ Verification
────────────────────────  ────────────────────────
[Corpus Management]       [4 Horizontal Cards]
[Upload References]       Card 1: Upload
[Document Library]        Card 2: Chunking
[Configuration]           Card 3: Verify
[Statistics]              Card 4: Export

                          [Results Section]
                          - Summary metrics
                          - Verification details
────────────
Footer
```

### Component Changes

| Current Component                       | New Location              | Changes                            |
| --------------------------------------- | ------------------------- | ---------------------------------- |
| `render_corpus_management()`            | Corpus Tab                | Expanded to full tab, not expander |
| `render_document_upload()`              | Verification Tab → Card 1 | Contained in card                  |
| `render_chunking_selection()`           | Verification Tab → Card 2 | Contained in card                  |
| `render_ai_verification()`              | Verification Tab → Card 3 | Contained in card                  |
| `render_output_format_selection()`      | Verification Tab → Card 4 | Contained in card                  |
| `render_generate_document()`            | Verification Tab → Card 4 | Merged with export                 |
| `render_verification_results_summary()` | Below cards               | Enhanced with metrics              |

### Files to Modify

1. **`frontend/main.py`** - Main application structure

   - Replace linear steps with tab-based layout
   - Create horizontal card layout for verification workflow
   - Reorganize component rendering order

2. **`frontend/app/ui_components.py`** - UI component functions

   - Add card wrapper functions
   - Update rendering for card contexts
   - Add metrics display helpers

3. **`frontend/app/corpus.py`** - Corpus management
   - Remove expander wrapper (becomes full tab)
   - Enhanced layout for dedicated tab space
   - Keep all existing functionality

---

## Implementation Phases

### Phase 1: Tab Structure Foundation (~30 minutes)

**Objective**: Replace linear layout with tab-based navigation

**Tasks**:

- [ ] Add tab creation at top of main content area
- [ ] Move corpus management to Tab 1 (remove expander wrapper)
- [ ] Move verification workflow to Tab 2
- [ ] Test tab switching maintains session state

**Files Modified**:

- `frontend/main.py` - Add `st.tabs()` after backend status
- `frontend/app/corpus.py` - Remove expander, render directly

**Code Changes**:

```python
# In main.py, replace corpus expander + steps with:
tab1, tab2 = st.tabs(["📚 Corpus", "✅ Verification"])

with tab1:
    render_corpus_tab()  # New function

with tab2:
    render_verification_tab()  # New function
```

**Verification**:

- [ ] Both tabs load without errors
- [ ] Switching tabs preserves state
- [ ] All existing functionality accessible

---

### Phase 2: Horizontal Verification Cards (~45 minutes)

**Objective**: Convert sequential steps to 4 horizontal cards

**Tasks**:

- [ ] Create horizontal column layout (4 cards)
- [ ] Card 1: Upload document section
- [ ] Card 2: Chunking mode selection
- [ ] Card 3: AI verification (if corpus active)
- [ ] Card 4: Output format + generate/download
- [ ] Add visual card containers with `st.container()`

**Files Modified**:

- `frontend/main.py` - Create `render_verification_tab()` function
- `frontend/app/ui_components.py` - Add card rendering helpers

**Code Structure**:

```python
def render_verification_tab():
    """Render Verification tab with horizontal cards"""
    st.header("Document Verification")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container():
            st.markdown("### 1️⃣ Upload")
            render_upload_card()

    with col2:
        with st.container():
            st.markdown("### 2️⃣ Chunking")
            render_chunking_card()

    with col3:
        with st.container():
            st.markdown("### 3️⃣ Verify")
            render_verify_card()

    with col4:
        with st.container():
            st.markdown("### 4️⃣ Export")
            render_export_card()

    # Results below cards
    if st.session_state.document_info:
        st.divider()
        render_results_section()
```

**Verification**:

- [ ] All 4 cards display horizontally
- [ ] Upload functionality works in Card 1
- [ ] Chunking selection works in Card 2
- [ ] Verification triggers in Card 3
- [ ] Export/download works in Card 4

---

### Phase 3: Enhanced Corpus Tab (~30 minutes)

**Objective**: Create dedicated corpus management tab with better layout

**Tasks**:

- [ ] Remove expander wrapper from corpus components
- [ ] Create two-column layout (main + sidebar)
- [ ] Left column: Upload + document library (placeholder for future)
- [ ] Right column: Configuration + statistics
- [ ] Add status banner at top

**Files Modified**:

- `frontend/app/corpus.py` - Refactor for full tab layout

**Code Structure**:

```python
def render_corpus_tab():
    """Render Corpus tab with expanded layout"""
    st.header("Reference Corpus")

    # Status banner
    if st.session_state.reference_docs_uploaded:
        st.success("✅ Corpus Active | Ready for verification")
    else:
        st.warning("⚠️ Corpus Not Configured")

    st.divider()

    # Two-column layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Upload section
        if not st.session_state.reference_docs_uploaded:
            render_corpus_creation()
        else:
            render_active_corpus()

    with col2:
        # Stats and actions
        render_corpus_stats()
        render_corpus_actions()
```

**Verification**:

- [ ] Corpus creation works in dedicated tab
- [ ] Active corpus displays in expanded layout
- [ ] Statistics show in right column
- [ ] All existing corpus functionality preserved

---

### Phase 4: Results Section Enhancement (~25 minutes)

**Objective**: Improve results display below verification cards

**Tasks**:

- [ ] Add metrics row (chunks, verified, confidence, time)
- [ ] Move existing verification summary below metrics
- [ ] Add clear visual separation from cards
- [ ] Keep download button accessible

**Files Modified**:

- `frontend/app/ui_components.py` - Enhance `render_verification_results_summary()`

**Code Structure**:

```python
def render_results_section():
    """Render results section below verification cards"""
    if not st.session_state.verification_complete:
        return

    st.subheader("Results")

    # Metrics row
    results = st.session_state.verification_results
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Chunks", results.get("total_chunks", 0))
    with col2:
        st.metric("Verified", results.get("total_verified", 0))
    with col3:
        avg_score = calculate_avg_score(results)
        st.metric("Confidence", f"{avg_score:.1f}/10")
    with col4:
        st.metric("Time", f"{results.get('processing_time_seconds', 0):.1f}s")

    st.divider()

    # Existing summary (enhanced)
    render_verification_details()
```

**Verification**:

- [ ] Results display below cards
- [ ] Metrics show correct data
- [ ] Summary shows confidence breakdown
- [ ] Download button remains accessible

---

### Phase 5: Polish & Testing (~20 minutes)

**Objective**: Final cleanup and comprehensive testing

**Tasks**:

- [ ] Remove unused code/comments
- [ ] Ensure consistent spacing and dividers
- [ ] Test full workflow: Corpus → Upload → Chunk → Verify → Export
- [ ] Test edge cases (no corpus, verification errors, etc.)
- [ ] Verify responsive behavior with different screen sizes
- [ ] Check sidebar still functions correctly

**Verification Checklist**:

- [ ] Full happy path works (with corpus)
- [ ] Basic path works (without corpus)
- [ ] Tab switching maintains state
- [ ] All buttons function correctly
- [ ] Error handling displays properly
- [ ] Download works for all formats
- [ ] Start Over button resets correctly
- [ ] No console errors or warnings
- [ ] Performance is acceptable

---

## File Structure Impact

### Files Modified

| File                            | Change Type      | Description                                 |
| ------------------------------- | ---------------- | ------------------------------------------- |
| `frontend/main.py`              | Major refactor   | Replace linear steps with tab + card layout |
| `frontend/app/ui_components.py` | Moderate updates | Add card helpers, enhance results display   |
| `frontend/app/corpus.py`        | Minor refactor   | Remove expander wrapper, expand layout      |
| `frontend/app/state.py`         | No changes       | Session state management unchanged          |
| `frontend/app/api_client.py`    | No changes       | API calls unchanged                         |
| `frontend/app/config.py`        | No changes       | Configuration unchanged                     |

### Files Created

None - all changes are modifications to existing files

### Files Tested

- All modified files require testing
- Focus on `main.py` as primary entry point
- Verify `corpus.py` tab layout
- Check `ui_components.py` for any issues

---

## Development Guidelines

### Code Patterns

1. **Use containers for cards**:

   ```python
   with st.container():
       st.markdown("### Card Title")
       # Card content
   ```

2. **Maintain session state patterns**:

   - Continue using `st.session_state` for all state
   - Keep existing state variable names
   - Preserve reset functions

3. **Keep API integration unchanged**:

   - All `api_client` calls remain identical
   - No changes to request/response handling
   - Maintain error handling patterns

4. **Follow existing logging**:
   - Keep termcolor cprint statements
   - Maintain logging.logger usage
   - Don't remove debug output

### UI Consistency

- Use `st.divider()` between major sections
- Use `st.header()` for main sections
- Use `st.subheader()` for subsections
- Use `st.markdown("### Title")` for card titles
- Maintain emoji usage for visual hierarchy

### Error Handling

- Preserve all existing error messages
- Keep validation logic unchanged
- Maintain spinner/progress indicators
- Don't change error display patterns

---

## Success Metrics

### Functional Metrics

- [ ] 100% feature parity with current version
- [ ] Zero new bugs introduced
- [ ] All existing test cases pass (if any)
- [ ] No performance degradation

### UX Metrics

- [ ] Tab navigation works smoothly
- [ ] Cards display properly in horizontal layout
- [ ] Mobile/responsive behavior acceptable
- [ ] Visual hierarchy improved over current version

### Code Quality

- [ ] No additional dependencies required
- [ ] Code remains maintainable
- [ ] Module separation preserved
- [ ] No code duplication introduced

---

## Risks & Mitigation

### Risk: Breaking existing functionality

**Mitigation**:

- Test each phase independently before proceeding
- Keep session state management unchanged
- Preserve all API calls and error handling
- Test full workflow after each major change

### Risk: Tab switching state loss

**Mitigation**:

- Streamlit tabs automatically preserve state
- Verify state persistence after Phase 1
- Keep all state in `st.session_state` (already done)

### Risk: Horizontal cards too cramped on smaller screens

**Mitigation**:

- Test on different screen sizes
- Streamlit's column layout is responsive
- Consider adjusting column widths if needed
- Can add responsive breakpoints if necessary

### Risk: Corpus tab feels empty when not configured

**Mitigation**:

- Add clear instructions and call-to-action
- Keep status banner visible
- Show benefits of configuring corpus
- This is acceptable for MVP - no placeholder content needed

---

## Timeline Estimate

| Phase                        | Duration | Cumulative |
| ---------------------------- | -------- | ---------- |
| Phase 1: Tab Structure       | 30 min   | 30 min     |
| Phase 2: Horizontal Cards    | 45 min   | 75 min     |
| Phase 3: Enhanced Corpus Tab | 30 min   | 105 min    |
| Phase 4: Results Enhancement | 25 min   | 130 min    |
| Phase 5: Polish & Testing    | 20 min   | 150 min    |

**Total Estimated Time**: ~2.5 hours

---

## Post-Refactor Considerations

### Future Enhancements (Out of Scope)

These are design elements from the mockup that are NOT included in this MVP refactor:

- Document library view with search (corpus tab)
- Multiple result views with segmented control (Summary/Table/Analysis/Export tabs)
- Advanced filtering in results table
- Charts and analytics views
- Export preview functionality
- Configuration settings in corpus tab (model selection, thresholds)

### Maintenance Notes

- New tab-based structure easier to extend with future features
- Card layout supports adding more workflow steps if needed
- Corpus tab has room for document library UI later
- Results section can easily add view modes in future

---

## Acceptance Criteria

**Definition of Done**:

1. ✅ Application runs without errors
2. ✅ Two tabs present and functional (Corpus, Verification)
3. ✅ Corpus management works in dedicated tab
4. ✅ Verification workflow displays as 4 horizontal cards
5. ✅ All existing features work identically:
   - Document upload and processing
   - Chunking mode selection
   - AI verification (when corpus active)
   - Output format selection
   - Document generation and download
   - Corpus creation and clearing
6. ✅ Results section displays below cards with metrics
7. ✅ Session state preserved across tab switches
8. ✅ No console errors or warnings
9. ✅ Sidebar functionality unchanged
10. ✅ Footer displays correctly

**Testing Scenarios**:

1. **No Corpus + Generate**: Upload doc → Select chunking → Select format → Generate → Download
2. **With Corpus + Verify**: Create corpus → Upload doc → Select chunking → Verify → Generate → Download
3. **Tab Switching**: Switch between tabs at various workflow stages
4. **Start Over**: Complete workflow → Start Over → Verify clean state
5. **Error Handling**: Test with invalid files, backend down, etc.

---

## Notes

- This refactor focuses purely on UI reorganization
- No new features or placeholders added
- All existing backend integration preserved
- Minimum viable changes to achieve design direction
- Future enhancements can build on this foundation
- Streamlit's native components used throughout (no custom CSS)
