# AI Verification Layer - Product Requirements Document

## Feature Overview

**Purpose**: Transform the Content Verification Tool from a manual checklist generator into an AI-powered verification system that automatically verifies document chunks against reference documents using Google Gemini AI.

**Context**: The current system generates empty verification checklists with 6 columns (Page #, Item #, Text, Verified ☑, Verification Source, Verification Note). Users manually fill these columns. This feature will use Gemini's File Search Tool to automatically verify chunks and pre-populate verification fields.

**Value Proposition**:

- **90% time savings**: AI verifies hundreds of chunks in minutes vs. hours of manual work
- **Citation-backed results**: Every verification includes source references from uploaded documents
- **Confidence scoring**: 1-10 scale helps prioritize human review
- **Cost-effective**: $0.15/1M tokens for indexing, free embeddings/storage

## Requirements Analysis

### Core Requirements

1. Upload multiple reference documents (PDF/DOCX) for a verification case
2. Create Gemini File Search store with metadata-enriched documents
3. Verify each chunked item against the document store using Gemini 2.5 Flash
4. Return verification results with: verified (bool), confidence_score (1-10), source citations, reasoning
5. Export fully-populated verification documents (Word/Excel/CSV) with AI results

### Success Criteria

- ✅ System successfully creates File Search stores and uploads documents
- ✅ AI verification completes for 100+ chunk documents in <5 minutes
- ✅ Verification results include citations with page/section references
- ✅ Exported documents contain pre-filled verification columns
- ✅ Cost stays under $0.50 per document verification (typical 50-page case)

### Dependencies

- Google GenAI Python SDK (>=1.43.0)
- Existing document processing pipeline (Docling, chunking)
- FastAPI backend and Streamlit frontend
- GEMINI_API_KEY environment variable

### Constraints

- Gemini API rate limits: Use batch processing with delays
- File Search store limit: One store per verification session
- Max file size: 10 MB (current system limit)
- Processing time: Must show progress to users

## Technical Architecture

### Database Changes

**New Models** (backend/app/models.py):

```python
class DocumentMetadata(BaseModel):
    document_id: str
    filename: str
    summary: str
    contextualization: str
    document_type: str
    keywords: List[str]
    generated_at: datetime

class VerificationResult(BaseModel):
    verified: bool
    confidence_score: int  # 1-10
    verification_source: str
    verification_note: str
    citations: List[dict]
    verified_at: datetime

class DocumentChunk(BaseModel):  # Extended
    # Existing fields...
    verified: Optional[bool] = None
    verification_score: Optional[int] = None
    verification_source: Optional[str] = None
    verification_note: Optional[str] = None
    citations: Optional[List[dict]] = None

class VerificationRequest(BaseModel):
    document_id: str
    case_context: str
    reference_documents: List[UploadFile]
    chunking_mode: ChunkingMode

class VerificationResponse(BaseModel):
    document_id: str
    verified_chunks: List[DocumentChunk]
    total_verified: int
    total_chunks: int
    store_id: str
```

### API Design

**POST /api/verify/upload-references**

```python
# Upload reference documents and create File Search store
Request: {
  "case_context": str,
  "files": List[File]
}
Response: {
  "store_id": str,
  "store_name": str,
  "documents_uploaded": int,
  "metadata": List[DocumentMetadata]
}
```

**POST /api/verify/execute**

```python
# Run verification on chunked document
Request: {
  "document_id": str,
  "store_id": str,
  "case_context": str,
  "chunking_mode": "paragraph" | "sentence"
}
Response: {
  "document_id": str,
  "verified_chunks": List[DocumentChunk],
  "total_verified": int,
  "total_chunks": int,
  "processing_time_seconds": float
}
```

**POST /api/verify/export**

```python
# Export with verification results
Request: {
  "document_id": str,
  "output_format": "word_landscape" | "word_portrait" | "excel" | "csv" | "json"
}
Response: FileResponse
```

### Frontend Components

**New UI Sections** (frontend/app.py):

1. **Step 0.5**: "Upload Reference Documents" (after document upload)

   - Multi-file upload with drag-drop
   - Case context text area
   - "Create Reference Library" button
   - Progress indicator for upload/indexing

2. **Step 2.5**: "Run AI Verification" (after chunking mode selection)

   - "Verify Against References" button
   - Progress bar showing chunk verification
   - Preview of verification results

3. **Step 4**: Enhanced export with verification data visualization
   - Summary stats (% verified, avg confidence)
   - Color-coded confidence scores
   - Download button for verified document

### Integration Points

**New Service Module** (backend/app/gemini_service.py):

- `GeminiVerificationService` class
- Methods: `create_store()`, `upload_document()`, `generate_metadata()`, `verify_chunk()`, `verify_batch()`

**Modified Modules**:

- `models.py`: Add verification fields
- `output_generator.py`: Populate verification columns with AI results
- `main.py`: Add verification endpoints

## Implementation Phases

### Phase 1: Foundation & Models (~45 minutes)

**Objective**: Install dependencies, extend data models, create Gemini service skeleton

**Tasks**:

- [ ] Add `google-genai>=1.43.0` to backend/requirements.txt
- [ ] Install package and verify import works
- [ ] Extend `DocumentChunk` model with verification fields
- [ ] Create `DocumentMetadata`, `VerificationRequest`, `VerificationResponse` models
- [ ] Add `OutputFormat.JSON` enum value
- [ ] Create `backend/app/gemini_service.py` with GeminiVerificationService class skeleton
- [ ] Add GEMINI_API_KEY to .env.example

**Files Modified**:

- `backend/requirements.txt` - Add google-genai dependency
- `backend/app/models.py` - Add verification models and extend DocumentChunk
- `backend/app/gemini_service.py` - **NEW FILE** - Create service class
- `.env.example` - **NEW FILE** - Add GEMINI_API_KEY template

**Verification**:

- [ ] `pip install -r backend/requirements.txt` succeeds
- [ ] `from google import genai` imports without errors
- [ ] Models validate with Pydantic (run `python -c "from app.models import *"`)
- [ ] Service class instantiates: `from app.gemini_service import GeminiVerificationService; svc = GeminiVerificationService()`

### Phase 2: File Search Store Creation (~60 minutes)

**Objective**: Implement reference document upload with metadata generation and File Search store creation

**Tasks**:

- [ ] Implement `GeminiVerificationService.create_store(case_id: str)` method
- [ ] Implement `generate_metadata(file_path, case_context)` using Gemini Flash Lite
- [ ] Implement `upload_to_store(file_path, store_name, metadata)` with custom metadata
- [ ] Add operation polling logic for indexing completion
- [ ] Implement file cleanup after upload
- [ ] Create POST /upload-references endpoint in main.py
- [ ] Add error handling for Gemini API failures

**Files Modified**:

- `backend/app/gemini_service.py` - Implement File Search methods
- `backend/app/main.py` - Add /upload-references endpoint

**Verification**:

- [ ] API call creates File Search store: `curl -X POST http://localhost:8000/upload-references -F file=@test.pdf`
- [ ] Check store exists: Verify response contains `store_id`
- [ ] Metadata generated with summary, document_type, keywords
- [ ] Operation completes (operation.done == True)
- [ ] Temporary files cleaned up after upload

### Phase 3: Chunk Verification Logic (~75 minutes)

**Objective**: Implement single and batch chunk verification against File Search store

**Tasks**:

- [ ] Implement `verify_chunk(chunk, store_name, case_context)` method
- [ ] Configure File Search tool with store reference
- [ ] Extract citations from grounding_metadata
- [ ] Implement `verify_batch(chunks, store_name, case_context, batch_size=5)` with async
- [ ] Add rate limiting (1-second delay between batches)
- [ ] Implement retry logic with exponential backoff (max 3 retries)
- [ ] Create POST /verify/execute endpoint
- [ ] Add progress tracking for batch processing

**Files Modified**:

- `backend/app/gemini_service.py` - Add verification methods
- `backend/app/main.py` - Add /verify/execute endpoint

**Verification**:

- [ ] Single chunk verification returns structured JSON with verified, confidence_score, source, note, citations
- [ ] Batch processing completes 50 chunks in <2 minutes
- [ ] Citations include title and excerpt from source documents
- [ ] Retry logic handles transient API failures
- [ ] Endpoint returns fully populated DocumentChunk objects

### Phase 4: Output Generation with AI Results (~45 minutes)

**Objective**: Modify output generators to populate verification columns with AI results

**Tasks**:

- [ ] Update `generate_word_document()` to fill Verified ☑, Source, Note columns
- [ ] Add confidence score to verification note (e.g., "Score: 8/10")
- [ ] Update `generate_excel_csv()` to include verification data
- [ ] Implement JSON export format with full verification metadata
- [ ] Add color-coded confidence indicators in Excel (conditional formatting)
- [ ] Update POST /export endpoint to handle verified documents

**Files Modified**:

- `backend/app/output_generator.py` - Populate verification columns
- `backend/app/models.py` - Add OutputFormat.JSON
- `backend/app/main.py` - Update /export endpoint

**Verification**:

- [ ] Word document shows ✅ for verified chunks, ☐ for unverified
- [ ] Verification Source column contains citation references
- [ ] Verification Note column contains AI reasoning + confidence score
- [ ] Excel file includes verification data with readable formatting
- [ ] JSON export includes full citation objects with titles and excerpts

### Phase 5: Frontend Integration (~90 minutes)

**Objective**: Add reference document upload UI and verification workflow to Streamlit

**Tasks**:

- [ ] Add "Step 0.5: Upload Reference Documents" section after document upload
- [ ] Create multi-file uploader (accept PDF/DOCX)
- [ ] Add case context text area (max 500 chars)
- [ ] Implement "Create Reference Library" button with progress indicator
- [ ] Store store_id in session state
- [ ] Add "Step 2.5: Run AI Verification" section after chunking
- [ ] Create "Verify Against References" button
- [ ] Add verification progress bar (chunks processed / total chunks)
- [ ] Display verification summary stats (% verified, avg confidence)
- [ ] Update export UI to show verification data

**Files Modified**:

- `frontend/app.py` - Add reference upload and verification UI sections

**Verification**:

- [ ] User can upload multiple reference documents (ZIP or individual files)
- [ ] Case context saves to session state
- [ ] "Create Reference Library" shows upload progress
- [ ] Store ID displayed after creation
- [ ] "Verify" button triggers verification with progress updates
- [ ] Summary stats show after verification completes
- [ ] Export button downloads verified document with populated columns

### Phase 6: Testing & Polish (~60 minutes)

**Objective**: End-to-end testing, error handling, and documentation

**Tasks**:

- [ ] Test full workflow: upload doc → upload refs → chunk → verify → export
- [ ] Test error cases: missing API key, invalid files, API failures
- [ ] Add user-friendly error messages for Gemini API errors
- [ ] Test with large documents (100+ chunks)
- [ ] Verify cost calculation (log token usage)
- [ ] Add timeout handling for long-running operations
- [ ] Create usage documentation in README
- [ ] Add environment variable setup instructions
- [ ] Test with different chunking modes (paragraph vs sentence)
- [ ] Validate citation extraction accuracy

**Files Modified**:

- `backend/app/gemini_service.py` - Add error messages and logging
- `frontend/app.py` - Add error handling and user feedback
- `README.md` - Add AI verification documentation
- `.env.example` - Document GEMINI_API_KEY setup

**Verification**:

- [ ] Full workflow completes successfully with 50-page document
- [ ] Error messages are clear and actionable
- [ ] Token usage logged for cost tracking
- [ ] Documentation includes setup instructions and API key configuration
- [ ] All verification columns populated correctly in exported document

## Success Metrics

1. **Performance**: 100 chunks verified in <3 minutes
2. **Accuracy**: >80% of chunks receive confidence scores ≥7
3. **Cost**: Average verification cost <$0.50 per 50-page document
4. **Reliability**: 99% success rate for verification requests (with retries)
5. **UX**: Users can complete full workflow in <10 minutes

## Risks & Mitigation

| Risk                           | Impact | Mitigation                                                         |
| ------------------------------ | ------ | ------------------------------------------------------------------ |
| Gemini API rate limits         | High   | Implement batch processing with delays, retry logic                |
| High costs from token usage    | Medium | Use Flash Lite for metadata, Flash for verification; monitor usage |
| Inaccurate verifications       | High   | Include confidence scores; recommend human review for scores <7    |
| File Search indexing delays    | Medium | Show progress indicators; use async polling                        |
| Large file processing timeouts | Medium | Implement chunked uploads; add timeout handling                    |

## Development Guidelines

**Code Patterns**:

- Follow existing service singleton pattern (`gemini_service = GeminiVerificationService()`)
- Use `cprint()` for colored terminal logging
- Maintain Pydantic models for all data structures
- Use async/await for Gemini API calls in batch processing

**Error Handling**:

- Catch `google.genai.errors.*` exceptions
- Return user-friendly error messages via HTTPException
- Log detailed errors with cprint for debugging
- Implement retry logic for transient failures

**Security**:

- Store GEMINI_API_KEY in environment variables only
- Validate all uploaded files (size, type)
- Sanitize case_context input (max length, no scripts)
- Clean up temporary files after processing

**Performance**:

- Use batch_size=5 for concurrent chunk verification
- Cache File Search store references in session
- Implement file cleanup to avoid storage bloat
- Monitor and log token usage for cost optimization

## File Structure Impact

**Created**:

- `.plans/ai-verification-layer.md` - This PRD
- `backend/app/gemini_service.py` - Gemini integration service
- `.env.example` - Environment variable template

**Modified**:

- `backend/requirements.txt` - Add google-genai
- `backend/app/models.py` - Add verification models
- `backend/app/main.py` - Add verification endpoints
- `backend/app/output_generator.py` - Populate verification columns
- `frontend/app.py` - Add reference upload and verification UI
- `README.md` - Add AI verification documentation

## Cost Analysis

**Estimated Cost per 50-page Document**:

- Initial indexing (3 reference docs, ~30K tokens): $0.0045
- Metadata generation (3 docs × 5K tokens): $0.00003
- Verification (100 chunks × 2K tokens each): $0.0042
- **Total**: ~$0.01 per verification

**Monthly Cost (100 verifications/month)**: ~$1.00

Storage and embeddings are FREE with File Search Tool.
