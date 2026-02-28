# 🚀 Local Frontend Startup Script for Windows PowerShell
# Usage: .\start_local_frontend.ps1

$ErrorActionPreference = "Stop"

Clear-Host
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🖥️  Starting Jubilant Frontend (Local)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to frontend directory
$FRONTEND_PATH = "d:\SEQUELSTRING\jubilant\jubilant\frontend"
Write-Host "📂 Navigating to $FRONTEND_PATH" -ForegroundColor Green
Set-Location $FRONTEND_PATH

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    npm install
}

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "📝 Creating .env file..." -ForegroundColor Yellow
    @"
VITE_API_BASE_URL=https://agentic-gl.sequelstring.com:3002
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✅ .env created with backend URL" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Starting frontend development server..." -ForegroundColor Cyan
Write-Host "📂 Directory: $(Get-Location)" -ForegroundColor Gray
Write-Host "⏳ Wait for 'Local: http://localhost:3005'" -ForegroundColor Gray
Write-Host ""

# Run the development server
npm run dev
