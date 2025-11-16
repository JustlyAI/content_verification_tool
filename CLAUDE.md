## General Guidelines

- reading and writing files should always implement encoding="utf-8"
- add informative print statements every step of the way to debug and see what the agent is doing and thinking
- have termcolor printing with cprint very step of the way to inform the user
- major variables should be all caps Variables on top of the script and not user input taking unless otherwise specified
- if there are models in the script do not change them as they now exist
- use pydantic
- do not delete requirements.txt unless you are sure it is not needed
- lets implement every project with seperation of concerns in mind
- always provide detailed instructions to the model considering everything carefully
- do not overcomplicate things. you should tend to simplify wherever possible
- do not mock codefiles if you suspect that they might already exist - rather, ask for the codefiles you need
- do not rewrite prompts or data classes unless specifically requested

# Document Verification Assistant - Project Plan

## Project Overview

A Streamlit web application that converts legal documents (PDF/DOCX) into structured verification checklists, enabling systematic verification of each sentence or paragraph against source materials.

---

## Technical Stack

### Frontend
- **Streamlit** - Web interface

### Backend
- **FastAPI** - REST API service (separate from Streamlit)
- **Python** - Core processing logic
- **Pydantic** - Data validation

### Document Processing
- **Docling** - PDF/DOCX conversion and parsing
- **HierarchicalChunker** (Docling) - Base document structure chunking
- **LangChain RecursiveCharacterTextSplitter** - Paragraph-level splitting
- **LangChain SpacyTextSplitter (sentencizer)** - Sentence-level splitting

### Output Generation
- **python-docx** - Word document generation
- **pandas + openpyxl** - Excel/CSV generation

### Deployment
- **Docker + Docker Compose** - Containerization of entire application

---

## Application Workflow

```
1. Upload Document (PDF/DOCX)
   ↓
2. Convert with Docling → DoclingDocument
   ↓
3. User Selection: Chunking Mode
   - Sentence-level chunking
   - Paragraph-level chunking
   ↓
4. Process & Extract Metadata
   - Page number
   - Item number (per page, resets each page)
   - Text content
   - Overlap flag (if item spans from previous page)
   ↓
5. User Selection: Output Format
   - Word (Landscape)
   - Word (Portrait)
   - CSV/Excel
   ↓
6. Generate Verification Table
   Columns:
   [Page # | Item # | Text | Verified ☑ | Verification Source | Verification Note]
```

---

## Detailed Processing Logic

### 1. Document Upload & Conversion
- **Supported formats**: PDF, DOCX
- **File size limit**: 100 MB maximum
- **Caching strategy**: Cache Docling conversion results to avoid re-processing same document with different chunking settings
- **OCR handling**: Basic OCR (no Tesseract required)

### 2. Document Parsing with Docling
**Configuration requirements:**
- Parse tables and preserve table structure
- Extract and include footnotes
- Footnotes should:
  - Follow body text from their source page
  - Be chunkable on sentence or paragraph basis
  - Maintain association with source page

**Metadata extraction:**
- Rely on Docling's `chunk.meta.doc_items` for source tracking
- Use provenance (`prov`) data to detect text spans across pages

### 3. Chunking Strategy

#### Base Processing
1. **HierarchicalChunker (Docling)**: 
   - Preserves document structure (headings, paragraphs, sections)
   - Maintains metadata including page numbers
   - Handles footnotes as separate items

#### Paragraph Mode
2. **LangChain RecursiveCharacterTextSplitter**:
   - Applied after HierarchicalChunker
   - Splits content at paragraph boundaries
   - Preserves structural integrity

#### Sentence Mode
3. **LangChain SpacyTextSplitter (sentencizer)**:
   - Applied after HierarchicalChunker
   - Splits content into individual sentences
   - Uses spaCy's sentence boundary detection

### 4. Metadata Tracking

**For each chunk, track:**

| Field | Description | Logic |
|-------|-------------|-------|
| `page_number` | Page where item appears | Extracted from Docling metadata |
| `item_number` | Position on page | Resets to 1 on each new page |
| `text` | Chunk content | Sentence or paragraph text |
| `is_overlap` | Boolean flag | True if item continues from previous page |

**Item Numbering Rules:**
- Start counting from **first full paragraph** on each page
- If first item on page is partial (continues from previous), mark `is_overlap=True`
- Partial/continuing text is **pinned to the start page** and counted there
- Item numbering resets to 1 on each new page
- Footnotes are numbered sequentially after body text on same page

**Page Attribution for Spans:**
- If sentence/paragraph spans multiple pages → attribute to **start page**

**Partial Text Detection:**
- Use Docling's **provenance (prov) data** to identify items spanning pages
- Items with prov data indicating multi-page span are marked with `is_overlap=True`

### 5. Output Generation

#### Word Documents (Landscape/Portrait)
**Table structure:**

| Column | Width | Content |
|--------|-------|---------|
| Page # | 10% | Integer page number |
| Item # | 10% | Integer item number (resets per page) |
| Text | 40% | Sentence or paragraph text |
| Verified ☑ | 10% | Checkbox symbol |
| Verification Source | 15% | Blank cell for user input |
| Verification Note | 15% | Blank cell for user input |

**Formatting:**
- Column widths proportional to page orientation
- Table borders enabled
- Header row with bold formatting
- Landscape: Wider columns for Text and Notes
- Portrait: Compressed layout

#### CSV/Excel
**Structure:**
- Same 6 columns as Word output
- Header row included
- No special formatting (keep basic)
- No data validation or filters
- Compatible with Excel and Google Sheets

---

## Architecture

### Component Separation

```
┌─────────────────────────────────────────────────┐
│              Streamlit Frontend                 │
│  - File upload interface                        │
│  - Chunking mode selection (radio buttons)      │
│  - Output format selection (dropdown)           │
│  - Download button for results                  │
└─────────────────┬───────────────────────────────┘
                  │ HTTP/REST
                  ↓
┌─────────────────────────────────────────────────┐
│              FastAPI Backend                    │
│  - /upload endpoint (file processing)           │
│  - /chunk endpoint (with mode parameter)        │
│  - /export endpoint (format selection)          │
│  - Docling conversion & caching                 │
│  - Metadata extraction & tracking               │
│                                                  │
│  Modular Structure:                             │
│  • corpus/ - Reference document management      │
│  • verification/ - AI chunk verification        │
│  • processing/ - Document conversion & chunking │
└─────────────────────────────────────────────────┘
```

**Why separate services:**
- **Scalability**: Backend can handle heavy processing independently
- **Caching**: FastAPI can maintain document cache across sessions
- **Testability**: API can be tested independently of UI
- **Flexibility**: Can add other frontends (CLI, web app) later
- **Modularity**: Clear separation of corpus, verification, and processing concerns

### Caching Strategy
- **Cache key**: Hash of uploaded file content
- **Cache contents**: 
  - DoclingDocument object
  - Basic metadata (page count, file info)
- **Cache invalidation**: Time-based (e.g., 1 hour) or manual clear
- **Storage**: In-memory (Redis) or file-based cache

---

## User Experience Flow

### Step 1: Upload
- Drag-and-drop or file picker
- Immediate validation (format, size)
- Loading indicator during Docling conversion
- Error messages for invalid files

### Step 2: Chunking Mode Selection
```
○ Paragraph-level chunking
○ Sentence-level chunking
```
- Radio buttons (single selection)
- Brief description of each mode
- Default: Paragraph-level

### Step 3: Output Format Selection
```
Select output format: [Dropdown ▼]
- Word (Landscape)
- Word (Portrait)
- Excel/CSV
```
- Dropdown menu
- Preview of table structure (static image/text)

### Step 4: Generate & Download
- "Generate Verification Document" button
- Progress indicator during generation
- Automatic download when ready
- Option to regenerate with different settings

**No preview step** - direct to download after generation

---

## Implementation Phases

### Phase 1: Core Processing Pipeline
1. FastAPI backend setup
2. Docling integration (PDF/DOCX → DoclingDocument)
3. HierarchicalChunker implementation
4. Basic metadata extraction

### Phase 2: Chunking Modes
1. LangChain integration
2. Paragraph mode (RecursiveCharacterTextSplitter)
3. Sentence mode (SpacyTextSplitter)
4. Metadata tracking and overlap detection

### Phase 3: Output Generation
1. Word document generation (python-docx)
   - Landscape layout
   - Portrait layout
2. Excel/CSV generation (pandas + openpyxl)
3. Table formatting logic

### Phase 4: Frontend & Integration
1. Streamlit UI components
2. API client for backend communication
3. File upload handling
4. User selection forms
5. Download mechanism

### Phase 5: Caching & Optimization
1. Document conversion caching
2. Performance optimization
3. Error handling and validation

### Phase 6: Containerization
1. Dockerfile for FastAPI backend
2. Dockerfile for Streamlit frontend
3. docker-compose.yml for orchestration
4. Environment configuration
5. Volume management for cache

---

## File Size & Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max file size | 100 MB | Balance processing time vs. utility |
| Max pages | No explicit limit | Controlled by file size |
| Supported formats | PDF, DOCX | Core legal document formats |
| Output formats | Word (2), Excel/CSV | Maximum compatibility |

---

## Error Handling

### File Upload Errors
- Invalid format → Clear message with supported formats
- File too large → Message with size limit
- Corrupted file → Docling conversion error handling

### Processing Errors
- Docling conversion failure → Fallback message, suggest manual review
- Chunking errors → Log error, return partial results if possible
- Memory issues → Implement streaming for large documents

### Output Generation Errors
- Word generation failure → Try alternative library or CSV fallback
- Excel errors → Fallback to basic CSV

---

## Testing Strategy

### Unit Tests
- Docling conversion accuracy
- Metadata extraction correctness
- Chunking mode outputs
- Overlap detection logic
- Page number tracking
- Item numbering resets

### Integration Tests
- FastAPI endpoints
- Streamlit → FastAPI communication
- Full workflow (upload → chunk → export)
- Caching behavior

### End-to-End Tests
- Upload various document types
- Test all chunking modes
- Verify all output formats
- Validate table structure and content

---

## Future Enhancements (Out of Scope for V1)

- Batch document processing
- Preview before export
- Custom column configuration
- Cloud storage integration (Google Drive, S3)
- Real-time collaboration features
- Advanced OCR (Tesseract) option
- Citation/source linking
- Multi-language support

---

## Open Questions

**None remaining** - All clarifications addressed above.

---

## Next Steps

1. **Confirm this plan** - Review and approve before coding begins
2. **Set up project structure** - Initialize repos, directory layout
3. **Begin Phase 1** - FastAPI backend + Docling integration
4. **Iterative development** - Build and test each phase sequentially
5. **Docker containerization** - Final phase before deployment

---

## Project Timeline Estimate

- **Phase 1-2**: 2-3 days (Core processing + chunking)
- **Phase 3**: 1-2 days (Output generation)
- **Phase 4**: 2-3 days (Frontend + integration)
- **Phase 5**: 1 day (Caching & optimization)
- **Phase 6**: 1 day (Docker setup)

**Total estimated time**: 7-10 days for V1 completion

---

## Technology Versions (Recommended)

```
Python: 3.11+
FastAPI: 0.104+
Streamlit: 1.28+
Docling: latest
LangChain: 0.1.0+
python-docx: 1.1.0+
pandas: 2.1+
openpyxl: 3.1+
spacy: 3.7+
pydantic: 2.5+
```
