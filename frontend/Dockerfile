# Frontend Dockerfile for Content Verification Tool
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY app/ ./app/
COPY gemini-logo.png .

# Expose Streamlit port
EXPOSE 8501

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV BACKEND_URL=http://backend:8080
ENV PORT=8501

# Health check (use PORT variable)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/_stcore/health || exit 1

# Run Streamlit on PORT from environment (Cloud Run compatibility)
# Use exec form with sh -c to properly handle signals while expanding PORT
CMD ["sh", "-c", "streamlit run main.py --server.port=${PORT} --server.address=0.0.0.0"]
