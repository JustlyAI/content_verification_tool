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
- **Output Formats**: Word (landscape/portrait), Excel, or CSV
- **Metadata Tracking**: Page numbers, item numbers, and cross-page overlap detection

### Output Structure

All outputs include 6 columns for verification workflows:

| Page # | Item # | Text | Verified ☑ | Verification Source | Verification Note |
| ------ | ------ | ---- | ---------- | ------------------- | ----------------- |
| 1      | 1      | ...  |            |                     |                   |

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
2. **Upload** PDF or DOCX file (max 100 MB)
3. **Select chunking mode**:
   - Paragraph-level: Groups related sentences
   - Sentence-level: Individual sentence verification
4. **Choose output format**: Word (landscape/portrait), Excel, or CSV
5. **Generate & Download** verification document

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

**Formats**: `word_landscape`, `word_portrait`, `excel`, `csv`

**Documentation**: http://localhost:8000/docs

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
│   │   ├── document_processor.py
│   │   ├── chunker.py
│   │   ├── output_generator.py
│   │   └── cache.py
│   └── requirements.txt
├── frontend/
│   ├── app.py                   # Streamlit UI
│   └── requirements.txt
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

**Backend**: FastAPI • Docling • LangChain • python-docx • pandas • spaCy

**Frontend**: Streamlit

**Infrastructure**: Docker • Docker Compose
