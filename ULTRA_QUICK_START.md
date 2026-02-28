# ⚡ ULTRA-QUICK START (5 MINUTES)

## 🎯 The 3-Step Process

### STEP 1️⃣: Start Backend (on Remote Server)

**Via SSH Terminal:**
```bash
ssh user@agentic-gl.sequelstring.com
cd /home/user/jubilant
nohup python server.py > server.log 2>&1 &
echo "✅ Backend started!"
```

**OR Run This Script:**
```bash
bash start_remote_backend.sh
```

---

### STEP 2️⃣: Start Frontend (on Your Computer)

**Windows - Double-Click This File:**
```
d:\SEQUELSTRING\jubilant\jubilant\start_local_frontend.bat
```

**OR Run This Command:**
```powershell
cd d:\SEQUELSTRING\jubilant\jubilant
npm run dev
```

---

### STEP 3️⃣: Open Your Browser

```
http://localhost:3005
```

**DONE! 🎉**

---

## 🧪 Verify It Works

### Quick Test Commands

**Test 1: Backend is running?**
```powershell
curl https://agentic-gl.sequelstring.com:3002/health
# Should return: OK or some JSON
```

**Test 2: Frontend is running?**
```
Open http://localhost:3005 in browser
# Should see your React app
```

**Test 3: They can talk to each other?**
```
Open Browser DevTools (F12)
Console tab → Should have NO red errors
```

---

## 📊 What's Running Where

| Component | Location | URL | Status |
|-----------|----------|-----|--------|
| **Backend** | Remote Server | `https://agentic-gl.sequelstring.com:3002` | Should be 🟢 Running |
| **Frontend** | Your Computer | `http://localhost:3005` | Should be 🟢 Running |

---

## 🆘 If Something Doesn't Work

### Problem: Backend won't start
**Solution:**
```bash
# Run diagnostic
bash diagnose_backend.sh

# Then try starting again
python server.py
```

### Problem: Frontend won't start
**Solution:**
```powershell
cd d:\SEQUELSTRING\jubilant\jubilant\frontend
npm install
npm run dev
```

### Problem: "Cannot connect to backend"
**Solution:**
```powershell
# Verify backend is really running
curl https://agentic-gl.sequelstring.com:3002/health

# Check .env file
cat d:\SEQUELSTRING\jubilant\jubilant\frontend\.env
# Should contain: VITE_API_BASE_URL=https://agentic-gl.sequelstring.com:3002
```

---

## 📁 All Files Created For You

```
✅ DEPLOYMENT_GUIDE.md              ← Detailed guide
✅ QUICK_COMMAND_REFERENCE.md       ← Commands cheat sheet
✅ README_SETUP.md                  ← Full setup docs
✅ SETUP_SUMMARY.md                 ← Overview
✅ ULTRA_QUICK_START.md             ← THIS FILE

✅ requirements.txt                 ← Python packages
✅ start_remote_backend.sh          ← Linux backend start
✅ start_remote_backend.ps1         ← Windows backend start
✅ start_local_frontend.bat         ← Windows frontend start (RECOMMENDED!)
✅ start_local_frontend.ps1         ← PowerShell frontend start
✅ diagnose_backend.sh              ← Linux diagnostics
✅ diagnose_backend.ps1             ← Windows diagnostics

✅ frontend/.env                    ← API configuration
✅ frontend/vite.config.ts          ← Already updated
```

---

## 🔄 Daily Workflow

### **Morning: Start Everything**

**Terminal 1 - SSH to Remote:**
```bash
ssh user@agentic-gl.sequelstring.com
cd /home/user/jubilant
nohup python server.py > server.log 2>&1 &
```

**Terminal 2 - Local Frontend:**
```powershell
cd d:\SEQUELSTRING\jubilant\jubilant
npm run dev
# Then open: http://localhost:3005
```

### **During Day: Keep Working**
Just use http://localhost:3005 in your browser

### **Evening: Stop Services**
```bash
# Stop backend (via SSH)
pkill -f server.py

# Stop frontend
# Press Ctrl+C in the npm run dev terminal
```

---

## 💡 Pro Tips

**Tip 1: Keep Backend Running 24/7**
```bash
# Use nohup to keep running even after SSH disconnects
nohup python server.py > server.log 2>&1 &

# Later, check it's still running
ps aux | grep server.py
```

**Tip 2: View Logs in Real-Time**
```bash
# On remote server
tail -f server.log
```

**Tip 3: Use Browser Tabs**
- Tab 1: `http://localhost:3005` - Your app
- Tab 2: `https://agentic-gl.sequelstring.com:3002/docs` - API docs (Swagger)
- Tab 3: Check connection test

**Tip 4: Keep Terminal Open**
Never close the terminal running `npm run dev` - if you do, frontend stops!

---

## ⚡ Common Commands

### Start Backend (Remote)
```bash
python server.py                    # Simple start
nohup python server.py > server.log 2>&1 &   # Background
```

### Stop Backend (Remote)
```bash
pkill -f server.py
```

### Start Frontend (Local)
```powershell
npm run dev
```

### Stop Frontend (Local)
```
Ctrl+C in terminal
```

### Check Backend Status
```bash
ps aux | grep server.py             # Is it running?
tail -f server.log                  # View logs
curl https://agentic-gl.sequelstring.com:3002/health    # Is it responding?
```

### Check Frontend Status
```powershell
netstat -ano | findstr :3005        # Is port 3005 in use?
```

---

## 🎓 Understanding the Setup

```
Your Browser                   Your Computer           Remote Server
┌──────────────┐              ┌─────────────┐        ┌──────────────┐
│              │              │ Frontend    │        │ Backend      │
│ localhost:   │◄────HTTP────►│ (Vite)      │        │ (FastAPI)    │
│ 3005         │   Requests   │             │        │              │
│              │   + Responses│ port 3005   │        │ port 3002    │
│              │              │             │        │              │
│              │              │ npm run dev │        │ python       │
└──────────────┘              └─────────────┘        └──────────────┘
      │                              │                      │
      │                              │                      │
      └──────────────┬───────────────┴──────────────────────┘
                     │
         ┌───────────▼────────────┐
         │   Internet / Domain    │
         │ agentic-gl.            │
         │ sequelstring.com       │
         └────────────────────────┘
```

---

## ✅ Final Checklist Before You Start

- [ ] Backend code is on remote server
- [ ] Python 3.8+ is installed on remote server
- [ ] You can SSH to remote server
- [ ] Node.js/npm installed on local machine
- [ ] Port 3002 is open on firewall
- [ ] You've read this file
- [ ] All setup files are created

**Ready? Go to Step 1️⃣ above!**

---

## 🎉 Success Indicators

✅ Backend started successfully when you see: `Server: http://0.0.0.0:3002`
✅ Frontend started successfully when you see: `Local: http://localhost:3005/`
✅ Connection works when you can open `http://localhost:3005` and see your app
✅ Everything works when no red errors in browser console (F12)

---

**NOW GO START YOUR SYSTEM! 🚀**

**Questions?** Check `README_SETUP.md`
**Commands forgot?** Check `QUICK_COMMAND_REFERENCE.md`
**Connection issues?** Check `DEPLOYMENT_GUIDE.md`

