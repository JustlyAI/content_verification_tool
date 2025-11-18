# Backend Dockerfile for Content Verification Tool
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set HuggingFace cache location before installing dependencies
ENV HF_HOME=/app/.cache/huggingface

# Create cache directories for models
RUN mkdir -p /app/.cache/huggingface/transformers /app/.cache/huggingface/datasets /app/.cache/torch /app/.cache/docling_artifacts

# Install system dependencies including OpenGL libraries for Docling and LibreOffice
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    libreoffice-writer \
    libreoffice-calc \
    default-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spacy model
RUN python -m spacy download en_core_web_sm

# Create a minimal test PDF and process it to cache all required models
RUN python -c "\
from reportlab.pdfgen import canvas; \
from reportlab.lib.pagesizes import letter; \
import tempfile; \
from pathlib import Path; \
tmp = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False); \
test_pdf = tmp.name; \
c = canvas.Canvas(test_pdf, pagesize=letter); \
c.drawString(100, 750, 'Test document for model caching'); \
c.save(); \
tmp.close(); \
print('✓ Created test PDF'); \
from docling.document_converter import DocumentConverter; \
from docling.datamodel.pipeline_options import PdfPipelineOptions; \
from docling.datamodel.base_models import InputFormat; \
from docling.document_converter import PdfFormatOption; \
pipeline_options = PdfPipelineOptions(); \
pipeline_options.do_table_structure = False; \
pipeline_options.do_ocr = False; \
converter = DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}); \
print('✓ Processing test PDF to download and cache models...'); \
result = converter.convert(test_pdf); \
print(f'✓ Successfully processed test document ({len(result.document.pages)} pages)'); \
print('✓ All required models downloaded and cached'); \
Path(test_pdf).unlink(); \
"

# Copy application code
COPY ./app ./app

# Create directories for cache and output
RUN mkdir -p /tmp/document_cache /tmp/output

# Expose port
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DOCLING_LIBREOFFICE_CMD=/usr/bin/libreoffice
ENV PORT=8080

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]