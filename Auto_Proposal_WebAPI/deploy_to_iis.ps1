# IIS Deployment Script for Auto Proposal WebAPI
# Run this script to prepare the application for IIS deployment
# IMPORTANT: Run PowerShell as Administrator

# Check if running as Administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "ERROR: Administrator Rights Required" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "This script must be run as Administrator to configure IIS." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please:" -ForegroundColor White
    Write-Host "1. Close this PowerShell window" -ForegroundColor Gray
    Write-Host "2. Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Gray
    Write-Host "3. Navigate to: $PSScriptRoot" -ForegroundColor Gray
    Write-Host "4. Run: .\deploy_to_iis.ps1" -ForegroundColor Gray
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Auto Proposal WebAPI - IIS Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python installation
Write-Host "Step 1: Checking Python installation..." -ForegroundColor Yellow
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if ($pythonPath) {
    Write-Host "[OK] Python found at: $pythonPath" -ForegroundColor Green
    $pythonVersion = python --version
    Write-Host "  Version: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Python not found! Please install Python 3.9 or higher" -ForegroundColor Red
    exit 1
}

# Step 2: Install required packages
Write-Host ""
Write-Host "Step 2: Installing required packages..." -ForegroundColor Yellow
Write-Host "  Installing wfastcgi (FastCGI for IIS)..." -ForegroundColor Gray
pip install wfastcgi asgiref --quiet

Write-Host "  Installing application dependencies..." -ForegroundColor Gray
pip install -r requirements.txt --quiet

Write-Host "[OK] Packages installed successfully" -ForegroundColor Green

# Step 3: Enable wfastcgi in IIS
Write-Host ""
Write-Host "Step 3: Enabling wfastcgi in IIS..." -ForegroundColor Yellow
Write-Host "  Running wfastcgi-enable..." -ForegroundColor Gray
$wfastcgiOutput = wfastcgi-enable 2>&1
Write-Host "[OK] wfastcgi enabled" -ForegroundColor Green
Write-Host "  $wfastcgiOutput" -ForegroundColor Gray

# Step 4: Update web.config with actual Python path
Write-Host ""
Write-Host "Step 4: Updating web.config with Python path..." -ForegroundColor Yellow
$pythonDir = Split-Path -Parent $pythonPath
$wfastcgiPath = Join-Path $pythonDir "Lib\site-packages\wfastcgi.py"

if (Test-Path $wfastcgiPath) {
    Write-Host "[OK] wfastcgi.py found at: $wfastcgiPath" -ForegroundColor Green
    
    # Read web.config
    $webConfigPath = ".\web.config"
    $webConfig = Get-Content $webConfigPath -Raw
    
    # Update Python paths
    $webConfig = $webConfig -replace 'C:\\Python311\\python\.exe', $pythonPath
    $webConfig = $webConfig -replace 'C:\\Python311\\Lib\\site-packages\\wfastcgi\.py', $wfastcgiPath
    
    # Update project path
    $projectPath = (Get-Location).Path
    $webConfig = $webConfig -replace 'D:\\PSE\\Projects\\Auto\\Coding\\Auto_Proposal_WebAPI', $projectPath
    
    # Save updated web.config
    $webConfig | Set-Content $webConfigPath -NoNewline
    
    Write-Host "[OK] web.config updated with correct paths" -ForegroundColor Green
} else {
    Write-Host "[ERROR] wfastcgi.py not found! Please reinstall wfastcgi" -ForegroundColor Red
    exit 1
}

# Step 5: Create logs directory
Write-Host ""
Write-Host "Step 5: Creating logs directory..." -ForegroundColor Yellow
if (-not (Test-Path ".\logs")) {
    New-Item -ItemType Directory -Path ".\logs" | Out-Null
    Write-Host "[OK] Logs directory created" -ForegroundColor Green
} else {
    Write-Host "[OK] Logs directory already exists" -ForegroundColor Green
}

# Step 6: Create pdf_files directory if not exists
Write-Host ""
Write-Host "Step 6: Checking pdf_files directory..." -ForegroundColor Yellow
if (-not (Test-Path ".\pdf_files")) {
    New-Item -ItemType Directory -Path ".\pdf_files" | Out-Null
    Write-Host "[OK] pdf_files directory created" -ForegroundColor Green
} else {
    Write-Host "[OK] pdf_files directory already exists" -ForegroundColor Green
}

# Step 7: Test the application locally
Write-Host ""
Write-Host "Step 7: Testing application..." -ForegroundColor Yellow
Write-Host "  Running quick test..." -ForegroundColor Gray
python -c "from src.auto_proposal.api.main import app; print('[OK] Application imports successfully')"

# Display summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deployment Preparation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Project Path: $projectPath" -ForegroundColor White
Write-Host "Python Path: $pythonPath" -ForegroundColor White
Write-Host "wfastcgi Path: $wfastcgiPath" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Open IIS Manager (run 'inetmgr')" -ForegroundColor White
Write-Host "2. Create a new Application Pool:" -ForegroundColor White
Write-Host "   - Name: AutoProposalAPI" -ForegroundColor Gray
Write-Host "   - .NET CLR Version: No Managed Code" -ForegroundColor Gray
Write-Host "3. Create a new Website:" -ForegroundColor White
Write-Host "   - Site name: AutoProposalAPI" -ForegroundColor Gray
Write-Host "   - Physical path: $projectPath" -ForegroundColor Gray
Write-Host "   - Application pool: AutoProposalAPI" -ForegroundColor Gray
Write-Host "   - Binding: http, Port: 8000 (or your preferred port)" -ForegroundColor Gray
Write-Host "4. Set folder permissions:" -ForegroundColor White
Write-Host "   - Right-click on site -> Edit Permissions -> Security" -ForegroundColor Gray
Write-Host "   - Add 'IIS AppPool\AutoProposalAPI' with Modify permissions" -ForegroundColor Gray
Write-Host "5. Start the website in IIS Manager" -ForegroundColor White
Write-Host "6. Test: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see IIS_DEPLOYMENT_GUIDE.md" -ForegroundColor Cyan
