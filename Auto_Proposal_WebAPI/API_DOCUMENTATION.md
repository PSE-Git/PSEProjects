# Auto Proposal API - Users and Companies Documentation

## Overview
Complete CRUD (Create, Read, Update, Delete) APIs for UserDetails and CompanyDetails tables.

## ✅ What Has Been Created

### 1. Database Models
- **UserDetails** (`src/auto_proposal/core/models.py`)
  - Fields: id, username, email, full_name, password_hash, phone, role, is_active, company_id
  - Relationship with CompanyDetails (Many-to-One)

- **CompanyDetails** (`src/auto_proposal/core/models.py`)
  - Fields: id, company_name, company_email, company_phone, address, city, state, country, postal_code, website, tax_id, industry, description, is_active
  - Relationship with UserDetails (One-to-Many)

### 2. Pydantic Schemas
Created in `src/auto_proposal/core/schemas.py`:
- UserDetailsBase, UserDetailsCreate, UserDetailsUpdate, UserDetailsResponse, UserDetailsWithCompany
- CompanyDetailsBase, CompanyDetailsCreate, CompanyDetailsUpdate, CompanyDetailsResponse, CompanyDetailsWithUsers

### 3. API Routes

#### Users API (`/api/users/`)
- **POST** `/api/users/` - Create a new user
- **GET** `/api/users/` - Get all users (with filters: skip, limit, is_active, role)
- **GET** `/api/users/{user_id}` - Get user by ID (includes company details)
- **GET** `/api/users/username/{username}` - Get user by username
- **PUT** `/api/users/{user_id}` - Update user
- **DELETE** `/api/users/{user_id}` - Delete user
- **PATCH** `/api/users/{user_id}/activate` - Activate user
- **PATCH** `/api/users/{user_id}/deactivate` - Deactivate user

#### Companies API (`/api/companies/`)
- **POST** `/api/companies/` - Create a new company
- **GET** `/api/companies/` - Get all companies (with filters: skip, limit, is_active, industry, city)
- **GET** `/api/companies/{company_id}` - Get company by ID (includes users)
- **GET** `/api/companies/{company_id}/users` - Get all users of a company
- **GET** `/api/companies/search/name/{name}` - Search companies by name
- **PUT** `/api/companies/{company_id}` - Update company
- **DELETE** `/api/companies/{company_id}` - Delete company (only if no users)
- **PATCH** `/api/companies/{company_id}/activate` - Activate company
- **PATCH** `/api/companies/{company_id}/deactivate` - Deactivate company

## 📝 API Examples

### Create User
```bash
POST http://localhost:8000/api/users/
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john.doe@example.com",
  "full_name": "John Doe",
  "password": "securepassword123",
  "phone": "+1234567890",
  "role": "user",
  "is_active": true,
  "company_id": 1
}
```

### Create Company
```bash
POST http://localhost:8000/api/companies/
Content-Type: application/json

{
  "company_name": "Tech Solutions Inc",
  "company_email": "info@techsolutions.com",
  "company_phone": "+1234567890",
  "address": "123 Main Street",
  "city": "New York",
  "state": "NY",
  "country": "USA",
  "postal_code": "10001",
  "website": "https://techsolutions.com",
  "tax_id": "12-3456789",
  "industry": "Technology",
  "description": "Leading technology solutions provider",
  "is_active": true
}
```

### Get All Users (with filters)
```bash
GET http://localhost:8000/api/users/?skip=0&limit=100&is_active=true&role=user
```

### Get User with Company Details
```bash
GET http://localhost:8000/api/users/1
```

### Update User
```bash
PUT http://localhost:8000/api/users/1
Content-Type: application/json

{
  "email": "john.updated@example.com",
  "full_name": "John Doe Updated",
  "role": "admin"
}
```

### Get Company with All Users
```bash
GET http://localhost:8000/api/companies/1
```

### Search Companies
```bash
GET http://localhost:8000/api/companies/search/name/Tech
```

## 🚀 Running the API

### Step 1: Configure Database
Edit `.env` file with your Google Cloud SQL credentials:
```env
DATABASE_URL=mysql+pymysql://username:password@34.100.231.86:3306/auto_proposal_db
```

### Step 2: Authorize Your IP in Google Cloud
1. Go to Google Cloud Console
2. Navigate to SQL > Instances > psedb1
3. Go to Connections tab
4. Add your IP to "Authorized networks"

### Step 3: Create Database
```sql
CREATE DATABASE auto_proposal_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Step 4: Initialize Tables
```powershell
python init_db.py
```

### Step 5: Start the Server
```powershell
python run.py
```

The API will be available at: http://localhost:8000

## 📚 Interactive API Documentation

Once the server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing with Postman

Import the collection file: `auto_proposal_complete.postman_collection.json`

This includes all endpoints for:
- Users CRUD operations
- Companies CRUD operations
- Clients operations
- Proposals operations

## Features

### User Management
- Password hashing (SHA-256)
- Unique username and email validation
- Role-based user types (admin, user, manager)
- Soft activation/deactivation
- Company association

### Company Management
- Unique company email validation
- Search by name (partial match)
- Filter by industry, city, active status
- Cannot delete company with associated users
- Comprehensive address and contact information

### Data Validation
- Email validation using Pydantic EmailStr
- Field length constraints
- Required vs optional fields
- Automatic timestamps (created_at, updated_at)

## Database Schema

### user_details Table
```sql
CREATE TABLE user_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    company_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES company_details(id)
);
```

### company_details Table
```sql
CREATE TABLE company_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(255) NOT NULL,
    company_email VARCHAR(255) UNIQUE NOT NULL,
    company_phone VARCHAR(50),
    address VARCHAR(500),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    website VARCHAR(255),
    tax_id VARCHAR(100),
    industry VARCHAR(100),
    description VARCHAR(1000),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## Error Handling

All endpoints include proper error handling:
- **400 Bad Request** - Validation errors, duplicate entries
- **404 Not Found** - Resource not found
- **201 Created** - Successful creation
- **204 No Content** - Successful deletion
- **200 OK** - Successful retrieval/update

## Next Steps

1. **Authorize your IP** in Google Cloud Console
2. **Update .env** with actual database credentials
3. **Run init_db.py** to create tables
4. **Start the server** with `python run.py`
5. **Test APIs** using Swagger UI at http://localhost:8000/docs

## Security Notes

⚠️ **Current Implementation**:
- Passwords are hashed using SHA-256
- **For Production**: Use bcrypt or Argon2 for password hashing
- **For Production**: Implement JWT authentication
- **For Production**: Add rate limiting
- **For Production**: Use HTTPS only

## Support

For issues:
1. Check `GOOGLE_CLOUD_SETUP.md` for database setup
2. Verify `.env` configuration
3. Check API documentation at `/docs`
4. Review error messages in terminal
