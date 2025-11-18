# Email Configuration Setup Script
# Run this script to set environment variables for email functionality

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Email Configuration Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "For Gmail, you need to:" -ForegroundColor Yellow
Write-Host "1. Enable 2-Factor Authentication on your Google Account" -ForegroundColor Yellow
Write-Host "2. Generate an App Password: https://myaccount.google.com/apppasswords" -ForegroundColor Yellow
Write-Host "3. Use the App Password (not your regular password)" -ForegroundColor Yellow
Write-Host ""

# Prompt for email configuration
$senderEmail = Read-Host "Enter your email address (e.g., youremail@gmail.com)"
$senderPassword = Read-Host "Enter your email app password" -AsSecureString
$senderPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($senderPassword))

# Set environment variables for current session
$env:SENDER_EMAIL = $senderEmail
$env:SENDER_PASSWORD = $senderPasswordPlain
$env:SMTP_SERVER = "smtp.gmail.com"
$env:SMTP_PORT = "587"

Write-Host ""
Write-Host "✓ Environment variables set for current session!" -ForegroundColor Green
Write-Host ""
Write-Host "Note: These variables are only set for the current PowerShell session." -ForegroundColor Yellow
Write-Host "To make them permanent, you can:" -ForegroundColor Yellow
Write-Host "1. Add them to your system environment variables, OR" -ForegroundColor Yellow
Write-Host "2. Run this script each time before starting the Flask app" -ForegroundColor Yellow
Write-Host ""
Write-Host "Current values:" -ForegroundColor Cyan
Write-Host "  SENDER_EMAIL: $senderEmail" -ForegroundColor Gray
Write-Host "  SMTP_SERVER: smtp.gmail.com" -ForegroundColor Gray
Write-Host "  SMTP_PORT: 587" -ForegroundColor Gray
Write-Host ""
Write-Host "You can now start your Flask app with: python app.py" -ForegroundColor Green
