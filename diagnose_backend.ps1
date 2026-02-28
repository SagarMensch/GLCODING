# 🔧 Windows Diagnostic Script for Backend
# Usage: .\diagnose_backend.ps1

Clear-Host
Write-Host ""
Write-Host "════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🔍 WINDOWS BACKEND DIAGNOSTIC TOOL" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check 1: Is Python installed?
Write-Host "1️⃣  Checking Python installation..." -ForegroundColor Yellow
$PythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if ($PythonPath) {
    $PythonVersion = python --version
    Write-Host "   ✅ $PythonVersion found at: $PythonPath" -ForegroundColor Green
} else {
    Write-Host "   ❌ Python not found! Install Python first." -ForegroundColor Red
    exit 1
}

# Check 2: Is port 3002 open?
Write-Host ""
Write-Host "2️⃣  Checking if port 3002 is available..." -ForegroundColor Yellow
$ProcessOnPort = Get-NetTCPConnection -LocalPort 3002 -ErrorAction SilentlyContinue
if ($ProcessOnPort) {
    Write-Host "   ⚠️  Port 3002 is already in use:" -ForegroundColor Red
    Get-Process -Id $ProcessOnPort.OwningProcess | Select-Object ProcessName, Id
    Write-Host "   To free it: taskkill /PID $($ProcessOnPort.OwningProcess) /F" -ForegroundColor Yellow
} else {
    Write-Host "   ✅ Port 3002 is available" -ForegroundColor Green
}

# Check 3: Check virtual environment
Write-Host ""
Write-Host "3️⃣  Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "   ✅ Virtual environment found" -ForegroundColor Green
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "   ✅ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "   ❌ Virtual environment not found" -ForegroundColor Red
    Write-Host "   Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "   ✅ Virtual environment created and activated" -ForegroundColor Green
}

# Check 4: Check dependencies
Write-Host ""
Write-Host "4️⃣  Checking Python dependencies..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    $RequiredPackages = @("fastapi", "uvicorn", "sqlalchemy", "supabase", "pandas", "numpy", "scikit-learn")
    $MissingCount = 0
    
    foreach ($Package in $RequiredPackages) {
        try {
            python -c "import $Package" 2>$null
            Write-Host "   ✅ $Package installed" -ForegroundColor Green
        } catch {
            Write-Host "   ❌ $Package missing" -ForegroundColor Red
            $MissingCount++
        }
    }
    
    if ($MissingCount -gt 0) {
        Write-Host ""
        Write-Host "   Installing missing packages..." -ForegroundColor Yellow
        pip install -q -r requirements.txt
        Write-Host "   ✅ Packages installed" -ForegroundColor Green
    }
} else {
    Write-Host "   ❌ requirements.txt not found" -ForegroundColor Red
}

# Check 5: Check FastAPI
Write-Host ""
Write-Host "5️⃣  Checking FastAPI/Uvicorn..." -ForegroundColor Yellow
try {
    $Version = python -c "import fastapi; print(fastapi.__version__)" 2>$null
    Write-Host "   ✅ FastAPI $Version installed" -ForegroundColor Green
} catch {
    Write-Host "   ❌ FastAPI not found, installing..." -ForegroundColor Red
    pip install -q fastapi uvicorn
}

# Check 6: Check if server.py exists
Write-Host ""
Write-Host "6️⃣  Checking server.py..." -ForegroundColor Yellow
if (Test-Path "server.py") {
    $FileSize = (Get-Item "server.py").Length
    Write-Host "   ✅ server.py found" -ForegroundColor Green
    Write-Host "   📊 File size: $FileSize bytes" -ForegroundColor Gray
} else {
    Write-Host "   ❌ server.py not found in current directory" -ForegroundColor Red
    exit 1
}

# Check 7: Syntax check
Write-Host ""
Write-Host "7️⃣  Checking Python syntax..." -ForegroundColor Yellow
try {
    python -m py_compile server.py 2>$null
    Write-Host "   ✅ No syntax errors" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Syntax errors found:" -ForegroundColor Red
    python -m py_compile server.py
    exit 1
}

# Check 8: Check network connectivity
Write-Host ""
Write-Host "8️⃣  Checking network connectivity..." -ForegroundColor Yellow
try {
    $Connection = Test-Connection 8.8.8.8 -Count 1 -ErrorAction Stop
    Write-Host "   ✅ Internet connection available" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  No internet connection (needed for APIs)" -ForegroundColor Yellow
}

# Check 9: Environment variables
Write-Host ""
Write-Host "9️⃣  Checking environment variables..." -ForegroundColor Yellow
$EnvVars = @("SUPABASE_URL", "SUPABASE_KEY", "MISTRAL_API_KEY")
foreach ($Var in $EnvVars) {
    if ([Environment]::GetEnvironmentVariable($Var)) {
        Write-Host "   ✅ $Var is set" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  $Var not set (may be needed)" -ForegroundColor Yellow
    }
}

# Summary
Write-Host ""
Write-Host "════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✅ DIAGNOSTIC COMPLETE" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ready to start backend? Run one of these:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Option 1: python server.py" -ForegroundColor White
Write-Host "   Option 2: uvicorn server:app --host 0.0.0.0 --port 3002 --reload" -ForegroundColor White
Write-Host ""
