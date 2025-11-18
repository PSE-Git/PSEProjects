# Install IIS Features Required for Python/FastAPI
# Run this script as Administrator

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installing IIS Features for Python" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[ERROR] This script must be run as Administrator" -ForegroundColor Red
    Write-Host "Please right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Installing IIS Web Server Role..." -ForegroundColor Yellow
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole -All -NoRestart

Write-Host "Installing IIS Management Console..." -ForegroundColor Yellow
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ManagementConsole -All -NoRestart

Write-Host "Installing CGI support..." -ForegroundColor Yellow
Enable-WindowsOptionalFeature -Online -FeatureName IIS-CGI -All -NoRestart

Write-Host "Installing ISAPI Extensions..." -ForegroundColor Yellow
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ISAPIExtensions -All -NoRestart

Write-Host "Installing ISAPI Filters..." -ForegroundColor Yellow
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ISAPIFilter -All -NoRestart

Write-Host "Installing Application Development features..." -ForegroundColor Yellow
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ApplicationDevelopment -All -NoRestart

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "IIS Features Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Restart your computer (recommended) or run: iisreset" -ForegroundColor White
Write-Host "2. Run: .\deploy_to_iis.ps1" -ForegroundColor White
Write-Host ""

$restart = Read-Host "Do you want to restart IIS now? (y/n)"
if ($restart -eq "y" -or $restart -eq "Y") {
    Write-Host "Restarting IIS..." -ForegroundColor Yellow
    iisreset
    Write-Host "[OK] IIS restarted successfully" -ForegroundColor Green
}
