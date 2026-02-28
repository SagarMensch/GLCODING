@REM 🚀 Local Frontend Startup Script for Windows
@REM Usage: start_local_frontend.bat

@echo off
setlocal enabledelayedexpansion

cls
echo.
echo ==========================================
echo 🖥️  Starting Jubilant Frontend (Local)
echo ==========================================
echo.

REM Navigate to frontend directory
cd /d d:\SEQUELSTRING\jubilant\jubilant\frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    call npm install
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 📝 Creating .env file...
    (
        echo VITE_API_BASE_URL=https://agentic-gl.sequelstring.com:3002
    ) > .env
    echo ✅ .env created with backend URL
)

echo.
echo 🚀 Starting frontend development server on port 3005...
echo 📂 Directory: %cd%
echo.

REM Run the development server
call npm run dev

pause
