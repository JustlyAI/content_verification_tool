# AI Verification - Implementation Fixes Required

**Status:** 65% Complete | **Critical Bug Present** | **Frontend Missing**

---

## Quick Summary

**What Works:**
- ✅ Data models complete and excellent
- ✅ API endpoints functional
- ✅ Output generation perfect (Word/Excel/JSON all include verification data)
- ✅ Documentation comprehensive

**What's Broken:**
- 🔴 **CRITICAL:** Verification uses Google Search instead of uploaded reference documents
- 🔴 **BLOCKER:** No frontend UI (feature invisible to users)
- 🟡 Missing citation extraction from grounding metadata
- 🟡 No retry logic for transient failures

**Time to Fix:** ~2.5 hours for critical items (bug fix + frontend)

---

## FIX #1: Critical Bug - File Search Not Used (30 minutes)

### Problem
`backend/app/gemini_service.py` line 245-251 uses Google Search instead of File Search corpora.

### Current (WRONG) Code
```python
# Line 245-251
tool = types.Tool(
    google_search_retrieval=types.GoogleSearchRetrieval(
        dynamic_retrieval_config=types.DynamicRetrievalConfig(
            mode="MODE_DYNAMIC"
        )
    )
)
```

### Fix Required

**Replace lines 244-260 with:**

```python
# Configure File Search tool with corpus
tool = types.Tool(
    file_search=types.FileSearch(
        corpora=[store_name]
    )
)

# Generate verification using Gemini Flash with File Search
response = self.client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=prompt,
    config=types.GenerateContentConfig(
        temperature=0.1,
        response_mime_type="application/json",
        tools=[tool]  # Pass the File Search tool here
    )
)
```

### Success Test
```bash
# 1. Upload references
curl -X POST "http://localhost:8000/api/verify/upload-references" \
  -F "case_context=Test case" \
  -F "files=@reference.pdf"

# 2. Run verification
curl -X POST "http://localhost:8000/api/verify/execute" \
  -H "Content-Type: application/json" \
  -d '{"document_id": "...", "store_id": "...", "case_context": "Test", "chunking_mode": "paragraph"}'

# 3. Check citations reference uploaded documents, not web
```

---

## FIX #2: Extract Grounding Metadata Citations (30 minutes)

### Problem
Citations come from AI JSON response only, not from actual document grounding.

### Location
`backend/app/gemini_service.py` line 264 (after `result = json.loads(response.text)`)

### Add After Line 264

```python
# Extract grounding metadata if available
actual_citations = []
if hasattr(response, 'candidates') and response.candidates:
    candidate = response.candidates[0]
    if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
        if hasattr(candidate.grounding_metadata, 'grounding_chunks'):
            cprint(f"[Gemini] Found {len(candidate.grounding_metadata.grounding_chunks)} grounding chunks", "cyan")

            for grounding_chunk in candidate.grounding_metadata.grounding_chunks:
                citation = {}

                # Extract title from document or web source
                if hasattr(grounding_chunk, 'document') and grounding_chunk.document:
                    citation["title"] = grounding_chunk.document.title if hasattr(grounding_chunk.document, 'title') else "Document"
                elif hasattr(grounding_chunk, 'web') and grounding_chunk.web:
                    citation["title"] = grounding_chunk.web.title if hasattr(grounding_chunk.web, 'title') else "Web Source"
                else:
                    citation["title"] = "Unknown Source"

                # Extract excerpt
                if hasattr(grounding_chunk, 'content') and hasattr(grounding_chunk.content, 'text'):
                    citation["excerpt"] = grounding_chunk.content.text
                else:
                    citation["excerpt"] = ""

                # Add URI if available
                if hasattr(grounding_chunk, 'web') and hasattr(grounding_chunk.web, 'uri'):
                    citation["uri"] = grounding_chunk.web.uri

                actual_citations.append(citation)

# Prefer grounding metadata citations over AI-generated ones
if actual_citations:
    cprint(f"[Gemini] Using {len(actual_citations)} actual grounding citations", "green")
    chunk.citations = actual_citations
else:
    cprint(f"[Gemini] No grounding metadata, using AI-generated citations", "yellow")
    chunk.citations = result.get("citations", [])
```

---

## FIX #3: Build Frontend UI (90 minutes)

### File: `frontend/app.py`

### Step 1: Add Reference Upload UI (after document upload succeeds)

**Insert after line ~350 (after document upload success message):**

```python
# Step 2: Upload Reference Documents for AI Verification
if st.session_state.document_id and not st.session_state.reference_docs_uploaded:
    st.markdown("---")
    st.markdown("### 🤖 Step 2: AI Verification (Optional)")
    st.markdown("Upload reference documents to automatically verify content using AI.")

    with st.expander("📚 Upload Reference Documents", expanded=False):
        case_context = st.text_area(
            "Case Context",
            placeholder="Describe what you're verifying (e.g., 'Contract verification for Project X')",
            max_chars=500,
            help="Provide context to help AI understand the verification case",
            key="case_context_input"
        )

        reference_files = st.file_uploader(
            "Select Reference Documents",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            help="Upload documents to verify against (PDF or DOCX)",
            key="reference_uploader"
        )

        if st.button("Create Reference Library", disabled=not reference_files or not case_context, type="primary"):
            with st.spinner("Creating reference library..."):
                try:
                    # Prepare files for upload
                    files = [
                        ("files", (file.name, file.getvalue(), file.type))
                        for file in reference_files
                    ]

                    # Call API
                    response = requests.post(
                        f"{API_BASE_URL}/api/verify/upload-references",
                        data={"case_context": case_context},
                        files=files,
                        timeout=300
                    )

                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.store_id = result["store_id"]
                        st.session_state.reference_docs_uploaded = True
                        st.session_state.case_context = case_context

                        st.success(f"✅ Uploaded {result['documents_uploaded']} reference documents")
                        st.info(f"📦 Store ID: `{result['store_id']}`")

                        # Show metadata
                        with st.expander("View Document Metadata"):
                            for meta in result["metadata"]:
                                st.markdown(f"**{meta['filename']}**")
                                st.caption(f"Type: {meta['document_type']}")
                                st.caption(f"Summary: {meta['summary']}")

                        st.rerun()
                    else:
                        st.error(f"❌ Failed to upload references: {response.text}")

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
```

### Step 2: Add Verification Trigger UI (after chunking mode selection)

**Insert after chunking is complete (around line ~450):**

```python
# Step 3: Run AI Verification
if st.session_state.chunks and st.session_state.reference_docs_uploaded and not st.session_state.verification_complete:
    st.markdown("---")
    st.markdown("### ✨ Step 3: Run AI Verification")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.info(f"📊 Ready to verify {len(st.session_state.chunks)} chunks against reference documents")
    with col2:
        if st.button("🚀 Verify Now", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                status_text.text("Starting verification...")

                # Call verification API
                response = requests.post(
                    f"{API_BASE_URL}/api/verify/execute",
                    json={
                        "document_id": st.session_state.document_id,
                        "store_id": st.session_state.store_id,
                        "case_context": st.session_state.case_context,
                        "chunking_mode": st.session_state.chunking_mode
                    },
                    timeout=600
                )

                progress_bar.progress(50)
                status_text.text("Processing verification results...")

                if response.status_code == 200:
                    result = response.json()
                    st.session_state.verification_complete = True
                    st.session_state.verification_results = result

                    progress_bar.progress(100)
                    status_text.text("Verification complete!")

                    # Show statistics
                    st.success("✅ AI Verification Complete!")

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Chunks", result["total_chunks"])
                    with col2:
                        verified_count = result["total_verified"]
                        verified_pct = (verified_count / result["total_chunks"] * 100) if result["total_chunks"] > 0 else 0
                        st.metric("Verified", f"{verified_count}", f"{verified_pct:.1f}%")
                    with col3:
                        st.metric("Processing Time", f"{result['processing_time_seconds']:.1f}s")
                    with col4:
                        # Calculate average confidence
                        scores = [c.get("verification_score", 0) for c in result["verified_chunks"] if c.get("verified") and c.get("verification_score")]
                        avg_score = sum(scores) / len(scores) if scores else 0
                        st.metric("Avg Confidence", f"{avg_score:.1f}/10")

                    st.rerun()
                else:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Verification failed: {response.text}")

            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Error during verification: {str(e)}")

# Show verification results summary if complete
if st.session_state.verification_complete:
    st.markdown("---")
    st.markdown("### 📊 Verification Results Summary")

    results = st.session_state.verification_results
    verified_count = results.get("total_verified", 0)
    total_count = results.get("total_chunks", 0)
    unverified_count = total_count - verified_count

    col1, col2 = st.columns(2)
    with col1:
        st.success(f"✅ **Verified:** {verified_count} chunks")
    with col2:
        st.warning(f"⚠️ **Unverified:** {unverified_count} chunks")

    # Show confidence breakdown
    if results.get("verified_chunks"):
        scores = [c.get("verification_score", 0) for c in results["verified_chunks"] if c.get("verified") and c.get("verification_score")]

        if scores:
            low_confidence = sum(1 for s in scores if s < 5)
            medium_confidence = sum(1 for s in scores if 5 <= s < 8)
            high_confidence = sum(1 for s in scores if s >= 8)

            st.markdown("**Confidence Distribution:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🔴 Low (<5)", low_confidence)
            with col2:
                st.metric("🟡 Medium (5-7)", medium_confidence)
            with col3:
                st.metric("🟢 High (8-10)", high_confidence)
```

### Step 3: Enhance Export Section

**Update the export section (around line ~550) to show verification status:**

```python
# Before the download button, add this:
if st.session_state.verification_complete:
    st.info("📊 This document includes AI verification results with confidence scores and citations")
```

---

## FIX #4: Add Retry Logic (15 minutes - Optional)

### Location
`backend/app/gemini_service.py` - Add new method before `verify_chunk()`

### Add This Method

```python
def _retry_with_backoff(self, func, *args, max_retries=3, **kwargs):
    """
    Retry a function with exponential backoff

    Args:
        func: Function to retry
        max_retries: Maximum number of retry attempts
        *args, **kwargs: Arguments to pass to function

    Returns:
        Function result
    """
    import time

    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt == max_retries - 1:
                # Last attempt, raise error
                raise

            # Check if error is retryable
            error_str = str(e).lower()
            is_retryable = any(x in error_str for x in [
                'rate limit', '429', 'timeout', '500', '503',
                'temporarily', 'unavailable', 'deadline'
            ])

            if not is_retryable:
                # Don't retry client errors
                raise

            # Exponential backoff: 1s, 2s, 4s
            wait_time = 2 ** attempt
            cprint(f"[Gemini] Retry {attempt + 1}/{max_retries} in {wait_time}s: {e}", "yellow")
            time.sleep(wait_time)
```

### Update verify_batch() to use retry

**Change line ~295 from:**
```python
verified_chunk = self.verify_chunk(chunk, store_name, case_context)
```

**To:**
```python
verified_chunk = self._retry_with_backoff(
    self.verify_chunk, chunk, store_name, case_context
)
```

---

## Testing Checklist

### After Fixing Bug
- [ ] Backend starts without errors
- [ ] Upload reference documents via API
- [ ] Verify chunks via API
- [ ] Check verification results reference uploaded docs (not web)
- [ ] Citations include document names and excerpts

### After Building Frontend
- [ ] Streamlit UI loads without errors
- [ ] Can upload reference documents via UI
- [ ] "Create Reference Library" button works
- [ ] Can trigger verification via UI
- [ ] Progress indicators show during processing
- [ ] Results display correctly
- [ ] Export includes verification data

### Complete Workflow Test
1. Start backend: `cd backend/app && python main.py`
2. Start frontend: `cd frontend && streamlit run app.py`
3. Upload main document (PDF/DOCX)
4. Upload 2-3 reference documents
5. Create reference library (should see success message)
6. Select chunking mode
7. Click "Verify Now" (should show progress)
8. Check results summary (verify stats make sense)
9. Export to Word/Excel (verify columns populated)

---

## Files to Modify

1. **backend/app/gemini_service.py** (~lines 245-270)
   - Fix File Search configuration
   - Add grounding metadata extraction
   - Add retry logic (optional)

2. **frontend/app.py** (~3 sections)
   - Add reference upload UI
   - Add verification trigger UI
   - Enhance export section

**Total Lines Changed:** ~150 lines across 2 files

---

## Success Criteria

✅ **Feature is complete when:**

1. Verification searches uploaded documents, not Google
2. Citations reference actual document content
3. Users can upload references via UI
4. Users can trigger verification via UI
5. Progress indicators work
6. Results display with statistics
7. All export formats include verification data
8. End-to-end workflow works smoothly

**Estimated Total Time:** 2.5 hours (bug fix + frontend)
