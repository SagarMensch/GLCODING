# 🏗️ Architecture Diagram: How Frontend Talks to Remote Backend

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          YOUR SYSTEM ARCHITECTURE                           │
└─────────────────────────────────────────────────────────────────────────────┘

YOUR LOCAL MACHINE (Windows PC)
═══════════════════════════════════════════════════════════════════════════════
│
├─ 🌐 Browser
│  └─ http://localhost:3005
│     │
│     └─→ [React Frontend]
│         - App.tsx
│         - Components
│
├─ 📦 Vite Dev Server
│  ├─ Port: 3005
│  └─ Config: frontend/.env.local
│     VITE_API_BASE_URL=http://192.168.1.100:3002
│        │
│        └─→ ALL API CALLS GO HERE ↓
│

NETWORK (Internet/LAN)
═══════════════════════════════════════════════════════════════════════════════
│
├─ 🔌 Connection: http://192.168.1.100:3002
│  │
│  └─→ ✅ Frontend can reach backend
│


REMOTE SERVER (Windows/Linux Server)
═══════════════════════════════════════════════════════════════════════════════
│
├─ 🐍 Python Backend
│  ├─ Port: 3002
│  ├─ Command: uvicorn server:app --host 0.0.0.0 --port 3002
│  ├─ Status: ✅ RUNNING
│  │
│  ├─ Endpoints:
│  │  ├─ /api/process
│  │  ├─ /api/kpis
│  │  ├─ /api/upload
│  │  ├─ /api/history
│  │  └─ ... (etc)
│  │
│  └─ Database Connections
│     ├─ Supabase
│     ├─ Local SQLAlchemy DB
│     └─ Vector Search (ML Models)


WHAT HAPPENS WHEN YOU VISIT http://localhost:3005
═══════════════════════════════════════════════════════════════════════════════

1. Browser loads Frontend (React)
   └─ Gets files from http://localhost:3005

2. Frontend reads .env.local
   └─ VITE_API_BASE_URL=http://192.168.1.100:3002

3. Frontend makes API call
   ├─ Example: fetch('http://192.168.1.100:3002/api/process')
   └─ Request goes to Remote Server

4. Remote Backend receives request
   ├─ Processes data
   └─ Returns JSON response

5. Frontend displays results
   └─ User sees data in browser ✅


COMMON MISTAKES & FIXES
═══════════════════════════════════════════════════════════════════════════════

❌ WRONG:
   VITE_API_BASE_URL=http://0.0.0.0:3002
   └─ 0.0.0.0 = "all interfaces" (only works on server itself)
   └─ ERROR: ERR_ADDRESS_INVALID

✅ CORRECT:
   VITE_API_BASE_URL=http://192.168.1.100:3002
   └─ 192.168.1.100 = actual remote server IP
   └─ Works from any computer


FILE LOCATIONS
═══════════════════════════════════════════════════════════════════════════════

LOCAL MACHINE (Your Windows PC)
  d:\SEQUELSTRING\jubilant\
  └─ frontend/
     ├─ .env.local ← UPDATE THIS FILE
     │  VITE_API_BASE_URL=http://[REMOTE_IP]:3002
     ├─ src/
     │  └─ App.tsx
     └─ package.json
        Command: npm run dev


REMOTE SERVER (Desktop\jubilant\jubilant)
  C:\Users\vm_3sc_dev03\Desktop\jubilant\jubilant\
  ├─ server.py ← Backend code
  ├─ database.py
  ├─ models.py
  └─ venv\ ← Virtual environment
     └─ Scripts\activate
        Command: uvicorn server:app --host 0.0.0.0 --port 3002


STEP-BY-STEP SETUP
═══════════════════════════════════════════════════════════════════════════════

REMOTE SERVER TERMINAL:
  $ cd C:\Users\vm_3sc_dev03\Desktop\jubilant\jubilant
  $ venv\Scripts\activate
  $ uvicorn server:app --host 0.0.0.0 --port 3002
  ✅ Server running on 0.0.0.0:3002


LOCAL MACHINE (FIND SERVER IP):
  $ ipconfig
  # Write down Remote Server's IP (e.g., 192.168.1.100)


LOCAL MACHINE (UPDATE ENV):
  Edit: d:\SEQUELSTRING\jubilant\frontend\.env.local
  ─────────────────────────────────────────────
  VITE_API_BASE_URL=http://192.168.1.100:3002
  ─────────────────────────────────────────────


LOCAL MACHINE TERMINAL:
  $ cd d:\SEQUELSTRING\jubilant\frontend
  $ npm run dev
  ✅ Frontend running on http://localhost:3005


BROWSER:
  Open: http://localhost:3005
  Check: Browser Console (F12 → Console tab)
  Look for: ✅ No errors or ✅ API calls succeeding


TESTING THE CONNECTION
═══════════════════════════════════════════════════════════════════════════════

From LOCAL MACHINE PowerShell:
┌─────────────────────────────────────────────────────────────────┐
│ $ curl http://192.168.1.100:3002/                              │
│                                                                 │
│ Response: <html>...</html> or {"status":"running"}             │
│ Result: ✅ CONNECTED!                                          │
│                                                                 │
│ OR use built-in test:                                           │
│ $ .\test-backend-connection.ps1                                │
│ Enter Remote Server IP when prompted                           │
└─────────────────────────────────────────────────────────────────┘


TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════════

Problem: ERR_ADDRESS_INVALID
→ Solution: Use real IP instead of 0.0.0.0

Problem: Connection refused
→ Solution: Check if backend is running on remote server

Problem: Timeout / No response
→ Solution: Check firewall is allowing port 3002

Problem: CORS error
→ Solution: Already configured in server.py ✅

Problem: Wrong data showing
→ Solution: Clear browser cache (Ctrl+Shift+Delete)


SUMMARY
═════════════════════════════════════════════════════════════════════════════

Your Setup:
  ✅ Backend: Remote Server, Port 3002
  ✅ Frontend: Local Machine, Port 3005
  ✅ Communication: Frontend calls Backend via HTTPS/HTTP
  
Fix Required:
  1️⃣ Find Remote Server IP: ipconfig
  2️⃣ Update .env.local: VITE_API_BASE_URL=http://[IP]:3002
  3️⃣ Restart Frontend: npm run dev
  4️⃣ Test: Open http://localhost:3005

Result:
  🎉 Frontend ←→ Backend communication works!

```

---

## **Visual Data Flow**

```
┌───────────┐                                    ┌──────────────┐
│  Browser  │                                    │   Backend    │
│           │  GET /api/process                  │              │
│           │──────────────────────────────────→ │   Python     │
│ localhost │ (via 192.168.1.100:3002)          │   uvicorn    │
│  :3005    │                                    │   Port 3002  │
│           │  ← {"data": "..."}                │              │
│           │←──────────────────────────────────│              │
└───────────┘                                    └──────────────┘
    ↑                                                    ↑
    │                                                    │
 Local PC                                         Remote Server
```

