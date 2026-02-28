# ⚡ QUICK COMMAND REFERENCE - Backend & Frontend Setup

## 🎯 What You Need to Know

Your system has TWO parts:
- **Backend**: Python/FastAPI running on remote server at port 3002
- **Frontend**: React/Vite running on local machine at port 3005
- **Connection**: Frontend calls Backend via `https://agentic-gl.sequelstring.com:3002`

---

## 📋 QUICK COMMAND CHEAT SHEET

### 🌐 REMOTE SERVER COMMANDS (Run via SSH)

#### For Linux/Ubuntu:
```bash
# 1. Connect to remote server
ssh user@agentic-gl.sequelstring.com

# 2. Navigate to project
cd /home/user/jubilant

# 3. Create virtual environment (first time only)
python3 -m venv venv

# 4. Activate it
source venv/bin/activate

# 5. Install dependencies (first time only)
pip install -r requirements.txt

# 6. Run backend server
python server.py
# OR use Uvicorn directly:
uvicorn server:app --host 0.0.0.0 --port 3002 --reload

# 7. Run in background (keeps running after SSH disconnect)
nohup python server.py > server.log 2>&1 &

# 8. View logs
tail -f server.log

# 9. Stop the server
pkill -f server.py
```

#### For Windows Remote Server:
```powershell
# 1. Open PowerShell as Administrator

# 2. Navigate to project
cd C:\jubilant

# 3. Create virtual environment (first time only)
python -m venv venv

# 4. Activate it
.\venv\Scripts\Activate.ps1

# 5. Install dependencies (first time only)
pip install -r requirements.txt

# 6. Run backend
python server.py
# OR:
uvicorn server:app --host 0.0.0.0 --port 3002

# 7. Stop the server
# Press Ctrl+C in the terminal
```

---

### 💻 LOCAL MACHINE COMMANDS (Windows PowerShell)

#### Option A: Using Batch File (Easiest)
```powershell
# 1. Double-click this file to run:
# d:\SEQUELSTRING\jubilant\jubilant\start_local_frontend.bat

# 2. Wait for: "Local: http://localhost:3005"

# 3. Open browser and go to: http://localhost:3005
```

#### Option B: Using PowerShell Script
```powershell
# 1. Open PowerShell in the jubilant folder

# 2. Run the startup script:
cd d:\SEQUELSTRING\jubilant\jubilant
.\start_local_frontend.ps1

# 3. Wait for development server to start

# 4. Open browser: http://localhost:3005
```

#### Option C: Manual Commands
```powershell
# 1. Navigate to frontend folder
cd d:\SEQUELSTRING\jubilant\jubilant\frontend

# 2. Install dependencies (first time only)
npm install

# 3. Create .env file if not exists
# Add this line: VITE_API_BASE_URL=https://agentic-gl.sequelstring.com:3002

# 4. Run development server
npm run dev

# 5. Output will show: Local: http://localhost:3005
# 6. Open that URL in your browser
```

---

## 🧪 TESTING THE CONNECTION

### From Local Machine PowerShell:
```powershell
# Test if backend is accessible
curl https://agentic-gl.sequelstring.com:3002/health

# Or using Invoke-WebRequest
Invoke-WebRequest -Uri https://agentic-gl.sequelstring.com:3002/health
```

### From Remote Server (via SSH):
```bash
# Test backend is running
curl http://localhost:3002/health

# Or from a different machine
curl https://agentic-gl.sequelstring.com:3002/health
```

---

## 🚀 COMPLETE EXAMPLE: Step-by-Step

### **Step 1: Start Backend on Remote Server (via SSH)**
```bash
# On your local PowerShell, open SSH connection:
ssh user@agentic-gl.sequelstring.com

# On remote server terminal:
cd /home/user/jubilant
source venv/bin/activate
nohup python server.py > server.log 2>&1 &
echo "Backend started!"
```

### **Step 2: Start Frontend on Local Machine**
```powershell
# On local PowerShell:
cd d:\SEQUELSTRING\jubilant\jubilant\frontend
npm run dev

# Output:
# ➜  Local:   http://localhost:3005/
```

### **Step 3: Access the Application**
```
Open browser: http://localhost:3005
Frontend automatically calls: https://agentic-gl.sequelstring.com:3002
```

---

## 🔧 IMPORTANT ENVIRONMENT VARIABLES

### **Frontend .env** (d:\SEQUELSTRING\jubilant\jubilant\frontend\.env)
```env
VITE_API_BASE_URL=https://agentic-gl.sequelstring.com:3002
```

### **Backend in server.py** (already configured)
```python
CORS: allow_origins=["*"]  # Allows all origins
```

---

## ⚠️ COMMON ISSUES & FIXES

| Problem | Solution |
|---------|----------|
| **"Connection refused" error** | Make sure backend is running on remote server |
| **SSL certificate error** | Use `http://` instead of `https://` OR disable SSL check |
| **Frontend shows blank page** | Check browser console (F12) for errors, check backend is running |
| **Port 3002 already in use** | Kill process: `pkill -f server.py` or use different port |
| **Port 3005 already in use** | Change vite.config.ts to use different port |
| **CORS error** | Already fixed in server.py, but check backend is actually running |
| **Cannot SSH to remote** | Check SSH key, IP address, firewall rules |

---

## 📊 SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERNET / DOMAIN                         │
│                  agentic-gl.sequelstring.com                │
└─────────────────┬───────────────────────────────┬───────────┘
                  │                               │
          ┌───────▼────────┐            ┌────────▼──────────┐
          │  Remote Server │            │  Local Machine    │
          │  (Linux/Wins)  │            │  (Your Computer)  │
          ├────────────────┤            ├──────────────────┤
          │  PORT 3002     │◄──────────►│  PORT 3005        │
          │  Backend       │   HTTPS    │  Frontend         │
          │  Python        │ + API REST │  React            │
          │  FastAPI       │            │  Vite             │
          └────────────────┘            └──────────────────┘
                  ▲
                  │
          nohup python
          server.py
```

---

## 🎯 FINAL CHECKLIST

✅ Backend running on remote server (port 3002)
✅ Frontend running on local machine (port 3005)
✅ .env file configured with `VITE_API_BASE_URL=https://agentic-gl.sequelstring.com:3002`
✅ Port 3002 is open on firewall
✅ Domain `agentic-gl.sequelstring.com` resolves to remote server IP
✅ Browser can access http://localhost:3005
✅ Frontend console shows no CORS errors

---

## 📞 Still Having Issues?

**Check 1: Is backend running?**
```bash
curl https://agentic-gl.sequelstring.com:3002/health
```

**Check 2: What's in browser console?**
Press F12 in browser → Console tab → Look for errors

**Check 3: Are ports open?**
```bash
# On remote server
netstat -an | grep 3002
# Or
ss -tuln | grep 3002
```

**Check 4: Frontend .env file**
```powershell
cat d:\SEQUELSTRING\jubilant\jubilant\frontend\.env
```

