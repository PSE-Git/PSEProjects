# Login API - User Guide

## 🎯 Login Endpoint

**Endpoint:** `POST /api/auth/login`

**Base URL:** `http://localhost:8000`

---

## 📝 Request Format

### Request Body (JSON)
```json
{
  "company_name": "Sky Interiors",
  "email": "bagavath@pseconsulting.in",
  "password": "your_password"
}
```

### Field Validation
- **company_name**: Required, 1-150 characters
- **email**: Required, must be valid email format
- **password**: Required, minimum 1 character

---

## ✅ Success Response (200 OK)

```json
{
  "success": true,
  "message": "Login successful",
  "access_granted": true,
  "access_end_date": "2025-12-31T00:00:00",
  "user": {
    "id": 1,
    "email": "bagavath@pseconsulting.in",
    "full_name": "Bagavath Lakshmanan",
    "designation": "Project Manager",
    "phone": "9789912323",
    "role": "Admin",
    "is_active": true,
    "company_id": 1,
    "auto_proposal_access_end_date": "2025-12-31T00:00:00",
    "created_at": "2025-11-04T17:51:19",
    "updated_at": "2025-11-04T17:51:19",
    "company": {
      "id": 1,
      "company_name": "Sky Interiors",
      "industry_type": "Interior Design",
      "email": "info@skyinteriors.in",
      ...
    }
  }
}
```

---

## ❌ Error Responses

### 1. Invalid Company (404 NOT FOUND)
```json
{
  "detail": {
    "success": false,
    "message": "Company 'Wrong Company' not found",
    "error_code": "INVALID_COMPANY"
  }
}
```

### 2. Invalid User/Email (404 NOT FOUND)
```json
{
  "detail": {
    "success": false,
    "message": "User with email 'wrong@email.com' not found",
    "error_code": "INVALID_USER"
  }
}
```

### 3. Company Mismatch (403 FORBIDDEN)
```json
{
  "detail": {
    "success": false,
    "message": "User does not belong to company 'Sky Interiors'",
    "error_code": "COMPANY_MISMATCH"
  }
}
```

### 4. Invalid Password (401 UNAUTHORIZED)
```json
{
  "detail": {
    "success": false,
    "message": "Invalid password",
    "error_code": "INVALID_PASSWORD"
  }
}
```

### 5. Account Inactive (403 FORBIDDEN)
```json
{
  "detail": {
    "success": false,
    "message": "User account is deactivated. Please contact administrator.",
    "error_code": "ACCOUNT_INACTIVE"
  }
}
```

### 6. Access Expired (403 FORBIDDEN)
```json
{
  "detail": {
    "success": false,
    "message": "Access expired on 2025-01-01. Please renew subscription.",
    "error_code": "ACCESS_EXPIRED"
  }
}
```

### 7. Validation Error (422 UNPROCESSABLE ENTITY)
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "password"],
      "msg": "Field required"
    }
  ]
}
```

---

## 🧪 Testing Examples

### Using cURL (PowerShell)
```powershell
# Valid login
$body = @{
    company_name = "Sky Interiors"
    email = "bagavath@pseconsulting.in"
    password = "your_password"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/auth/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### Using Python
```python
import requests

url = "http://localhost:8000/api/auth/login"
data = {
    "company_name": "Sky Interiors",
    "email": "bagavath@pseconsulting.in",
    "password": "your_password"
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
```

### Using Postman
1. Method: POST
2. URL: `http://localhost:8000/api/auth/login`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "company_name": "Sky Interiors",
  "email": "bagavath@pseconsulting.in",
  "password": "your_password"
}
```

---

## 🔐 Set Password Endpoint (Admin/Testing)

**Endpoint:** `POST /api/auth/set-password/{user_id}`

**Query Parameter:** `password` (string)

**Example:**
```
POST /api/auth/set-password/1?password=NewPassword123
```

**Response:**
```json
{
  "success": true,
  "message": "Password set successfully for user bagavath@pseconsulting.in"
}
```

---

## 📊 Validation Logic Flow

1. ✅ Validate company exists (by company_name)
2. ✅ Validate user exists (by email)
3. ✅ Validate user belongs to company
4. ✅ Validate password is correct
5. ✅ Validate user account is active
6. ✅ Validate access hasn't expired
7. ✅ Grant access and return user details with company info

---

## 🌐 Interactive API Documentation

Visit: `http://localhost:8000/docs`

The Swagger UI provides:
- Interactive testing interface
- Complete API documentation
- Request/Response examples
- Try it out functionality

---

## 📌 Notes

- All passwords are hashed using bcrypt for security
- Access dates are checked against current date
- Users get warned if access expires within 7 days
- Company matching is case-sensitive
- Email matching is case-sensitive

