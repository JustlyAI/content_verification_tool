#!/bin/bash

# Start Backend Script for Content Verification Tool

echo "=================================================="
echo "  Content Verification Tool - Backend Startup"
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✓ Python3 found: $(python3 --version)"

# Navigate to backend directory
cd backend || exit 1

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Download SpaCy model if not present
echo ""
echo "📚 Checking SpaCy model..."
if ! python -c "import spacy; spacy.load('en_core_web_sm')" &> /dev/null; then
    echo "📥 Downloading SpaCy model en_core_web_sm..."
    python -m spacy download en_core_web_sm
    echo "✓ SpaCy model installed"
else
    echo "✓ SpaCy model already installed"
fi

# Create necessary directories
echo ""
echo "📁 Creating cache and output directories..."
mkdir -p /tmp/document_cache /tmp/output
echo "✓ Directories created"

# Start the backend server
echo ""
echo "=================================================="
echo "🚀 Starting Backend API Server..."
echo "=================================================="
echo ""
echo "📍 API URL: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo "🏥 Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd app
python main.py
