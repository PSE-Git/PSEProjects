# Simple Deployment - Run FastAPI with Uvicorn
# This script sets up the API to run directly with Uvicorn (no IIS complexity)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FastAPI Simple Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get the local IP address
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*"}).IPAddress
Write-Host "Local IP Address: $localIP" -ForegroundColor Green
Write-Host ""

Write-Host "Starting FastAPI server..." -ForegroundColor Yellow
Write-Host "The server will be accessible at:" -ForegroundColor White
Write-Host "  - http://localhost:8000" -ForegroundColor Cyan
Write-Host "  - http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "  - http://${localIP}:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "API Documentation will be at:" -ForegroundColor White
Write-Host "  - http://${localIP}:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run uvicorn with host binding to allow external access
python -m uvicorn src.auto_proposal.api.main:app --host 0.0.0.0 --port 8000 --reload
