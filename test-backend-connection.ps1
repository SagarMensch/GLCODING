# Test Backend Connection Script
# Run this on your LOCAL MACHINE to verify backend is reachable

$remoteServerIP = Read-Host "Enter Remote Server IP (e.g., 192.168.1.100 or agentic-gl.sequelstring.com)"
$port = "3002"
$url = "http://$($remoteServerIP):$($port)"

Write-Host "🔍 Testing connection to: $url" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Test 1: Ping
Write-Host "`n[1] Testing Ping..." -ForegroundColor Yellow
try {
    if (Test-Connection -ComputerName $remoteServerIP -Count 1 -Quiet) {
        Write-Host "✅ Ping successful - Server is reachable" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Ping failed - Server might be blocking ICMP" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Ping error: $_" -ForegroundColor Red
}

# Test 2: Port connectivity
Write-Host "`n[2] Testing Port $port..." -ForegroundColor Yellow
try {
    $tcpClient = New-Object System.Net.Sockets.TcpClient
    $tcpClient.Connect($remoteServerIP, $port)
    if ($tcpClient.Connected) {
        Write-Host "✅ Port $port is open and listening" -ForegroundColor Green
    }
    $tcpClient.Close()
} catch {
    Write-Host "❌ Port $port is not reachable: $_" -ForegroundColor Red
}

# Test 3: HTTP Request
Write-Host "`n[3] Testing HTTP Request to $url..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ Backend is responding!" -ForegroundColor Green
    Write-Host "Status Code: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "Response Preview:" -ForegroundColor Green
    Write-Host $response.Content.Substring(0, [Math]::Min(200, $response.Content.Length)) -ForegroundColor Green
} catch {
    Write-Host "❌ HTTP request failed: $_" -ForegroundColor Red
    Write-Host "This might mean backend is not running or port is blocked" -ForegroundColor Yellow
}

# Test 4: Suggest correct configuration
Write-Host "`n[4] Suggested Configuration" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Update your frontend/.env.local:" -ForegroundColor Yellow
Write-Host "VITE_API_BASE_URL=http://$($remoteServerIP):$($port)" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Test 5: Firewall check (Windows)
Write-Host "`n[5] Checking Local Firewall..." -ForegroundColor Yellow
try {
    $firewallRule = Get-NetFirewallRule -DisplayName "*$port*" -ErrorAction SilentlyContinue
    if ($firewallRule) {
        Write-Host "✅ Port $port is allowed in Windows Firewall" -ForegroundColor Green
    } else {
        Write-Host "⚠️  No firewall rule found for port $port on local machine" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Could not check firewall: $_" -ForegroundColor Yellow
}

Write-Host "`nℹ️  Next Steps:" -ForegroundColor Cyan
Write-Host "1. If tests pass → Update frontend/.env.local with the URL above" -ForegroundColor White
Write-Host "2. Restart frontend: npm run dev" -ForegroundColor White
Write-Host "3. Open browser: http://localhost:3005" -ForegroundColor White
Write-Host "4. Check browser console (F12) for any errors" -ForegroundColor White
