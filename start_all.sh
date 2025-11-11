#!/bin/bash

# Start All Services Script for Content Verification Tool

echo "=========================================================="
echo "  Content Verification Tool - Starting All Services"
echo "=========================================================="
echo ""

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "🐳 Docker detected! Starting with Docker Compose..."
    echo ""
    echo "This will:"
    echo "  - Build backend and frontend containers"
    echo "  - Start backend API on http://localhost:8000"
    echo "  - Start frontend UI on http://localhost:8501"
    echo ""
    read -p "Continue with Docker? (y/n) " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "🚀 Starting services with Docker Compose..."
        docker-compose up --build
        exit 0
    fi
fi

# Local development mode
echo "📍 Starting in local development mode..."
echo ""
echo "This will start backend and frontend in separate terminal windows."
echo "Make sure you have Python 3.11+ installed."
echo ""
read -p "Continue with local mode? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Check if tmux is available
if command -v tmux &> /dev/null; then
    echo ""
    echo "🖥️  Starting services in tmux session..."

    # Create tmux session with two panes
    tmux new-session -d -s verification_tool

    # Split window horizontally
    tmux split-window -h -t verification_tool

    # Start backend in left pane
    tmux send-keys -t verification_tool:0.0 './start_backend.sh' C-m

    # Wait a bit for backend to start
    sleep 5

    # Start frontend in right pane
    tmux send-keys -t verification_tool:0.1 './start_frontend.sh' C-m

    # Attach to session
    echo ""
    echo "✓ Services started in tmux session 'verification_tool'"
    echo ""
    echo "Commands:"
    echo "  - Switch panes: Ctrl+B then arrow keys"
    echo "  - Detach session: Ctrl+B then D"
    echo "  - Reattach: tmux attach -t verification_tool"
    echo "  - Kill session: tmux kill-session -t verification_tool"
    echo ""
    sleep 2
    tmux attach -t verification_tool

else
    echo ""
    echo "⚠️  tmux not found. Please start services manually:"
    echo ""
    echo "Terminal 1: ./start_backend.sh"
    echo "Terminal 2: ./start_frontend.sh"
    echo ""
fi
