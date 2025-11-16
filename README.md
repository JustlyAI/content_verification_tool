# Content Verification Tool

Convert legal documents (PDF/DOCX) into structured verification checklists with AI-powered automated verification.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.51-red.svg)](https://streamlit.io/)
[![Docling](https://img.shields.io/badge/Docling-2.61.2-orange.svg)](https://github.com/DS4SD/docling)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-AI-4285F4.svg)](https://ai.google.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

<div align="center">
  <img src="gemini-logo.png" alt="Powered by Google Gemini" width="200">
  <p><em>Powered by Google Gemini AI</em></p>
</div>

---

## Features

- **Multi-Format Support**: PDF or DOCX documents (up to 100 MB)
- **Splitting Modes**: Sentence-level or paragraph-level verification
- **Structure Preservation**: Maintains document hierarchy, footnotes, and tables
- **Output Formats**: Word (landscape/portrait), Excel, CSV, or JSON
- **AI Verification**: Automated content verification using Google Gemini AI
  - Upload reference documents for verification
  - AI-powered chunk verification with confidence scores
  - Citation-backed results with source references
  - Batch processing with rate limiting
- **Metadata Tracking**: Page numbers, item numbers, and cross-page overlap detection

### Output Structure

All outputs include columns for verification workflows:

| Page # | Item # | Text | Verified ☑ | Verification Score | Verification Source | Verification Note |
| ------ | ------ | ---- | ---------- | ------------------ | ------------------- | ----------------- |
| 1      | 1      | ...  |            |                    |                     |                   |

---

## Quick Start

### Prerequisites

**Docker (Recommended):**

- Docker 20.10+ and Docker Compose 2.0+
- 4GB+ RAM recommended

**Local Development:**

- Python 3.11+
- 4GB+ RAM recommended

### Docker Setup (Recommended)

```bash
# Start the application
docker-compose up --build

# Access:
# • Streamlit UI: http://localhost:8501
# • API Docs: http://localhost:8000/docs
# • Health Check: http://localhost:8000/health

# Stop services
docker-compose down
```

### Local Development Setup

#### Option 1: UV (Fast & Modern)

[UV](https://github.com/astral-sh/uv) is a fast Python package manager (10-100x faster than pip).

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
# or: brew install uv

# Create virtual environment
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e ".[backend,frontend,test]"

# Download SpaCy model
python -m spacy download en_core_web_sm

# Start services (in separate terminals)
cd backend/app && python main.py
cd frontend && streamlit run app.py
```

#### Option 2: Traditional pip

```bash
# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cd app && python main.py

# Frontend setup (new terminal)
cd frontend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## Usage

### Streamlit UI Workflow

1. **Open** http://localhost:8501
2. **(Optional) AI Reference Corpus**: Expand the panel at top to upload reference documents
3. **Upload** PDF or DOCX file (max 100 MB)
4. **Select splitting mode**:
   - **Paragraph-level**: Groups related sentences, fewer chunks
   - **Sentence-level**: Individual sentence verification, more chunks
5. **(Optional) Run AI Verification**: Verify chunks against reference documents
6. **Choose output format**: Word (landscape/portrait), Excel, CSV, or JSON
7. **Generate & Download** verification document

---

## AI Verification Setup

### 1. Get Gemini API Key

Visit [Google AI Studio](https://aistudio.google.com/apikey) and create an API key.

### 2. Configure Environment

```bash
# Create .env file
cp .env.example .env

# Add your API key
echo "GEMINI_API_KEY=your_api_key_here" >> .env
```

### 3. Restart Services

```bash
docker-compose down
docker-compose up --build
```

### AI Verification Features

- **Reference Corpus Management**: Upload and manage reference documents via File Search stores
- **Automated Verification**: AI verifies chunks using `gemini-2.5-flash` with semantic search
- **Metadata Generation**: AI extracts document summaries and keywords using `gemini-2.5-flash-lite`
- **Confidence Scores**: 1-10 scale for verification reliability
- **Source Citations**: Grounding metadata with exact references and excerpts
- **Batch Processing**: Rate-limited concurrent verification with retry logic
- **Cost Efficient**: ~$0.01 per 50-page document, free File Search storage

---

## API Usage

### Key Endpoints

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

**AI Verification**

```bash
# Upload references
curl -X POST "http://localhost:8000/api/verify/upload-references" \
  -F "case_context=Contract verification case" \
  -F "files=@reference1.pdf"

# Execute verification
curl -X POST "http://localhost:8000/api/verify/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "abc123...",
    "store_id": "corpora/verification_case_abc123",
    "case_context": "Contract verification",
    "chunking_mode": "paragraph"
  }'
```

**Formats**: `word_landscape`, `word_portrait`, `excel`, `csv`, `json`

**Full Documentation**: http://localhost:8000/docs

---

## Architecture

```
┌─────────────────────────────────┐
│    Streamlit Frontend (8501)    │
│  • File upload                  │
│  • Corpus management            │
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
│                                 │
│  AI Verification:               │
│  • CorpusManager                │
│    - File Search stores         │
│    - Metadata (flash-lite)      │
│  • GeminiVerifier               │
│    - Verification (flash)       │
│    - Grounding citations        │
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

## Project Structure

```
content_verification_tool/
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI application
│   │   ├── models.py              # Pydantic models
│   │   ├── corpus/                # Corpus management
│   │   │   └── corpus_manager.py
│   │   ├── verification/          # AI verification
│   │   │   └── gemini_verifier.py
│   │   └── processing/            # Document processing
│   │       ├── cache.py
│   │       ├── document_processor.py
│   │       ├── chunker.py
│   │       └── output_generator.py
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── config.py              # Configuration
│   │   ├── state.py               # Session state
│   │   ├── api_client.py          # Backend client
│   │   ├── corpus.py              # Corpus management
│   │   └── ui_components.py       # UI components
│   ├── app.py                      # Main Streamlit app
│   └── requirements.txt
├── pyproject.toml                  # UV/pip package config
├── .env.example                    # Environment template
├── docker-compose.yml              # Docker orchestration
└── README.md
```

---

## Troubleshooting

### Backend Issues

**Port 8000 already in use**

```bash
# Mac/Linux
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
```

**Module not found**

```bash
pip install -r backend/requirements.txt
python -m spacy download en_core_web_sm
```

**Docling conversion fails**

- Check file is not corrupted
- Verify file size (max 100 MB)
- Check backend logs: `docker-compose logs -f backend`

### Frontend Issues

**Backend API not available**

```bash
# Check backend health
curl http://localhost:8000/health

# Verify environment
echo $BACKEND_URL  # Should be http://localhost:8000
```

**Upload fails**

- Verify file format (PDF or DOCX only)
- Check file size (< 100 MB)
- Review backend logs

### Docker Issues

**Container won't start**

```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild
docker-compose down -v
docker-compose up --build
```

**Out of memory**

- Increase Docker memory in Docker Desktop settings
- Minimum: 4GB, Recommended: 8GB

### Performance

**Slow processing**

- Large documents (50+ pages) may take 1-2 minutes
- Sentence mode is slower than paragraph mode
- First run downloads SpaCy model (one-time)

**Clear cache**

```bash
# Via API
curl -X DELETE http://localhost:8000/cache/clear

# Manual
rm -rf /tmp/document_cache/*
```

---

## Development

### Running Tests

```bash
# UV
pytest
pytest --cov=backend/app --cov=frontend/app

# Traditional
python -m pytest tests/
```

### Cache Management

Cache location: `/tmp/document_cache`

```bash
# Clear cache
docker-compose exec backend rm -rf /tmp/document_cache/*
```

### Logs

```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Save to file
docker-compose logs > application.log
```

---

## Tech Stack

**Backend**: FastAPI • Docling • LangChain • python-docx • pandas • spaCy • Google Gemini API

**Frontend**: Streamlit

**Infrastructure**: Docker • Docker Compose • UV/pip

**AI Models**:

- `gemini-2.5-flash` - Chunk verification
- `gemini-2.5-flash-lite` - Metadata generation
- File Search (RAG) - Reference corpus with automatic embeddings

---

## Future Improvements

- Better semantic chunking of multi-sentence 'clauses'.
- Structured outputs for verification results (awaiting availability with File Search)

---

## Cost Estimation (AI Verification)

Typical costs using Gemini models:

- Metadata generation (`gemini-2.5-flash-lite`): ~$0.00003 per document
- Verification (`gemini-2.5-flash`): ~$0.0042 per 100 chunks
- **Total for 50-page document**: ~$0.01

**File Search (RAG):**

- Storage: FREE
- Query-time embeddings: FREE
- Initial indexing: $0.15 per 1M tokens (one-time)

---

## Support

1. Check troubleshooting guide above
2. Review backend logs: `docker-compose logs backend`
3. Test with sample documents
4. Check API docs: http://localhost:8000/docs
5. Review project plan: `CLAUDE.md`

---

**Version**: 1.2.0
**Last Updated**: 2025-11-16
