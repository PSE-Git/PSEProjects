# Troubleshoot connectivity issues
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Network Troubleshooting" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if port 8000 is in use
Write-Host "Checking if port 8000 is in use..." -ForegroundColor Yellow
$port8000 = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($port8000) {
    Write-Host "[OK] Port 8000 is in use by:" -ForegroundColor Green
    $port8000 | ForEach-Object {
        $processId = $_.OwningProcess
        $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
        Write-Host "  Process: $($process.ProcessName) (PID: $processId)" -ForegroundColor White
        Write-Host "  State: $($_.State)" -ForegroundColor White
        Write-Host "  Local Address: $($_.LocalAddress):$($_.LocalPort)" -ForegroundColor White
    }
} else {
    Write-Host "[WARNING] Port 8000 is NOT in use - no server is running!" -ForegroundColor Red
    Write-Host "You need to start the server first using: .\run_server.ps1" -ForegroundColor Yellow
}

Write-Host ""

# Check Windows Firewall rules for port 8000
Write-Host "Checking Windows Firewall rules for port 8000..." -ForegroundColor Yellow
$firewallRule = Get-NetFirewallRule -DisplayName "*8000*" -ErrorAction SilentlyContinue
if ($firewallRule) {
    Write-Host "[OK] Firewall rule exists for port 8000" -ForegroundColor Green
    $firewallRule | ForEach-Object {
        Write-Host "  Rule: $($_.DisplayName)" -ForegroundColor White
        Write-Host "  Enabled: $($_.Enabled)" -ForegroundColor White
    }
} else {
    Write-Host "[WARNING] No firewall rule found for port 8000" -ForegroundColor Yellow
    Write-Host "Creating firewall rule..." -ForegroundColor Yellow
    
    # Try to create firewall rule (requires admin)
    try {
        New-NetFirewallRule -DisplayName "FastAPI Port 8000" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow -ErrorAction Stop
        Write-Host "[OK] Firewall rule created successfully" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Failed to create firewall rule. Run PowerShell as Administrator and execute:" -ForegroundColor Red
        Write-Host "  New-NetFirewallRule -DisplayName 'FastAPI Port 8000' -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow" -ForegroundColor Yellow
    }
}

Write-Host ""

# Get network adapter info
Write-Host "Network Adapters:" -ForegroundColor Yellow
Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notlike "169.254.*" -and $_.IPAddress -ne "127.0.0.1"} | ForEach-Object {
    Write-Host "  IP: $($_.IPAddress)" -ForegroundColor White
    Write-Host "  Interface: $($_.InterfaceAlias)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. If server is not running, start it with: .\run_server.ps1" -ForegroundColor White
Write-Host "2. If firewall rule creation failed, run PowerShell as Administrator" -ForegroundColor White
Write-Host "3. Test access from browser: http://192.168.1.4:8000/docs" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
