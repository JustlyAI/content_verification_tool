# Content Verification Tool - Setup Guide

This guide provides detailed instructions for setting up and running the Content Verification Tool.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start with Docker](#quick-start-with-docker)
- [Local Development Setup](#local-development-setup)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Docker Installation (Recommended)

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher

[Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Local Development

- **Python**: Version 3.11 or higher
- **pip**: Latest version
- **System RAM**: Minimum 4GB (8GB recommended for large documents)
- **Disk Space**: At least 2GB free space

---

## Quick Start with Docker

### 1. Clone the Repository

```bash
git clone <repository-url>
cd content_verification_tool
```

### 2. Build and Start Services

```bash
docker-compose up --build
```

This will:
- Build both backend and frontend Docker images
- Start the backend API on http://localhost:8000
- Start the frontend UI on http://localhost:8501
- Create persistent volumes for cache and output files

### 3. Access the Application

Open your browser and navigate to:

**Frontend UI**: http://localhost:8501

**API Documentation**: http://localhost:8000/docs

### 4. Stop Services

```bash
# Stop services (keep volumes)
docker-compose down

# Stop services and remove volumes
docker-compose down -v
```

---

## Local Development Setup

### Backend Setup

#### 1. Navigate to Backend Directory

```bash
cd backend
```

#### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Download SpaCy Model

```bash
python -m spacy download en_core_web_sm
```

#### 5. Run Backend Server

```bash
# From backend directory
cd app
python main.py

# Or use uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be available at http://localhost:8000

### Frontend Setup

#### 1. Open New Terminal and Navigate to Frontend Directory

```bash
cd frontend
```

#### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Set Backend URL (Optional)

```bash
# Linux/Mac
export BACKEND_URL=http://localhost:8000

# Windows
set BACKEND_URL=http://localhost:8000
```

#### 5. Run Frontend Application

```bash
streamlit run app.py
```

The frontend will be available at http://localhost:8501

---

## Usage Guide

### Step-by-Step Workflow

#### 1. Upload Document

- Click **"Choose a file"** or drag and drop
- Supported formats: **PDF**, **DOCX**
- Maximum file size: **100 MB**
- Click **"🚀 Upload and Process"**

The system will:
- Validate the file
- Convert it using Docling
- Extract document structure
- Cache the result

#### 2. Select Chunking Mode

Choose how to split your document:

**📝 Paragraph-level chunking**
- Groups related sentences together
- Best for contextual verification
- Produces fewer, larger chunks

**📄 Sentence-level chunking**
- Splits into individual sentences
- Best for detailed verification
- Produces more, smaller chunks

#### 3. Choose Output Format

Select your preferred output:

**📄 Word Document (Landscape)**
- More horizontal space
- Better for long text
- Ideal for detailed notes

**📄 Word Document (Portrait)**
- Standard page layout
- Suitable for printing
- Traditional format

**📊 Excel Spreadsheet**
- Filtering and sorting capabilities
- Formula support
- Data analysis features

**📋 CSV File**
- Universal compatibility
- Lightweight format
- Easy import/export

#### 4. Generate and Download

- Click **"🎯 Generate Document"**
- Wait for processing (may take 30-60 seconds for large documents)
- Click **"⬇️ Download Verification Document"**

### Output Structure

All outputs contain a table with these columns:

| Column | Description |
|--------|-------------|
| **Page #** | Page number where the item appears |
| **Item #** | Item number on that page (resets per page) |
| **Text** | The sentence or paragraph text |
| **Verified ☑** | Checkbox for marking verification status |
| **Verification Source** | Field to record the source used for verification |
| **Verification Note** | Field for additional notes or comments |

---

## API Documentation

### Available Endpoints

#### Health Check

```bash
GET http://localhost:8000/health
```

Returns backend status and configuration.

#### Upload Document

```bash
POST http://localhost:8000/upload
Content-Type: multipart/form-data

file: <PDF or DOCX file>
```

Returns document metadata and ID.

#### Chunk Document

```bash
POST http://localhost:8000/chunk
Content-Type: application/json

{
  "document_id": "string",
  "chunking_mode": "paragraph" | "sentence"
}
```

Returns list of chunks with metadata.

#### Export Document

```bash
POST http://localhost:8000/export
Content-Type: application/json

{
  "document_id": "string",
  "chunking_mode": "paragraph" | "sentence",
  "output_format": "word_landscape" | "word_portrait" | "excel" | "csv"
}
```

Returns export metadata.

#### Download File

```bash
GET http://localhost:8000/download/{document_id}
```

Downloads the exported file.

#### Clear Cache

```bash
DELETE http://localhost:8000/cache/clear
```

Clears all cached documents.

### Interactive API Documentation

Visit http://localhost:8000/docs for Swagger UI with interactive testing.

---

## Troubleshooting

### Backend Issues

#### "Module not found" Error

```bash
# Ensure all dependencies are installed
pip install -r backend/requirements.txt

# Download SpaCy model
python -m spacy download en_core_web_sm
```

#### "Port 8000 already in use"

```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :8000    # Windows

# Or change the port in docker-compose.yml or backend startup
```

#### Docling Conversion Fails

- Ensure the PDF is not corrupted
- Check file size (max 100 MB)
- Try with a different PDF
- Check backend logs for detailed error

### Frontend Issues

#### "Backend API is not available"

1. Ensure backend is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Check BACKEND_URL environment variable:
   ```bash
   echo $BACKEND_URL  # Should be http://localhost:8000
   ```

3. Restart both services

#### Upload Fails

- Check file format (PDF or DOCX only)
- Verify file size (< 100 MB)
- Check backend logs for errors
- Try a smaller test document

#### Download Doesn't Start

- Ensure document was exported successfully
- Check browser's download settings
- Try a different browser
- Check backend /tmp/output directory permissions

### Docker Issues

#### Container Won't Start

```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild containers
docker-compose down -v
docker-compose up --build
```

#### Out of Memory

```bash
# Increase Docker memory limit in Docker Desktop settings
# Minimum: 4GB, Recommended: 8GB
```

#### Permission Errors

```bash
# Linux: Fix volume permissions
sudo chown -R $USER:$USER /tmp/document_cache /tmp/output
```

### Performance Issues

#### Slow Processing

- Large documents (50+ pages) may take 1-2 minutes
- Sentence mode is slower than paragraph mode
- First run downloads SpaCy model (one-time delay)

#### Memory Usage

- Backend may use 500MB-2GB RAM
- Frontend uses minimal resources
- Cache grows over time - clear periodically

---

## Advanced Configuration

### Environment Variables

#### Backend

- `PYTHONUNBUFFERED=1` - Enable real-time logging
- `CACHE_DIR` - Custom cache directory path
- `OUTPUT_DIR` - Custom output directory path

#### Frontend

- `BACKEND_URL` - Backend API URL (default: http://localhost:8000)
- `STREAMLIT_SERVER_PORT` - Custom Streamlit port

### Cache Management

Cache location: `/tmp/document_cache`

```bash
# Clear cache via API
curl -X DELETE http://localhost:8000/cache/clear

# Manual clear
rm -rf /tmp/document_cache/*
```

### Logs

#### Docker Logs

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Save logs to file
docker-compose logs > application.log
```

#### Local Development Logs

Backend logs appear in terminal where uvicorn is running.
Frontend logs appear in Streamlit terminal.

---

## Production Deployment

### Security Considerations

1. **Change CORS settings** in `backend/app/main.py`:
   ```python
   allow_origins=["https://your-frontend-domain.com"]
   ```

2. **Use HTTPS** with reverse proxy (nginx, Caddy)

3. **Set file size limits** at reverse proxy level

4. **Implement authentication** if needed

5. **Use persistent storage** for cache and outputs

### Scaling

- Use Redis for shared cache across instances
- Add load balancer for multiple backend instances
- Use object storage (S3, GCS) for outputs
- Implement queue system for async processing

---

## Support

For issues and questions:

1. Check this troubleshooting guide
2. Review backend logs
3. Test with sample documents
4. Check API documentation at /docs
5. Review the project plan in CLAUDE.md

---

**Version**: 1.0.0
**Last Updated**: 2025-11-11
