# Backend Dockerfile for Content Verification Tool
FROM python:3.11-slim

# Set working directory
WORKDIR /app

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

# Pre-download OCR models to avoid first-request delay
RUN python -c "from docling.document_converter import DocumentConverter; from docling.datamodel.base_models import InputFormat; from docling.datamodel.pipeline_options import PdfPipelineOptions; from docling.document_converter import PdfFormatOption; opts = PdfPipelineOptions(); opts.do_ocr = True; converter = DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)}); print('OCR models downloaded')"

# Copy application code
COPY ./app ./app

# Create directories for cache and output
RUN mkdir -p /tmp/document_cache /tmp/output

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DOCLING_LIBREOFFICE_CMD=/usr/bin/libreoffice

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
