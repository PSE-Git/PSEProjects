# PowerShell script to test the Login API

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   Login API Test Script" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

$baseUrl = "http://localhost:8000/api/auth"

# Test 1: Set password for user
Write-Host "`n1. Setting password for user..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/set-password/1?password=Test@123" `
        -Method POST `
        -ErrorAction Stop
    $result = $response.Content | ConvertFrom-Json
    Write-Host "   ✓ Success: $($result.message)" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Valid login
Write-Host "`n2. Testing VALID login..." -ForegroundColor Yellow
$loginData = @{
    company_name = "Sky Interiors"
    email = "bagavath@pseconsulting.in"
    password = "Test@123"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/login" `
        -Method POST `
        -ContentType "application/json" `
        -Body $loginData `
        -ErrorAction Stop
    $result = $response.Content | ConvertFrom-Json
    Write-Host "   ✓ Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "   ✓ Message: $($result.message)" -ForegroundColor Green
    Write-Host "   ✓ User: $($result.user.full_name)" -ForegroundColor Green
    Write-Host "   ✓ Role: $($result.user.role)" -ForegroundColor Green
    Write-Host "   ✓ Access Granted: $($result.access_granted)" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Invalid company
Write-Host "`n3. Testing INVALID company..." -ForegroundColor Yellow
$loginData = @{
    company_name = "Wrong Company"
    email = "bagavath@pseconsulting.in"
    password = "Test@123"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/login" `
        -Method POST `
        -ContentType "application/json" `
        -Body $loginData `
        -ErrorAction Stop
} catch {
    $errorResponse = $_.ErrorDetails.Message | ConvertFrom-Json
    Write-Host "   ✓ Status: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Green
    Write-Host "   ✓ Error: $($errorResponse.detail.message)" -ForegroundColor Green
    Write-Host "   ✓ Code: $($errorResponse.detail.error_code)" -ForegroundColor Green
}

# Test 4: Invalid password
Write-Host "`n4. Testing INVALID password..." -ForegroundColor Yellow
$loginData = @{
    company_name = "Sky Interiors"
    email = "bagavath@pseconsulting.in"
    password = "WrongPassword"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/login" `
        -Method POST `
        -ContentType "application/json" `
        -Body $loginData `
        -ErrorAction Stop
} catch {
    $errorResponse = $_.ErrorDetails.Message | ConvertFrom-Json
    Write-Host "   ✓ Status: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Green
    Write-Host "   ✓ Error: $($errorResponse.detail.message)" -ForegroundColor Green
    Write-Host "   ✓ Code: $($errorResponse.detail.error_code)" -ForegroundColor Green
}

# Test 5: Invalid email
Write-Host "`n5. Testing INVALID email..." -ForegroundColor Yellow
$loginData = @{
    company_name = "Sky Interiors"
    email = "nonexistent@example.com"
    password = "Test@123"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/login" `
        -Method POST `
        -ContentType "application/json" `
        -Body $loginData `
        -ErrorAction Stop
} catch {
    $errorResponse = $_.ErrorDetails.Message | ConvertFrom-Json
    Write-Host "   ✓ Status: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Green
    Write-Host "   ✓ Error: $($errorResponse.detail.message)" -ForegroundColor Green
    Write-Host "   ✓ Code: $($errorResponse.detail.error_code)" -ForegroundColor Green
}

Write-Host "`n=============================================" -ForegroundColor Cyan
Write-Host "   All Tests Complete!" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "`nAPI Documentation: http://localhost:8000/docs" -ForegroundColor Magenta
