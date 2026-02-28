#!/bin/bash
# 🔧 Troubleshooting & Diagnostic Script for Remote Backend
# Usage: bash diagnose_backend.sh

echo "════════════════════════════════════════════════"
echo "🔍 BACKEND DIAGNOSTIC TOOL"
echo "════════════════════════════════════════════════"
echo ""

# Check 1: Is Python installed?
echo "1️⃣  Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ $PYTHON_VERSION"
else
    echo "   ❌ Python3 not found! Install it first."
    exit 1
fi

# Check 2: Is port 3002 open?
echo ""
echo "2️⃣  Checking if port 3002 is available..."
if lsof -i :3002 > /dev/null 2>&1; then
    echo "   ⚠️  Port 3002 is already in use:"
    lsof -i :3002
    echo "   To free it: fuser -k 3002/tcp"
else
    echo "   ✅ Port 3002 is available"
fi

# Check 3: Check virtual environment
echo ""
echo "3️⃣  Checking virtual environment..."
if [ -d "venv" ]; then
    echo "   ✅ Virtual environment found"
    source venv/bin/activate
    echo "   ✅ Virtual environment activated"
else
    echo "   ❌ Virtual environment not found"
    echo "   Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "   ✅ Virtual environment created and activated"
fi

# Check 4: Check dependencies
echo ""
echo "4️⃣  Checking Python dependencies..."
if [ -f "requirements.txt" ]; then
    MISSING=0
    while IFS= read -r package || [ -n "$package" ]; do
        # Remove version specifiers for checking
        PACKAGE_NAME=$(echo "$package" | cut -d'=' -f1 | cut -d'<' -f1 | cut -d'>' -f1)
        if python3 -c "import $PACKAGE_NAME" 2>/dev/null; then
            echo "   ✅ $PACKAGE_NAME installed"
        else
            echo "   ❌ $PACKAGE_NAME missing"
            MISSING=$((MISSING+1))
        fi
    done < requirements.txt
    
    if [ $MISSING -gt 0 ]; then
        echo ""
        echo "   Installing missing packages..."
        pip install -q -r requirements.txt
        echo "   ✅ Packages installed"
    fi
else
    echo "   ❌ requirements.txt not found"
fi

# Check 5: Check FastAPI and Uvicorn
echo ""
echo "5️⃣  Checking FastAPI/Uvicorn..."
if python3 -c "import fastapi; print(f'FastAPI {fastapi.__version__}')" 2>/dev/null; then
    echo "   ✅ FastAPI installed"
else
    echo "   ❌ FastAPI not found, installing..."
    pip install -q fastapi uvicorn
fi

# Check 6: Check if server.py exists
echo ""
echo "6️⃣  Checking server.py..."
if [ -f "server.py" ]; then
    echo "   ✅ server.py found"
    LINES=$(wc -l < server.py)
    echo "   📊 File size: $LINES lines"
else
    echo "   ❌ server.py not found in current directory"
    exit 1
fi

# Check 7: Syntax check
echo ""
echo "7️⃣  Checking Python syntax..."
if python3 -m py_compile server.py 2>/dev/null; then
    echo "   ✅ No syntax errors"
else
    echo "   ❌ Syntax errors found:"
    python3 -m py_compile server.py
    exit 1
fi

# Check 8: Check network connectivity
echo ""
echo "8️⃣  Checking network connectivity..."
if ping -c 1 8.8.8.8 > /dev/null 2>&1; then
    echo "   ✅ Internet connection available"
else
    echo "   ⚠️  No internet connection (needed for APIs)"
fi

# Check 9: Check firewall for port 3002
echo ""
echo "9️⃣  Checking firewall..."
if sudo ufw status | grep -q "Status: active"; then
    if sudo ufw status | grep -q "3002"; then
        echo "   ✅ Port 3002 is allowed in firewall"
    else
        echo "   ⚠️  Port 3002 not in firewall rules"
        echo "   To allow: sudo ufw allow 3002/tcp"
    fi
else
    echo "   ℹ️  Firewall status: inactive (probably OK)"
fi

# Summary
echo ""
echo "════════════════════════════════════════════════"
echo "✅ DIAGNOSTIC COMPLETE"
echo "════════════════════════════════════════════════"
echo ""
echo "Ready to start backend? Run:"
echo "   python server.py"
echo ""
echo "Or with Uvicorn:"
echo "   uvicorn server:app --host 0.0.0.0 --port 3002 --reload"
echo ""
