#!/bin/bash
# 🚀 Remote Server Startup Script for Linux/Ubuntu
# Usage: bash start_remote_backend.sh

set -e  # Exit on error

echo "=========================================="
echo "📦 Starting Jubilant Backend on Remote Server"
echo "=========================================="

# Variables
REPO_PATH="/home/user/jubilant"  # CHANGE THIS TO YOUR PATH
VENV_PATH="$REPO_PATH/venv"
LOG_PATH="$REPO_PATH/backend.log"
PID_FILE="$REPO_PATH/backend.pid"

# Step 1: Navigate to project directory
echo "📂 Navigating to $REPO_PATH"
cd "$REPO_PATH"

# Step 2: Create virtual environment if it doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv "$VENV_PATH"
fi

# Step 3: Activate virtual environment
echo "🔌 Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Step 4: Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Step 5: Kill any existing process on port 3002
echo "🛑 Checking for existing processes on port 3002..."
if lsof -i :3002 > /dev/null 2>&1; then
    echo "⚠️  Process found on port 3002, stopping it..."
    fuser -k 3002/tcp || true
fi

# Step 6: Start backend server in background
echo "🚀 Starting backend server on port 3002..."
nohup python -u server.py > "$LOG_PATH" 2>&1 &
BACKEND_PID=$!
echo "$BACKEND_PID" > "$PID_FILE"

# Step 7: Wait a moment for server to start
sleep 3

# Step 8: Verify server is running
if ps -p $BACKEND_PID > /dev/null; then
    echo "✅ Backend started successfully!"
    echo "📊 Server PID: $BACKEND_PID"
    echo "📝 Log file: $LOG_PATH"
    echo "🌐 Access at: https://agentic-gl.sequelstring.com:3002"
    echo ""
    echo "📋 View logs: tail -f $LOG_PATH"
    echo "🛑 Stop server: kill $BACKEND_PID"
else
    echo "❌ Failed to start backend!"
    cat "$LOG_PATH"
    exit 1
fi

echo "=========================================="
