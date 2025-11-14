# Corpus Management Panel Refactor - Product Requirements Document

## Feature Overview

**Purpose**: Refactor the Streamlit frontend to provide independent, always-accessible corpus (reference document) management through a native Streamlit expander UI, removing it from the linear wizard workflow.

**Context**: Currently, corpus creation is embedded as "Step 1.5" in the document verification wizard, making it feel like an optional afterthought and tightly coupling it to the document upload flow. This refactor decouples corpus management into a standalone feature accessible at any time.

**Value Proposition**:
- Users can create and manage reference document corpuses independently of verifying documents
- Improved UX using vanilla Streamlit components (no custom CSS)
- Better discoverability of AI verification capabilities
- Allows corpus reuse across multiple document verification sessions
- Simple, maintainable implementation

## Requirements Analysis

### Core Requirements

1. **Independent Corpus Management**
   - Remove corpus creation from "Step 1.5" in the wizard
   - Create a persistent expander section at the top of the page
   - Expander state can be open/closed
   - Corpus state persists across Streamlit reruns

2. **Expander Functionality**
   - Expander always visible with clear label indicating corpus status
   - Expander contains all corpus management features:
     - Create new corpus (case context + file upload)
     - View active corpus information
     - Display corpus metadata (documents, keywords, summaries)
     - Clear/reset corpus functionality
   - Uses native `st.expander()` component

3. **Session State Integration**
   - Maintain existing corpus state variables
   - No need for panel visibility state (handled by expander)
   - Ensure corpus persists when expander is collapsed

4. **UI/UX Requirements**
   - Use vanilla Streamlit components only
   - No custom CSS or HTML
   - Clear visual indicator of corpus status in expander label
   - Expander can be collapsed to save space

### Success Criteria

- [ ] Corpus creation is completely independent of document upload workflow
- [ ] Corpus expander is accessible from the top of the page at all times
- [ ] Users can create corpus at any time during the workflow
- [ ] Existing verification functionality works identically
- [ ] Corpus state persists when expander is collapsed
- [ ] No regression in existing features (upload, chunking, export)
- [ ] Uses only vanilla Streamlit components (no custom CSS/HTML)

### Dependencies

- Existing Streamlit session state management
- Current Gemini service integration (`/api/verify/upload-references`)
- Backend API endpoints remain unchanged

### Constraints

- Use vanilla Streamlit components only (no custom CSS/HTML)
- Must maintain single-file frontend architecture (no component split yet)
- Cannot break existing Docker deployment
- Must work with current backend API without changes

## Technical Architecture

### Frontend Changes (frontend/app.py)

**No Database Changes**: This is a frontend-only refactor

**No API Changes**: Existing endpoints remain the same:
- `POST /api/verify/upload-references`
- `POST /api/verify/execute`

### UI Component Structure

```
┌──────────────────────────────────────────────────┐
│  Header                                          │
├──────────────────────────────────────────────────┤
│  🤖 AI Reference Corpus [✅ Active / ⚠️ None]   │
│  ▼ Manage Corpus (expandable)                    │
│    ├─ Create Corpus                              │
│    ├─ View Corpus Info & Metadata                │
│    └─ Clear Corpus                               │
├──────────────────────────────────────────────────┤
│                                                  │
│  Main Content (Wizard Steps)                     │
│                                                  │
│  Step 1: Upload Document                         │
│  Step 2: Chunking Mode                           │
│  Step 2.5: Run AI Verification (if corpus active)│
│  Step 3: Output Format                           │
│  Step 4: Generate & Download                     │
│                                                  │
└──────────────────────────────────────────────────┘
```

### Native Streamlit Components

Using vanilla Streamlit only:
```python
# Corpus expander at top of page
with st.expander(
    "🤖 AI Reference Corpus - " +
    ("✅ Active" if st.session_state.reference_docs_uploaded else "⚠️ Not Configured"),
    expanded=False
):
    # All corpus management UI here
    if st.session_state.reference_docs_uploaded:
        # Show active corpus info
        # Clear button
    else:
        # Corpus creation form
```

### Session State Changes

**No New State Variables Needed** - Expander state is managed by Streamlit

**Existing State Variables** (unchanged):
```python
st.session_state.store_id              # Corpus ID
st.session_state.reference_docs_uploaded  # Has corpus
st.session_state.case_context          # Context text
st.session_state.verification_complete    # Verification status
st.session_state.verification_results     # Results cache
```

## Implementation Phases

### Phase 1: Foundation - Expander Structure (~20 minutes)

**Objective**: Create corpus management expander at top of page using vanilla Streamlit

**Tasks**:
- [ ] Add corpus expander before main wizard content
- [ ] Create dynamic expander label showing corpus status
- [ ] Structure expander with conditional UI (active vs inactive corpus)
- [ ] No custom CSS or HTML needed

**Files Modified**:
- `frontend/app.py`:
  - Line ~320-360: Add corpus expander after header, before Step 1
  - Create `render_corpus_management()` helper function

**Implementation Details**:
```python
def render_corpus_management():
    """Render corpus management UI in expander"""

    # Dynamic label based on corpus status
    if st.session_state.reference_docs_uploaded:
        label = "🤖 AI Reference Corpus - ✅ Active"
        expanded_default = False  # Collapsed when active
    else:
        label = "🤖 AI Reference Corpus - ⚠️ Not Configured"
        expanded_default = False  # Let user expand when needed

    with st.expander(label, expanded=expanded_default):
        if st.session_state.reference_docs_uploaded:
            # Show active corpus UI
            render_active_corpus()
        else:
            # Show corpus creation form
            render_corpus_creation()

# Place in main() after header, before Step 1
render_corpus_management()
```

**Verification**:
- [ ] Expander appears at top of page with correct label
- [ ] Label shows corpus status (Active/Not Configured)
- [ ] Expander can be expanded/collapsed
- [ ] State persists across reruns

### Phase 2: Extract Corpus UI (~30 minutes)

**Objective**: Move corpus creation UI from Step 1.5 into the expander

**Tasks**:
- [ ] Create `render_corpus_creation()` function (for inactive state)
- [ ] Create `render_active_corpus()` function (for active state)
- [ ] Copy corpus creation UI from lines 458-528 into creation function
- [ ] Add corpus metadata display to active function
- [ ] Remove old Step 1.5 UI from wizard flow
- [ ] Add "clear corpus" functionality

**Files Modified**:
- `frontend/app.py`:
  - Line 458-528: Delete old "Step 1.5" UI section
  - Add two new helper functions:
    - `render_corpus_creation()` - Creation form
    - `render_active_corpus()` - Active corpus display

**Implementation Details**:
```python
def render_corpus_creation():
    """Render corpus creation form (when no active corpus)"""
    st.markdown("Upload reference documents to enable AI verification")

    case_context = st.text_area(
        "Case Context",
        placeholder="Describe what you're verifying (e.g., 'Contract verification for Project X')",
        max_chars=500,
        help="Provide context to help AI understand the verification case",
        key="case_context_input",
    )

    reference_files = st.file_uploader(
        "Select Reference Documents",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        help="Upload documents to verify against (PDF or DOCX)",
        key="reference_uploader",
    )

    if st.button(
        "Create Reference Library",
        disabled=not reference_files or not case_context,
        type="primary",
        use_container_width=True
    ):
        # Existing creation logic from lines 487-528
        ...

def render_active_corpus():
    """Render active corpus information and management"""
    st.success("✅ Corpus is active and ready for verification")
    st.info(f"📦 Store ID: `{st.session_state.store_id}`")

    # Display metadata if stored
    if hasattr(st.session_state, 'corpus_metadata'):
        with st.expander("📄 View Document Metadata", expanded=False):
            for meta in st.session_state.corpus_metadata:
                st.markdown(f"**{meta['filename']}**")
                st.caption(f"Type: {meta['document_type']}")
                st.caption(f"Summary: {meta['summary']}")

    st.divider()

    # Clear corpus button
    col1, col2 = st.columns([1, 1])
    with col2:
        if st.button("🗑️ Clear Corpus", type="secondary", use_container_width=True):
            st.session_state.store_id = None
            st.session_state.reference_docs_uploaded = False
            st.session_state.case_context = None
            if hasattr(st.session_state, 'corpus_metadata'):
                delattr(st.session_state, 'corpus_metadata')
            st.rerun()
```

**Verification**:
- [ ] Expander contains all corpus management features
- [ ] Creating corpus works identically to before
- [ ] Corpus status shows correctly in expander
- [ ] Metadata displays properly when expanded
- [ ] Clear corpus button resets state
- [ ] Step 1.5 UI is completely removed from wizard

### Phase 3: Integration & Workflow Updates (~20 minutes)

**Objective**: Update the verification workflow to work with the new expander location

**Tasks**:
- [ ] Remove Step 1.5 section completely
- [ ] Update Step 2.5 visibility (keep existing logic)
- [ ] Add helper prompts to guide users to expander
- [ ] Ensure wizard numbering makes sense

**Files Modified**:
- `frontend/app.py`:
  - Line 458-528: Delete entire Step 1.5 section
  - Line ~394-456: Add tip in Step 1 if no corpus exists
  - Line ~554-639: Keep Step 2.5 as-is (already checks for corpus)

**Implementation Details**:
```python
# In Step 1 (after file upload)
st.header("Step 1: Upload Document To Verify")
if not st.session_state.reference_docs_uploaded:
    st.info("💡 **Tip**: Expand 'AI Reference Corpus' above to enable automated verification")

# In Step 2 (chunking mode)
st.header("Step 2: Select Chunking Mode")
if st.session_state.reference_docs_uploaded:
    st.success("🤖 AI Verification is enabled - you'll be able to run verification after selecting chunking mode")

# Step 2.5 visibility - NO CHANGES NEEDED
# Already checks: if st.session_state.reference_docs_uploaded and not st.session_state.verification_complete
```

**Verification**:
- [ ] Step 1.5 is completely removed
- [ ] Users see helpful prompts to use expander
- [ ] Verification step (2.5) appears when corpus is active
- [ ] Workflow feels natural and intuitive
- [ ] No confusing step numbering

### Phase 4: Polish & Testing (~20 minutes)

**Objective**: Add final touches, improve UX, and comprehensive testing

**Tasks**:
- [ ] Add loading states when creating corpus
- [ ] Improve error handling in expander
- [ ] Save corpus metadata to session state for display
- [ ] Comprehensive testing of all workflows
- [ ] Update documentation

**Files Modified**:
- `frontend/app.py`:
  - Enhance error messages in corpus creation
  - Store metadata in session state after upload
- `README.md`:
  - Update AI Verification section to reflect new UI
  - Update workflow description

**Implementation Details**:
```python
# In corpus creation success handler
if response.status_code == 200:
    result = response.json()
    st.session_state.store_id = result["store_id"]
    st.session_state.reference_docs_uploaded = True
    st.session_state.case_context = case_context
    st.session_state.corpus_metadata = result["metadata"]  # Save for display

    st.success(f"✅ Uploaded {result['documents_uploaded']} reference documents")
    st.rerun()
```

**Verification**:
- [ ] Full workflow test: Expand expander → Create corpus → Upload doc → Verify → Export
- [ ] Test with and without corpus at each step
- [ ] Test corpus creation, verification, and clearing
- [ ] Error handling shows helpful messages
- [ ] Performance is acceptable (no lag)
- [ ] Documentation is updated
- [ ] Expander label updates correctly based on corpus state

### Phase 5: Final Report & Handoff (~10 minutes)

**Objective**: Document changes and provide comprehensive status report

**Tasks**:
- [ ] Create implementation summary document
- [ ] Document any technical debt or future improvements
- [ ] List all modified files with line ranges
- [ ] Note any breaking changes (none expected)
- [ ] Provide testing checklist for validation

**Deliverables**:
- Implementation summary in `.plans/corpus-panel-implementation-report.md`
- Updated `README.md` with new UI flow
- Testing checklist for validation

**Verification**:
- [ ] All documentation is accurate
- [ ] Implementation report is complete
- [ ] Testing checklist covers all scenarios

## Success Metrics

**Functional Metrics**:
- All existing features work without regression
- Corpus creation works identically from expander
- Expander expand/collapse works smoothly
- Users can access corpus management at any time

**UX Metrics**:
- Reduced steps in main wizard (no Step 1.5)
- Clearer separation of concerns (verify vs manage corpus)
- More discoverable AI verification feature
- Simple, clean UI using native Streamlit components

**Technical Metrics**:
- No performance degradation
- Session state remains stable
- No custom CSS/HTML (vanilla Streamlit only)
- Single-file architecture maintained

## File Structure Impact

### Files Modified

**Primary Changes**:
- `frontend/app.py` (~850 lines):
  - Add corpus expander before Step 1 (line ~320)
  - Remove Step 1.5 UI (delete lines 458-528)
  - Add helper functions:
    - `render_corpus_management()` - Main expander wrapper
    - `render_corpus_creation()` - Creation form
    - `render_active_corpus()` - Active corpus display
  - Update Step 1 and Step 2 with helper tips
  - Store corpus_metadata in session state

**Documentation Updates**:
- `README.md`:
  - Update "AI Verification (NEW)" section (lines 121-262)
  - Add description of new panel UI
  - Update workflow steps

**New Files**:
- `.plans/corpus-panel-refactor.md` (this document)
- `.plans/corpus-panel-implementation-report.md` (created in Phase 5)

### Files Unchanged

- `backend/app/main.py` - No changes needed
- `backend/app/gemini_service.py` - No changes needed
- `backend/app/models.py` - No changes needed
- All other backend files - No changes needed

## Development Guidelines

### Code Patterns

- **Streamlit Conventions**: Use `st.session_state` for all stateful data
- **Naming**: Use snake_case for functions, UPPER_CASE for constants
- **Comments**: Add docstrings to new functions
- **Vanilla Streamlit Only**: No custom CSS, HTML, or JavaScript

### Error Handling

- Maintain existing try/catch patterns around API calls
- Show user-friendly error messages in expander
- Log errors with `cprint()` for debugging

### Security

- No new security concerns (frontend-only change)
- Maintain existing API call patterns
- No changes to authentication or authorization

### Performance

- Native Streamlit components (no custom rendering)
- Expander rendering is lightweight (no heavy computations)
- Session state updates are minimal
- Avoid unnecessary reruns

## Risks & Mitigation

### Risk 1: Session State Synchronization

**Risk**: Expander state might desync with corpus state after rerun

**Mitigation**:
- Test rerun behavior thoroughly
- Use keys for all interactive elements
- Add state validation checks
- Rely on corpus state (not expander state) for logic

### Risk 2: Breaking Existing Workflows

**Risk**: Moving corpus UI might break user expectations

**Mitigation**:
- Thorough testing of all workflows
- Keep verification behavior identical
- Add helpful prompts to guide users

## Future Enhancements

**Post-MVP Improvements**:
1. Multiple corpus management (list, switch between corpuses)
2. Corpus editing (add/remove documents)
3. Corpus sharing (export/import)
4. Corpus analytics (usage stats, verification history)
5. Nested expanders for advanced settings
6. Corpus search/filter functionality

**Technical Debt**:
- Eventually split frontend into modular components
- Add unit tests for panel logic
- Migrate to Redis for corpus persistence
- Add SSE for real-time verification progress

## Implementation Timeline

**Total Estimated Time**: ~1.5 hours

- Phase 1 (Foundation): 20 minutes
- Phase 2 (Extract UI): 30 minutes
- Phase 3 (Integration): 20 minutes
- Phase 4 (Polish): 20 minutes
- Phase 5 (Report): 10 minutes

**Suggested Approach**: Implement phases sequentially, testing after each phase before proceeding.

---

**Document Version**: 2.0 (Updated for Vanilla Streamlit)
**Created**: 2025-11-13
**Updated**: 2025-11-13
**Status**: Ready for Implementation
