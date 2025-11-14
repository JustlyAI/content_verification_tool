# Content Verification Tool

Convert legal documents (PDF/DOCX) into structured verification checklists for systematic content verification.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.51-red.svg)](https://streamlit.io/)
[![Docling](https://img.shields.io/badge/Docling-2.61.2-orange.svg)](https://github.com/DS4SD/docling)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

---

## Features

- **Multi-Format Support**: PDF or DOCX documents (up to 100 MB)
- **Chunking Modes**: Sentence-level or paragraph-level verification
- **Structure Preservation**: Maintains document hierarchy, footnotes, and tables
- **Output Formats**: Word (landscape/portrait), Excel, CSV, or JSON
- **Metadata Tracking**: Page numbers, item numbers, and cross-page overlap detection
- **🆕 AI Verification**: Automated content verification using Google Gemini AI
  - Upload reference documents for verification
  - AI-powered chunk verification with confidence scores
  - Citation-backed results with source references
  - Batch processing with rate limiting

### Output Structure

All outputs include 6 columns for verification workflows:

| Page # | Item # | Text | Verified ☑ | Verification Score | Verification Source | Verification Note |
| ------ | ------ | ---- | ---------- | ------------------ | ------------------- | ----------------- |
| 1      | 1      | ...  |            |                    |                     |

---

## Quick Start

### Prerequisites

- Docker and Docker Compose (recommended) **OR** Python 3.11+
- 4GB+ RAM recommended

### Docker (Recommended)

```bash
# Start the application
docker-compose up --build

# Access:
# • Streamlit UI: http://localhost:8501
# • API Docs: http://localhost:8000/docs
# • Health Check: http://localhost:8000/health
```

### Local Development

```bash
# Make scripts executable
chmod +x start_*.sh

# Start both services
./start_all.sh

# OR start separately:
# Terminal 1: ./start_backend.sh
# Terminal 2: ./start_frontend.sh
```

See [SETUP.md](SETUP.md) for detailed instructions.

---

## Usage

1. **Open** `http://localhost:8501`
2. **(Optional) Create AI Reference Corpus**: Expand the "AI Reference Corpus" panel at the top to upload reference documents for automated verification
3. **Upload** PDF or DOCX file (max 100 MB)
4. **Select chunking mode**:
   - Paragraph-level: Groups related sentences
   - Sentence-level: Individual sentence verification
5. **(Optional) Run AI Verification**: If corpus is active, verify chunks against reference documents
6. **Choose output format**: Word (landscape/portrait), Excel, CSV, or JSON
7. **Generate & Download** verification document

---

## API Usage

### Endpoints

**Upload Document**

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf"
```

**Export Document**

```bash
curl -X POST "http://localhost:8000/export" \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "abc123...",
    "chunking_mode": "sentence",
    "output_format": "word_landscape"
  }'
```

**Download File**

```bash
curl -X GET "http://localhost:8000/download/abc123..." \
  --output verification.docx
```

**Formats**: `word_landscape`, `word_portrait`, `excel`, `csv`, `json`

**Documentation**: http://localhost:8000/docs

---

## AI Verification (NEW)

Automatically verify document chunks against reference documents using Google Gemini AI.

### Streamlit UI Workflow

The Streamlit UI features a dedicated **AI Reference Corpus** panel at the top of the page:

1. **Expand the panel** to create or manage your reference corpus
2. **Upload reference documents** (PDF/DOCX) with case context
3. **View corpus status** - panel shows "✅ Active" or "⚠️ Not Configured"
4. **Clear corpus** when done to start fresh

The corpus panel is always accessible and independent of the main verification workflow.

### Setup

1. **Get Gemini API Key**:

   - Visit https://aistudio.google.com/apikey
   - Create a new API key

2. **Configure Environment**:

   ```bash
   # Create .env file in the root directory
   cp .env.example .env

   # Add your API key
   echo "GEMINI_API_KEY=your_api_key_here" >> .env
   ```

3. **Restart Services** (if running):
   ```bash
   docker-compose down
   docker-compose up --build
   ```

### AI Verification Workflow

1. **Upload Reference Documents**

   ```bash
   curl -X POST "http://localhost:8000/api/verify/upload-references" \
     -F "case_context=This is a contract verification case" \
     -F "files=@reference1.pdf" \
     -F "files=@reference2.pdf"
   ```

   Response:

   ```json
   {
     "store_id": "corpora/verification_case_abc123",
     "store_name": "verification_case_abc123",
     "documents_uploaded": 2,
     "metadata": [...]
   }
   ```

2. **Upload Document to Verify**

   ```bash
   curl -X POST "http://localhost:8000/upload" \
     -F "file=@document_to_verify.pdf"
   ```

3. **Execute AI Verification**

   ```bash
   curl -X POST "http://localhost:8000/api/verify/execute" \
     -H "Content-Type: application/json" \
     -d '{
       "document_id": "abc123...",
       "store_id": "corpora/verification_case_abc123",
       "case_context": "Contract verification case",
       "chunking_mode": "paragraph"
     }'
   ```

   Response:

   ```json
   {
     "document_id": "abc123...",
     "verified_chunks": [...],
     "total_verified": 45,
     "total_chunks": 50,
     "processing_time_seconds": 120.5,
     "store_id": "corpora/verification_case_abc123"
   }
   ```

4. **Export with Verification Results**
   ```bash
   curl -X POST "http://localhost:8000/export" \
     -H "Content-Type: application/json" \
     -d '{
       "document_id": "abc123...",
       "chunking_mode": "paragraph",
       "output_format": "json"
     }'
   ```

### Verification Output

AI-verified chunks include:

- **verified**: Boolean indicating if content was found in references
- **verification_score**: Confidence level (1-10)
- **verification_source**: Citation with document name and location
- **verification_note**: AI reasoning and explanation
- **citations**: Detailed citation objects with excerpts

Example verified chunk in JSON export:

```json
{
  "page_number": 1,
  "item_number": "3",
  "text": "The contract term is 12 months.",
  "verified": true,
  "verification_score": 9,
  "verification_source": "Contract.pdf, Section 2.1",
  "verification_note": "Exact match found in contract terms section",
  "citations": [
    {
      "title": "Contract.pdf",
      "excerpt": "The contract term shall be twelve (12) months..."
    }
  ]
}
```

### Cost Estimation

Typical costs using Gemini 2.0 Flash:

- **Metadata generation**: ~$0.00003 per document
- **Verification**: ~$0.0042 per 100 chunks
- **Total for 50-page document**: ~$0.01

Storage and embeddings are **FREE** with Gemini File Search.

### Features

✅ **Automated Verification**: AI checks each chunk against reference documents
✅ **Confidence Scores**: 1-10 scale for reliability assessment
✅ **Source Citations**: Exact references with document names and excerpts
✅ **Batch Processing**: Handles hundreds of chunks efficiently
✅ **Rate Limiting**: Built-in delays to respect API limits
✅ **Export Integration**: Pre-populated verification columns in all formats

---

## Architecture

```
┌─────────────────────────────────┐
│    Streamlit Frontend (8501)    │
│  • File upload                  │
│  • Mode selection               │
│  • Download handling            │
└────────────┬────────────────────┘
             │ REST API
             ↓
┌─────────────────────────────────┐
│    FastAPI Backend (8000)       │
│  • Docling conversion           │
│  • Chunking pipeline            │
│  • Output generation            │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│    Processing Pipeline          │
│  Docling → HybridChunker →      │
│    ├─ Paragraph (LangChain)     │
│    └─ Sentence (SpaCy)          │
└─────────────────────────────────┘
```

---

## Development

### Manual Setup

**Backend:**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cd app && python main.py
```

**Frontend:**

```bash
cd frontend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Project Structure

```
content_verification_tool/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # Pydantic models
│   │   ├── gemini_service.py    # AI verification service
│   │   ├── document_processor.py
│   │   ├── chunker.py
│   │   ├── output_generator.py
│   │   └── cache.py
│   └── requirements.txt
├── frontend/
│   ├── app/                     # Modular application components
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration and constants
│   │   ├── state.py            # Session state management
│   │   ├── api_client.py       # Backend API client
│   │   ├── corpus.py           # Corpus management UI
│   │   └── ui_components.py    # Reusable UI components
│   ├── app.py                   # Main Streamlit application
│   └── requirements.txt
├── .env.example                 # Environment variables template
├── docker-compose.yml
├── start_all.sh
└── SETUP.md
```

---

## Troubleshooting

**Backend not available**: Ensure Docker containers are running with `docker-compose ps`

**File too large**: Maximum file size is 100 MB

**Slow processing**: Ensure Docker has 4GB+ RAM allocated

**View logs**: `docker-compose logs -f backend`

---

## Tech Stack

**Backend**: FastAPI • Docling • LangChain • python-docx • pandas • spaCy • Google Gemini AI

**Frontend**: Streamlit

**Infrastructure**: Docker • Docker Compose
