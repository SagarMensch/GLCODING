# 🚀 Remote Server Startup Script for Windows PowerShell
# Usage: .\start_remote_backend.ps1

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "📦 Starting Jubilant Backend on Windows Remote Server" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Variables
$REPO_PATH = "C:\jubilant"  # CHANGE THIS TO YOUR PATH
$VENV_PATH = "$REPO_PATH\venv"
$LOG_PATH = "$REPO_PATH\backend.log"

# Step 1: Navigate to project directory
Write-Host "📂 Navigating to $REPO_PATH" -ForegroundColor Green
Set-Location $REPO_PATH

# Step 2: Create virtual environment if it doesn't exist
if (-not (Test-Path $VENV_PATH)) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv $VENV_PATH
}

# Step 3: Activate virtual environment
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Green
& "$VENV_PATH\Scripts\Activate.ps1"

# Step 4: Install dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
pip install -q -r requirements.txt

# Step 5: Kill any existing process on port 3002
Write-Host "🛑 Checking for existing processes on port 3002..." -ForegroundColor Yellow
$processOnPort = Get-NetTCPConnection -LocalPort 3002 -ErrorAction SilentlyContinue
if ($processOnPort) {
    Write-Host "⚠️  Process found on port 3002, stopping it..." -ForegroundColor Red
    Stop-Process -Id $processOnPort.OwningProcess -Force
    Start-Sleep -Seconds 1
}

# Step 6: Start backend server
Write-Host "🚀 Starting backend server on port 3002..." -ForegroundColor Cyan
Write-Host "📝 Log file: $LOG_PATH" -ForegroundColor Gray

# Run the server (this will block the terminal)
python server.py | Tee-Object -FilePath $LOG_PATH

Write-Host "==========================================" -ForegroundColor Cyan
