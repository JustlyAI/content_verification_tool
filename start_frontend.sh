#!/bin/bash

# Start Frontend Script for Content Verification Tool

echo "=================================================="
echo "  Content Verification Tool - Frontend Startup"
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✓ Python3 found: $(python3 --version)"

# Check if backend is running
echo ""
echo "🔍 Checking backend connection..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✓ Backend is running at http://localhost:8000"
else
    echo "⚠️  Warning: Backend is not responding at http://localhost:8000"
    echo "   Please start the backend first using ./start_backend.sh"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Navigate to frontend directory
cd frontend || exit 1

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

# Set backend URL
export BACKEND_URL=http://localhost:8000

# Start the frontend server
echo ""
echo "=================================================="
echo "🚀 Starting Frontend Application..."
echo "=================================================="
echo ""
echo "🌐 Frontend URL: http://localhost:8501"
echo "🔗 Backend URL: $BACKEND_URL"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

streamlit run app.py
