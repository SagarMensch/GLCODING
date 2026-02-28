# 🎯 QUICK FIX - Your Error & Solution

## **Your Error Summary**
```
ERR_ADDRESS_INVALID
http://0.0.0.0:3002
```

**Why it fails:** `0.0.0.0` is only valid on the **server itself**, not for remote access.

---

## **⚡ 3-Step Quick Fix**

### **STEP 1: Find Remote Server IP**
Run on the remote server where backend is running:

**Windows Remote Server:**
```powershell
ipconfig
# Find: IPv4 Address: 192.168.1.100 (or similar)
```

**Linux Remote Server:**
```bash
hostname -I
# Output: 192.168.1.100
```

### **STEP 2: Update Frontend .env File**

**File:** `frontend/.env.local`

```properties
# OLD (WRONG - doesn't work):
VITE_API_BASE_URL=http://0.0.0.0:3002

# NEW (CORRECT - use real IP):
VITE_API_BASE_URL=http://192.168.1.100:3002

# OR use hostname if available:
VITE_API_BASE_URL=http://agentic-gl.sequelstring.com:3002
```

### **STEP 3: Restart Frontend**

```powershell
# In your local machine's frontend folder
npm run dev
```

---

## **📊 What's Running Where**

| Component | Location | Command | Access From |
|-----------|----------|---------|-------------|
| **Backend** | Remote Server | `uvicorn server:app --host 0.0.0.0 --port 3002` | `http://REMOTE_IP:3002` |
| **Frontend** | Local Machine | `npm run dev` (port 3005) | `http://localhost:3005` |
| **Frontend calls Backend** | Local → Remote | API requests | Uses `VITE_API_BASE_URL` |

---

## **🧪 Test It Immediately**

### **Option 1: PowerShell Test (Easy)**
```powershell
# Open PowerShell on your LOCAL MACHINE and run:
.\test-backend-connection.ps1
# When prompted, enter your remote server IP
```

### **Option 2: Manual Test**
```powershell
# Replace 192.168.1.100 with your actual remote IP
curl http://192.168.1.100:3002/

# If you see HTML/JSON response → ✅ Backend is reachable
# If you see error → ❌ Check firewall or IP
```

---

## **📋 Checklist**

- [ ] **Remote Server**: Backend running with `uvicorn server:app --host 0.0.0.0 --port 3002`
- [ ] **Find Remote IP**: Run `ipconfig` (Windows) or `hostname -I` (Linux) on remote server
- [ ] **Update .env**: Change `frontend/.env.local` to use real IP
- [ ] **Restart Frontend**: Run `npm run dev` on local machine
- [ ] **Test**: Open `http://localhost:3005` in browser
- [ ] **Check Console**: Press F12, look at Network tab for API calls

---

## **🚨 If Still Getting Error**

### **Check 1: Is Backend Running?**
```powershell
# On remote server
netstat -ano | grep 3002
# Should show LISTENING
```

### **Check 2: Is Firewall Blocking?**
**Windows Remote Server:**
```powershell
# Allow port 3002
netsh advfirewall firewall add rule name="Allow 3002" dir=in action=allow protocol=tcp localport=3002
```

**Linux Remote Server:**
```bash
sudo ufw allow 3002/tcp
```

### **Check 3: Verify Correct IP**
```powershell
# Test from LOCAL machine:
Test-NetConnection -ComputerName 192.168.1.100 -Port 3002
# Should show: TcpTestSucceeded: True
```

---

## **💡 Pro Tips**

1. **Save Remote IP** - Write it down for future use
2. **Use Hostname** - If you have DNS like `agentic-gl.sequelstring.com`, use that instead of IP
3. **HTTPS Later** - Once working, switch to HTTPS for production
4. **Check Logs** - Backend logs show which IP is connecting

---

## **📚 Files Created to Help**

| File | Purpose |
|------|---------|
| `frontend/.env.local` | Your local dev configuration |
| `test-backend-connection.ps1` | PowerShell script to test connection |
| `FIX_ERROR_QUICK_GUIDE.md` | Detailed troubleshooting guide |

---

## **Example: Fully Working Setup**

### **Remote Server (Windows, IP: 192.168.1.100)**
```powershell
C:\Users\vm_3sc_dev03\Desktop\jubilant\jubilant> uvicorn server:app --host 0.0.0.0 --port 3002
INFO: Uvicorn running on http://0.0.0.0:3002
✅ Backend is running and listening
```

### **Local Machine (Your PC)**

**frontend/.env.local:**
```properties
VITE_API_BASE_URL=http://192.168.1.100:3002
```

**Terminal:**
```powershell
npm run dev
➜ Local: http://localhost:3005/
✅ Frontend is running
```

**Browser:** 
- Visit `http://localhost:3005`
- Frontend makes API calls to `http://192.168.1.100:3002` ✅
- **No more error!**

---

**Got it working? 🎉 Continue building!**
