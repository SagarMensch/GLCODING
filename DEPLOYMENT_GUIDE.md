# Deployment Guide for Remote Server

## Your Server Details
- **External IP:** `35.244.36.222`
- **Internal IP:** `10.19.0.2`
- **Domain:** `https://agentic-gl.sequelstring.com`
- **Port:** `3002`

## Step 1: Copy Code to the Server
Copy the entire `jubilant\jubilant\` folder to the remote server. Example:
```
C:\Apps\jubilant\
    ├── jubilant\              ← Backend (server.py, .env)
    │   └── frontend\          ← React source code
    ├── DEPLOYMENT_PACKAGE\    ← setup_server.ps1 & start_proxy.ps1
    └── PRODUCTION_DEPLOYMENT\
        └── proxy\             ← Node.js reverse proxy
```

## Step 2: Run Setup (ONE TIME ONLY)
Open PowerShell on the remote server:
```powershell
cd "C:\Apps\jubilant\DEPLOYMENT_PACKAGE"
powershell.exe -ExecutionPolicy Bypass -File .\setup_server.ps1
```
This automatically: creates venv, installs Python packages, builds React, installs Node proxy.

## Step 3: Launch the Application
```powershell
powershell.exe -ExecutionPolicy Bypass -File .\start_proxy.ps1
```

## Result
Client opens `https://agentic-gl.sequelstring.com` → sees the full application.

## Architecture
```
Client Browser
     │
     ▼
[Port 3002] Node.js Proxy (0.0.0.0:3002)
     │
     ├── /api/*  →  [Port 8001] Python Backend (127.0.0.1:8001)
     └── /*      →  Serves React Frontend (static files)
```
