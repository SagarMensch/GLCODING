# 🚀 JUBILANT - Backend & Frontend Integration Guide

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Architecture](#architecture)
3. [Remote Server Setup](#remote-server-setup)
4. [Local Frontend Setup](#local-frontend-setup)
5. [Connection Testing](#connection-testing)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Quick Start

### For the Impatient (TL;DR)

**On Remote Server (via SSH):**
```bash
cd /home/user/jubilant
source venv/bin/activate
nohup python server.py > server.log 2>&1 &
```

**On Local Machine (PowerShell):**
```powershell
cd d:\SEQUELSTRING\jubilant\jubilant\frontend
npm run dev
# Open browser: http://localhost:3005
```

---

## 🏗️ Architecture

```
Your Local Computer                    Remote Server
┌─────────────────────┐               ┌──────────────────┐
│  Browser            │               │  Backend         │
│  localhost:3005     │◄──HTTP REST──►│  port 3002       │
│  (React Frontend)   │               │  Python/FastAPI  │
└─────────────────────┘               └──────────────────┘
                                       https://agentic-gl.sequelstring.com:3002
```

---

## 🖥️ Remote Server Setup

### Prerequisites
- SSH access to `agentic-gl.sequelstring.com`
- Python 3.8+ installed
- Port 3002 open on firewall

### Step-by-Step Instructions

#### 1. **Connect to Remote Server**
```bash
# From your local machine
ssh user@agentic-gl.sequelstring.com
# Password: [enter your password]
```

#### 2. **Upload Code (if not already there)**
```bash
# From your local PowerShell
scp -r d:\SEQUELSTRING\jubilant\jubilant user@agentic-gl.sequelstring.com:/home/user/

# Or use WinSCP GUI for easier file transfer
```

#### 3. **Setup Virtual Environment**
```bash
# On remote server
cd /home/user/jubilant

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
# You should see (venv) at the start of terminal
```

#### 4. **Install Dependencies**
```bash
# Make sure you're in the venv
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. **Verify Setup**
```bash
# Run diagnostic
bash diagnose_backend.sh
# Should show all ✅ checks
```

#### 6. **Start Backend Server**

**Option A: Simple Start (for testing)**
```bash
python server.py
# Output: Starting Agentic AI Invoice Orchestration Platform
#         Server: http://0.0.0.0:3002
# Press Ctrl+C to stop
```

**Option B: Background Start (recommended for production)**
```bash
# Start in background (survives SSH disconnect)
nohup python server.py > server.log 2>&1 &

# View logs
tail -f server.log

# Check if running
ps aux | grep server.py

# Stop it
pkill -f server.py
```

**Option C: Using Uvicorn**
```bash
# With auto-reload (good for development)
uvicorn server:app --host 0.0.0.0 --port 3002 --reload

# Without reload (production)
uvicorn server:app --host 0.0.0.0 --port 3002 --workers 4
```

---

## 💻 Local Frontend Setup

### Prerequisites
- Node.js 16+ installed
- npm installed
- Code cloned locally

### Step-by-Step Instructions

#### 1. **Navigate to Frontend Directory**
```powershell
cd d:\SEQUELSTRING\jubilant\jubilant\frontend
```

#### 2. **Install Dependencies**
```powershell
npm install
# Takes 2-5 minutes on first run
```

#### 3. **Configure Environment**

Create `.env` file in frontend directory:
```env
VITE_API_BASE_URL=https://agentic-gl.sequelstring.com:3002
```

Create `.env.development` for development:
```env
VITE_API_BASE_URL=https://agentic-gl.sequelstring.com:3002
```

#### 4. **Start Development Server**
```powershell
npm run dev
# Output: ➜  Local:   http://localhost:3005/
#         ➜  press h to show help
```

#### 5. **Open in Browser**
```
http://localhost:3005
```

---

## 🔌 Connection Testing

### Test 1: Backend is Running
```bash
# From any machine
curl https://agentic-gl.sequelstring.com:3002/health
# OR
curl https://agentic-gl.sequelstring.com:3002/docs  # Swagger UI
```

### Test 2: DNS Resolution
```powershell
# From local PowerShell
nslookup agentic-gl.sequelstring.com
# Should return the IP address of remote server
```

### Test 3: Port Accessibility
```powershell
# From local PowerShell
Test-NetConnection -ComputerName agentic-gl.sequelstring.com -Port 3002
# Should show "TcpTestSucceeded : True"
```

### Test 4: API Call from Frontend
Add this component to test in your React app:

```tsx
// ConnectionTest.tsx
import { useEffect, useState } from 'react';

export default function ConnectionTest() {
  const [status, setStatus] = useState('Testing...');

  useEffect(() => {
    const testAPI = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_BASE_URL;
        const response = await fetch(`${apiUrl}/health`);
        setStatus(response.ok ? '✅ Connected' : '❌ Failed');
      } catch (error) {
        setStatus(`❌ Error: ${error.message}`);
      }
    };
    testAPI();
  }, []);

  return <div>{status}</div>;
}
```

---

## 🆘 Troubleshooting

### Issue: Frontend shows blank page
**Solution:**
1. Open DevTools (F12)
2. Check Console for errors
3. If API errors, verify backend is running: `curl https://agentic-gl.sequelstring.com:3002/health`

### Issue: "Connection refused" or "Failed to fetch"
**Solution:**
1. Verify backend is running on remote server: `ps aux | grep server.py`
2. Check port is open: `sudo netstat -tuln | grep 3002`
3. Check firewall: `sudo ufw status`
4. Allow port 3002: `sudo ufw allow 3002/tcp`

### Issue: SSL Certificate Error
**Solution:**
Option 1: Use http instead of https (if on private network)
Option 2: Add certificate exception
Option 3: Update environment variable: `VITE_API_BASE_URL=http://agentic-gl.sequelstring.com:3002`

### Issue: "Port 3002 already in use"
**Solution:**
```bash
# Find process using port
lsof -i :3002

# Kill it
fuser -k 3002/tcp
# OR
pkill -f server.py

# Or use different port
python server.py --port 3003  # Modify server.py to support this
```

### Issue: Frontend shows CORS error
**Solution:**
Already configured in server.py, but if still having issues:
1. Check server.py has: `allow_origins=["*"]`
2. Restart backend: `pkill -f server.py && python server.py`

### Issue: "Module not found" error
**Solution:**
```bash
# Make sure you're in venv
source venv/bin/activate

# Reinstall requirements
pip install --upgrade -r requirements.txt

# Check specific module
pip show fastapi
```

---

## 📚 File Reference

### Created Files
| File | Purpose |
|------|---------|
| `DEPLOYMENT_GUIDE.md` | Complete deployment instructions |
| `QUICK_COMMAND_REFERENCE.md` | Cheat sheet of commands |
| `requirements.txt` | Python dependencies |
| `start_remote_backend.sh` | Automated backend startup (Linux) |
| `start_remote_backend.ps1` | Automated backend startup (Windows) |
| `start_local_frontend.bat` | Automated frontend startup |
| `start_local_frontend.ps1` | Automated frontend startup (PowerShell) |
| `diagnose_backend.sh` | Diagnostic tool (Linux) |
| `diagnose_backend.ps1` | Diagnostic tool (Windows) |

### Configuration Files
| File | Purpose |
|------|---------|
| `frontend/.env` | Frontend environment variables |
| `frontend/vite.config.ts` | Vite configuration with proxy |
| `frontend/package.json` | Frontend dependencies |
| `server.py` | Backend main server file |

---

## ✅ Pre-Launch Checklist

- [ ] Backend running on remote server (port 3002)
- [ ] Frontend running locally (port 3005)
- [ ] `.env` file created with correct API URL
- [ ] Port 3002 is open on firewall
- [ ] Can reach backend via: `curl https://agentic-gl.sequelstring.com:3002/health`
- [ ] Browser can access: `http://localhost:3005`
- [ ] No CORS errors in browser console
- [ ] No connection errors in browser console

---

## 🚀 Running in Production

### Using PM2 (Recommended)
```bash
# Install PM2
npm install -g pm2

# Start backend
pm2 start "python server.py" --name backend

# View status
pm2 status

# View logs
pm2 logs backend

# Auto-start on reboot
pm2 startup
pm2 save
```

### Using systemd (Linux)
Create `/etc/systemd/system/jubilant-backend.service`:
```ini
[Unit]
Description=Jubilant Backend Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/jubilant
ExecStart=/home/ubuntu/jubilant/venv/bin/python server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable jubilant-backend
sudo systemctl start jubilant-backend
sudo systemctl status jubilant-backend
```

---

## 📞 Need Help?

1. Check logs:
   - Backend: `tail -f server.log`
   - Frontend: Check browser console (F12)

2. Run diagnostics:
   - Linux: `bash diagnose_backend.sh`
   - Windows: `.\diagnose_backend.ps1`

3. Check connectivity:
   ```powershell
   curl https://agentic-gl.sequelstring.com:3002/health
   curl https://agentic-gl.sequelstring.com:3002/docs
   ```

---

**Last Updated:** February 25, 2026
**Version:** 2.0.0
