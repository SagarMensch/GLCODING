import subprocess
import sys

# Start server in background
proc = subprocess.Popen(
    [sys.executable, "server.py"],
    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

print(f"Server started with PID: {proc.pid}")
print("Visit http://localhost:3005")
