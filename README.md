# Content Verification Tool

A professional document verification tool that converts legal briefs, contracts, and other documents into structured verification checklists. Built for legal professionals who need to systematically verify document content against source materials.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.51+-red.svg)](https://streamlit.io/)
[![Docling](https://img.shields.io/badge/Docling-2.61.2-orange.svg)](https://github.com/DS4SD/docling)
[![LangChain](https://img.shields.io/badge/LangChain-1.0.5-brightgreen.svg)](https://www.langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

---

## Features

### 🎯 Core Capabilities

- **Multi-Format Support**: Upload PDF or DOCX documents (up to 100 MB)
- **Intelligent Chunking**: Choose between sentence-level or paragraph-level verification
- **Structure Preservation**: Maintains document hierarchy, footnotes, and tables
- **Flexible Output**: Export to Word (landscape/portrait) or Excel/CSV
- **Smart Metadata**: Tracks page numbers, item numbers, and cross-page overlaps

### 🔬 Advanced Processing

- **Docling Integration**: State-of-the-art document parsing with OCR support
- **Page-Aware Numbering**: Item numbers reset on each page for easy reference
- **Overlap Detection**: Identifies text spanning multiple pages
- **Footnote Handling**: Includes and chunks footnotes alongside body text
- **Caching**: Avoid re-processing with intelligent document caching

### 📊 Output Formats

All outputs include 6 columns optimized for verification workflows:

| Page # | Item # | Text | Verified ☑ | Verification Source | Verification Note |
| ------ | ------ | ---- | ---------- | ------------------- | ----------------- |
| 1      | 1      | ...  |            |                     |                   |

---

## Quick Start

### Prerequisites

- Docker and Docker Compose installed (recommended) **OR** Python 3.11+
- 4GB+ RAM recommended
- Modern web browser

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd content_verification_tool

# Start the application with Docker Compose
docker-compose up --build

# Access the application
# Streamlit UI: http://localhost:8501
# FastAPI Docs: http://localhost:8000/docs
# Health Check: http://localhost:8000/health
```

That's it! The application is now running.

### Option 2: Local Development

```bash
# Clone the repository
git clone <repository-url>
cd content_verification_tool

# Make scripts executable
chmod +x start_*.sh

# Start both services (uses tmux or separate terminals)
./start_all.sh

# OR start services separately:
# Terminal 1: ./start_backend.sh
# Terminal 2: ./start_frontend.sh
```

For detailed setup instructions, see [SETUP.md](SETUP.md).

---

## Usage

### Web Interface (Recommended)

1. **Open the Streamlit UI** at `http://localhost:8501`

2. **Upload Your Document**

   - Drag and drop your PDF or DOCX file
   - Or use the file picker
   - Maximum file size: 100 MB

3. **Select Chunking Mode**

   - **Paragraph-level**: Groups related sentences together (recommended for contracts)
   - **Sentence-level**: Individual sentence verification (recommended for briefs with citations)

4. **Choose Output Format**

   - **Word (Landscape)**: Best for detailed review on desktop
   - **Word (Portrait)**: Standard printable format
   - **Excel/CSV**: For data analysis or import into other tools

5. **Generate & Download**
   - Click "Generate Verification Document"
   - Your formatted document downloads automatically

### Example Workflow

```
Upload: legal_brief.pdf (45 pages)
  ↓
Select: Sentence-level chunking
  ↓
Choose: Word (Landscape)
  ↓
Result: legal_brief_verification.docx
  → 342 sentences
  → 45 pages tracked
  → 6 overlap items flagged
```

---

## API Usage

The FastAPI backend can be used independently for programmatic access.

### Upload Document

```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

**Response:**

```json
{
  "document_id": "abc123...",
  "filename": "document.pdf",
  "page_count": 25,
  "file_size": 26214400,
  "message": "Document uploaded and converted successfully (25 pages)"
}
```

### Chunk Document

```bash
curl -X POST "http://localhost:8000/chunk" \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "abc123...",
    "chunking_mode": "sentence"
  }'
```

**Response:**

```json
{
  "document_id": "abc123...",
  "chunking_mode": "sentence",
  "chunks": [
    {
      "page_number": 1,
      "item_number": 1,
      "text": "This is the first sentence.",
      "is_overlap": false
    }
  ],
  "total_chunks": 342,
  "message": "Document chunked successfully (342 chunks in sentence mode)"
}
```

### Export Document

```bash
curl -X POST "http://localhost:8000/export" \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "abc123...",
    "chunking_mode": "sentence",
    "output_format": "word_landscape"
  }'
```

**Response:**

```json
{
  "document_id": "abc123...",
  "output_format": "word_landscape",
  "filename": "document_verification_20251111_123456.docx",
  "message": "Document exported successfully as word_landscape"
}
```

### Download File

```bash
curl -X GET "http://localhost:8000/download/abc123..." \
  --output verification.docx
```

**Supported formats:**

- `word_landscape`
- `word_portrait`
- `excel`
- `csv`

### API Documentation

Full interactive API documentation available at:

- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## Architecture

```
┌─────────────────────────────────────────┐
│        Streamlit Frontend               │
│        (Port 8501)                      │
│  • File upload interface                │
│  • Mode selection                       │
│  • Download handling                    │
└───────────────┬─────────────────────────┘
                │ REST API
                ↓
┌─────────────────────────────────────────┐
│        FastAPI Backend                  │
│        (Port 8000)                      │
│  • Document conversion (Docling)        │
│  • Chunking pipeline                    │
│  • Metadata extraction                  │
│  • Output generation                    │
│  • Caching layer                        │
└───────────────┬─────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────┐
│        Processing Pipeline              │
│                                         │
│  Docling → HierarchicalChunker →       │
│    ├─ RecursiveCharacterTextSplitter   │
│    └─ SpacyTextSplitter (sentencizer)  │
└─────────────────────────────────────────┘
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# FastAPI Backend
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
CACHE_TTL=3600  # Cache timeout in seconds
MAX_FILE_SIZE_MB=100

# Streamlit Frontend
STREAMLIT_SERVER_PORT=8501
BACKEND_URL=http://backend:8000

# Docling
DOCLING_OCR_ENABLED=true
DOCLING_TABLE_PARSING=true

# LangChain
LANGCHAIN_CHUNK_SIZE=1000
LANGCHAIN_CHUNK_OVERLAP=200
```

### Advanced Configuration

**Custom chunking parameters** (backend/config.py):

```python
# Paragraph mode settings
PARAGRAPH_CHUNK_SIZE = 1000
PARAGRAPH_CHUNK_OVERLAP = 200

# Sentence mode settings
SENTENCE_MIN_LENGTH = 10  # Minimum chars for a sentence
```

**Output formatting** (backend/output/styles.py):

```python
# Word document styling
TABLE_BORDER_STYLE = "single"
HEADER_FONT_SIZE = 12
BODY_FONT_SIZE = 10
```

---

## Development

### Local Development Setup

#### Quick Start with Scripts

```bash
# Clone repository
git clone <repository-url>
cd content_verification_tool

# Make scripts executable
chmod +x start_*.sh

# Option 1: Start both services together (recommended)
./start_all.sh

# Option 2: Start services separately
# Terminal 1:
./start_backend.sh

# Terminal 2:
./start_frontend.sh
```

The scripts automatically:

- Create virtual environments
- Install dependencies
- Download SpaCy models
- Start the services

#### Manual Setup

```bash
# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cd app
python main.py

# Frontend setup (new terminal)
cd frontend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

For detailed setup instructions and troubleshooting, see [SETUP.md](SETUP.md).

### Project Structure

```
content_verification_tool/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application
│   │   ├── models.py               # Pydantic data models
│   │   ├── document_processor.py   # Docling integration
│   │   ├── chunker.py              # Chunking strategies
│   │   ├── output_generator.py     # Word/Excel/CSV generation
│   │   └── cache.py                # Document caching
│   ├── Dockerfile
│   ├── .dockerignore
│   └── requirements.txt
├── frontend/
│   ├── app.py                      # Streamlit application
│   ├── Dockerfile
│   ├── .dockerignore
│   └── requirements.txt
├── docker-compose.yml               # Multi-container orchestration
├── start_backend.sh                 # Backend startup script
├── start_frontend.sh                # Frontend startup script
├── start_all.sh                     # Combined startup script
├── .gitignore
├── CLAUDE.md                        # Project plan and specifications
├── SETUP.md                         # Detailed setup guide
└── README.md                        # This file
```

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=.

# Frontend tests
cd frontend
pytest tests/ -v

# Integration tests
pytest tests/integration/ -v
```

### Code Quality

```bash
# Format code
black backend/ frontend/
isort backend/ frontend/

# Lint
flake8 backend/ frontend/
pylint backend/ frontend/

# Type checking
mypy backend/
```

---

## Docker Deployment

### Production Build

```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "version": "1.0.0"}
```

### Scaling

```bash
# Scale backend workers
docker-compose up -d --scale backend=3

# Monitor performance
docker stats
```

---

## Troubleshooting

### Common Issues

**Issue**: "File too large" error

```
Solution: Check MAX_FILE_SIZE_MB in .env file
Default: 100 MB
```

**Issue**: Docling conversion fails

```
Solution:
1. Check if PDF is password-protected
2. Verify OCR settings in config
3. Try re-uploading the file
```

**Issue**: Slow processing

```
Solution:
1. Ensure Docker has adequate memory (4GB+)
2. Check cache settings (CACHE_TTL)
3. Consider sentence mode for very large documents
```

**Issue**: Missing footnotes in output

```
Solution:
1. Verify Docling parsed footnotes (check logs)
2. Ensure DOCLING_FOOTNOTE_PARSING=true in .env
```

### Debug Mode

Enable debug logging:

```env
# .env
LOG_LEVEL=DEBUG
STREAMLIT_LOG_LEVEL=debug
```

View detailed logs:

```bash
docker-compose logs -f --tail=100 backend
```

---

## Tech Stack

### Backend

- **FastAPI** - High-performance API framework
- **Docling** - Document parsing and conversion
- **LangChain** - Text splitting and chunking
- **python-docx** - Word document generation
- **pandas + openpyxl** - Excel/CSV generation
- **Pydantic** - Data validation
- **spaCy** - Sentence tokenization

### Frontend

- **Streamlit** - Interactive web UI
- **Requests** - API client

### Infrastructure

- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Redis** (optional) - Caching backend

---

## Acknowledgments

- **Docling** - For excellent document parsing capabilities
- **LangChain** - For flexible text processing tools
- **FastAPI** - For the outstanding API framework
- **Streamlit** - For making web UIs simple
