# 🚀 Complete Guide: Running Backend on Remote Server & Accessing from Local Machine

## **Architecture Overview**
```
Local Machine (Windows)          Remote Server (Linux/Windows)
├─ Frontend (port 3005)    ──────→  Backend (port 3002)
├─ Browser                        │
└─ API Calls                       └─ https://agentic-gl.sequelstring.com:3002
```

---

## **OPTION 1: Run Backend on Remote Server (Recommended)**
 
### **Step 1: Connect to Remote Server via SSH**
```bash
# On Local Windows PowerShell (using SSH)
ssh user@agentic-gl.sequelstring.com
# or if using custom port
ssh -p 22 user@agentic-gl.sequelstring.com
```

### **Step 2: Clone or Upload Your Code to Remote Server**
```bash
# Option A: Clone from Git
git clone <your-repo-url> /home/user/jubilant
cd /home/user/jubilant

# Option B: Use SCP to upload files
scp -r d:\SEQUELSTRING\jubilant user@agentic-gl.sequelstring.com:/home/user/
```

### **Step 3: Install Python Dependencies on Remote Server**
```bash
# Navigate to project directory
cd /home/user/jubilant

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or on Windows Remote:
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
# If no requirements.txt exists, install manually:
pip install fastapi uvicorn sqlalchemy supabase pandas numpy scikit-learn
```

### **Step 4: Run Backend on Remote Server (Production)**

**Option A: Simple Command**
```bash
python server.py
# Output: Server: http://0.0.0.0:3002
```

**Option B: Using Uvicorn Directly (Better)**
```bash
uvicorn server:app --host 0.0.0.0 --port 3002 --reload
# For production without reload:
uvicorn server:app --host 0.0.0.0 --port 3002
```

**Option C: Run in Background with Nohup (Linux)**
```bash
# Start and keep running even after SSH disconnect
nohup python -u server.py > server.log 2>&1 &

# Check if running
ps aux | grep server.py

# View logs
tail -f server.log

# Stop the process
pkill -f server.py
```

**Option D: Use Screen or Tmux (Linux)**
```bash
# Using Screen
screen -S backend
python server.py
# Detach: Ctrl+A then D
# Reattach: screen -r backend
# Kill: screen -X -S backend quit

# Using Tmux
tmux new-session -d -s backend -c /home/user/jubilant
tmux send-keys -t backend "python server.py" Enter
tmux ls
tmux kill-session -t backend
```

### **Step 5: Configure Firewall & Open Port 3002**

```bash
# For Linux with UFW
sudo ufw allow 3002/tcp
sudo ufw status

# For Linux with iptables
sudo iptables -A INPUT -p tcp --dport 3002 -j ACCEPT
sudo iptables-save

# For Windows Remote Server
netsh advfirewall firewall add rule name="Backend 3002" dir=in action=allow protocol=tcp localport=3002
```

---

## **OPTION 2: Run Backend Locally & Access from Remote**

### **Windows PowerShell Commands:**

```powershell
# Navigate to project
cd d:\SEQUELSTRING\jubilant\jubilant

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install fastapi uvicorn sqlalchemy supabase pandas numpy scikit-learn

# Run backend (localhost)
python server.py

# Or use Uvicorn directly
uvicorn server:app --host 0.0.0.0 --port 3002 --reload
```

### **Then Access from Remote:**
Your local machine backend becomes accessible to remote machines via:
```
http://<YOUR_LOCAL_IP>:3002
# Example: http://192.168.1.100:3002
```

To find your local IP:
```powershell
ipconfig
# Look for "IPv4 Address"
```

---

## **OPTION 3: Use Docker (Production-Ready)**

### **Create Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir \
    fastapi uvicorn sqlalchemy supabase pandas numpy scikit-learn

EXPOSE 3002

CMD ["python", "server.py"]
```

### **Run with Docker**
```bash
# Build image
docker build -t jubilant-backend .

# Run container
docker run -d -p 3002:3002 --name jubilant-backend jubilant-backend

# View logs
docker logs jubilant-backend

# Stop container
docker stop jubilant-backend
```

---

## **OPTION 4: Deploy Using PM2 (Node-based Process Manager)**

### **Install PM2**
```bash
npm install -g pm2
```

### **Create PM2 Config (ecosystem.config.js)**
```javascript
module.exports = {
  apps: [{
    name: 'jubilant-backend',
    script: 'server.py',
    interpreter: 'python',
    instances: 1,
    exec_mode: 'fork',
    env: {
      'NODE_ENV': 'production'
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
  }]
};
```

### **Start with PM2**
```bash
pm2 start ecosystem.config.js
pm2 status
pm2 logs jubilant-backend
```

---

## **LOCAL MACHINE: Configure Frontend to Use Remote Backend**

### **1. Update .env files**
```env
# .env
VITE_API_BASE_URL=https://agentic-gl.sequelstring.com:3002

# Or if local:
VITE_API_BASE_URL=http://localhost:3002
```

### **2. Update vite.config.ts**
```typescript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3005,
    proxy: {
      '/api': {
        target: 'https://agentic-gl.sequelstring.com:3002',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        secure: false
      }
    }
  }
})
```

### **3. Run Frontend Locally**
```powershell
cd d:\SEQUELSTRING\jubilant\jubilant\frontend
npm install
npm run dev
# Output: Local: http://localhost:3005
```

### **4. Access Frontend**
- Open browser: `http://localhost:3005`
- Frontend automatically calls backend at `https://agentic-gl.sequelstring.com:3002`

---

## **Testing Connection**

### **From Windows PowerShell (Local)**
```powershell
# Test if backend is accessible
curl https://agentic-gl.sequelstring.com:3002/health
# or
Invoke-WebRequest -Uri https://agentic-gl.sequelstring.com:3002/health
```

### **From Remote Server**
```bash
curl http://localhost:3002/health
# or
curl https://agentic-gl.sequelstring.com:3002/health
```

---

## **Troubleshooting**

| Issue | Solution |
|-------|----------|
| **Connection Refused** | Check if port 3002 is open: `netstat -an \| findstr :3002` |
| **SSL Certificate Error** | Use `http://` instead of `https://` or add cert exceptions |
| **CORS Error** | Already configured in server.py (allow_origins=["*"]) |
| **Process Won't Stop** | `pkill -f server.py` or `taskkill /IM python.exe` |
| **Port Already in Use** | Change port: `uvicorn server:app --port 3003` |

---

## **Summary: Quick Start Commands**

### **Remote Server (Linux)**
```bash
ssh user@agentic-gl.sequelstring.com
cd /home/user/jubilant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
nohup python server.py > server.log 2>&1 &
```

### **Local Machine (Windows)**
```powershell
cd d:\SEQUELSTRING\jubilant\jubilant\frontend
npm install
npm run dev
# Now visit http://localhost:3005
```

