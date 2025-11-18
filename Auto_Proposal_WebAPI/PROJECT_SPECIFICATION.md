# Auto Proposal Application - Project Specification Document

**Version:** 1.0  
**Date:** November 14, 2025  
**Project Name:** Auto Proposal Application  
**Development Platform:** Python WebAPI with Google Cloud Database  

---

## 1. Project Overview

### 1.1 Description
The **Auto Proposal Application** is a comprehensive business proposal management system designed to streamline the creation, management, and delivery of professional project proposals. The application enables businesses to efficiently manage client information, create detailed proposals with Bill of Quantities (BOQ) items, and generate professional PDF documents for client presentation.

### 1.2 Problem Statement
Traditional proposal creation is time-consuming, error-prone, and lacks standardization. Businesses struggle with:
- Manual calculation of project costs and BOQ items
- Inconsistent proposal formatting and branding
- Poor tracking of client proposals and their status
- Difficulty in maintaining historical proposal data
- Lack of centralized BOQ item management across projects

### 1.3 Objectives
- **Automate** proposal generation with pre-defined BOQ templates
- **Centralize** client and proposal data in a secure cloud database
- **Standardize** proposal format with company branding
- **Accelerate** proposal creation from days to minutes
- **Enable** real-time collaboration and proposal tracking
- **Provide** secure multi-company and multi-user support

---

## 2. Scope

### 2.1 In-Scope Functionalities
- **User Management:** Multi-user authentication with role-based access control
- **Company Management:** Support for multiple companies with isolated data
- **Client Management:** Complete CRUD operations for client information
- **BOQ Item Management:** Centralized Bill of Quantities item library with Excel import
- **Proposal Creation:** Dynamic proposal builder with BOQ item selection
- **Proposal Item Management:** Add, edit, delete items within proposals
- **PDF Generation:** Professional PDF output with company branding
- **Authentication:** Secure login with password hashing (bcrypt)
- **Cloud Database:** Google Cloud SQL for scalable, reliable data storage
- **RESTful API:** Complete API layer for all operations
- **Deployment:** IIS and standalone server deployment options

### 2.2 Out-of-Scope
- Mobile native applications (current focus: Web-based UI)
- Payment gateway integration
- Email automation for proposal delivery
- Advanced analytics and reporting dashboards
- Multi-language support (English only in v1.0)
- Customer portal for proposal viewing

### 2.3 Target Users
- **Primary:** Project managers, sales teams, estimation teams
- **Secondary:** Business owners, account managers
- **Industries:** Construction, interior design, consulting, IT services, manufacturing

### 2.4 Platforms Supported
- **Backend:** Web API accessible from any platform
- **Frontend:** Python-based desktop UI (planned web UI in future)
- **Deployment:** Windows Server with IIS, standalone Uvicorn server
- **Database:** Google Cloud SQL (MySQL)


## 3. System Architecture

### 3.1 Architecture Overview
The Auto Proposal Application follows a three-tier architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                      │
│                                                             │
│  ┌──────────────┐         ┌─────────────────┐             │
│  │  Python UI   │         │  API Clients    │             │
│  │  (Desktop)   │         │  (Postman, etc) │             │
│  └──────────────┘         └─────────────────┘             │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/REST
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           FastAPI Web Application                    │  │
│  │  ┌──────────┐  ┌──────────┐  ┌─────────────────┐   │  │
│  │  │  Routes  │  │ Services │  │   Middleware    │   │  │
│  │  │  (APIs)  │  │  (Logic) │  │  (CORS, Auth)   │   │  │
│  │  └──────────┘  └──────────┘  └─────────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           SQLAlchemy ORM Layer                       │  │
│  │  ┌─────────┐  ┌─────────┐  ┌──────────────────┐    │  │
│  │  │ Models  │  │ Schemas │  │   Repository     │    │  │
│  │  └─────────┘  └─────────┘  └──────────────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ SQL/SSL
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                             │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │        Google Cloud SQL (MySQL)                      │  │
│  │  ┌────────────┐  ┌──────────┐  ┌───────────────┐   │  │
│  │  │ UserDetails│  │ClientDtls│  │  Proposal     │   │  │
│  │  │ CompanyDtls│  │ BOQItems │  │ProposalItems  │   │  │
│  │  └────────────┘  └──────────┘  └───────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  Database: PSEAutoProposal                                  │
│  Region: asia-south1                                        │
│  SSL: Enabled with certificates                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Data Flow

1. **User Interaction → API Request**
   - User performs action in UI (e.g., create proposal)
   - UI sends HTTP request to FastAPI endpoint

2. **API Processing**
   - FastAPI route receives request
   - Validates request data using Pydantic schemas
   - Authenticates user credentials
   - Calls business logic in services layer

3. **Database Operations**
   - SQLAlchemy ORM translates operations to SQL
   - Secure connection to Google Cloud SQL over SSL
   - Transaction management ensures data integrity

4. **Response Generation**
   - Data retrieved from database
   - Formatted using Pydantic response models
   - Returned as JSON to client

5. **PDF Generation (if applicable)**
   - ReportLab library generates PDF
   - Saved to local file system
   - URL returned to client for download

---

## 4. Technology Stack

### 4.1 Backend Technologies
- **Language:** Python 3.12
- **Web Framework:** FastAPI 0.104.1
- **ASGI Server:** Uvicorn 0.24.0
- **ORM:** SQLAlchemy 2.0.23
- **Database Driver:** PyMySQL 1.1.0
- **Validation:** Pydantic 2.4.2
- **Authentication:** bcrypt 4.1.1

### 4.2 Database
- **Provider:** Google Cloud SQL
- **Engine:** MySQL
- **Instance:** alert-outlet-475913-f7:asia-south1:psedb1
- **Database:** PSEAutoProposal
- **Host:** 34.100.231.86:3306
- **Security:** SSL/TLS encryption with client certificates

### 4.3 Additional Libraries
- **PDF Generation:** ReportLab 4.0.7
- **Excel Processing:** pandas 2.1.2, openpyxl 3.1.2
- **Testing:** pytest 7.4.3, httpx 0.25.1
- **Environment Management:** python-dotenv 1.0.0
- **Cloud Connector:** cloud-sql-python-connector 1.5.0
- **ASGI/WSGI Bridge:** asgiref 3.7.2, a2wsgi

### 4.4 Development Tools
- **IDE:** Visual Studio Code
- **AI Assistant:** GitHub Copilot
- **API Testing:** Postman
- **Version Control:** Git
- **Deployment:** IIS (Windows Server), Uvicorn (standalone)

### 4.5 Middleware & Extensions
- **CORS:** Enabled for cross-origin requests
- **Static Files:** PDF file serving
- **Error Handling:** Custom HTTP exception handling
- **Logging:** Application and database connection logs

---

## 5. Modules & Features

### 5.1 Authentication Module
**Purpose:** Secure user access and session management

**Features:**
- Login with company name, username, and password
- Password hashing using bcrypt
- Comprehensive validation (7-step process):
  1. Company existence validation
  2. User existence validation
  3. Company-user association check
  4. User active status verification
  5. Password hash verification
  6. Subscription validity check
  7. Access end date validation
- Set/reset password functionality
- Role-based access control (Admin, User, Manager)

**API Endpoints:**
- `POST /api/auth/login` - User authentication
- `POST /api/auth/set-password/{user_id}` - Set/update password

---

### 5.2 User Management Module
**Purpose:** Manage user accounts and permissions

**Features:**
- Create new users with company association
- Update user details (name, email, role, access dates)
- Activate/deactivate user accounts
- View user list with filtering (active status, role)
- Search users by company
- Automatic password hashing on creation

**API Endpoints:**
- `POST /api/users` - Create user
- `GET /api/users` - List users (with filters)
- `GET /api/users/{user_id}` - Get user details
- `PUT /api/users/{user_id}` - Update user
- `DELETE /api/users/{user_id}` - Delete user
- `GET /api/users/company/{company_id}` - Users by company
- `PATCH /api/users/{user_id}/activate` - Activate user
- `PATCH /api/users/{user_id}/deactivate` - Deactivate user

---

### 5.3 Company Management Module
**Purpose:** Multi-company support with isolated data

**Features:**
- Company registration with industry type
- Subscription management (start/end dates)
- Update company profile (email, address, phone)
- View all companies or filter by industry
- Deactivate companies
- Automatic date tracking (created/modified)

**API Endpoints:**
- `POST /api/companies` - Create company
- `GET /api/companies` - List companies
- `GET /api/companies/{company_id}` - Get company details
- `PUT /api/companies/{company_id}` - Update company
- `DELETE /api/companies/{company_id}` - Delete company
- `GET /api/companies/industry/{industry_type}` - Filter by industry
- `PATCH /api/companies/{company_id}/deactivate` - Deactivate company

---

### 5.4 Client Management Module
**Purpose:** Maintain client database for proposals

**Features:**
- Add new clients with complete contact information
- Update client details (email, mobile, address)
- Search clients by company
- Active/inactive status management
- Track creation and modification dates
- Email validation

**API Endpoints:**
- `POST /api/clients` - Create client
- `GET /api/clients` - List all clients
- `GET /api/clients/{client_id}` - Get client details
- `GET /api/clients/company/{company_id}` - Clients by company
- `PUT /api/clients/{client_id}` - Update client
- `DELETE /api/clients/{client_id}` - Delete client
- `PATCH /api/clients/{client_id}/activate` - Activate client
- `PATCH /api/clients/{client_id}/deactivate` - Deactivate client

---

### 5.5 BOQ Item Management Module
**Purpose:** Centralized Bill of Quantities item library

**Features:**
- Add BOQ items with basic and premium rates
- Categorize by project type (Residential, Commercial, Industrial, etc.)
- Update pricing and descriptions
- Delete obsolete items
- Search items by title/description
- Import items from Excel (preview before save)
- Filter items by company and project type
- Get distinct project types for dropdown population

**API Endpoints:**
- `POST /api/boq-items` - Create BOQ item
- `GET /api/boq-items` - List items (with filters)
- `GET /api/boq-items/{sno}` - Get item details
- `PUT /api/boq-items/{sno}` - Update item
- `DELETE /api/boq-items/{sno}` - Delete item
- `GET /api/boq-items/search` - Search items
- `POST /api/boq-items/import-excel/preview` - Preview Excel import
- `POST /api/boq-items/import-excel/save` - Save Excel data
- `GET /api/boq-items/project-types/{company_id}` - Get project types

**Excel Import Format:**
- Columns: Description, Basic Rate, Premium Rate
- Automatic parsing with pandas
- Data validation before import

---

### 5.6 Proposal Management Module
**Purpose:** Create and manage project proposals

**Features:**
- Create proposals linked to clients
- Specify project details (type, area, materials, requirements)
- Track proposal status (Draft, Sent, Accepted, Rejected)
- Update proposal information
- Delete proposals
- Filter by company or client
- Automatic date tracking
- PDF generation for client presentation

**API Endpoints:**
- `POST /api/proposals` - Create proposal
- `GET /api/proposals` - List proposals
- `GET /api/proposals/{proposal_id}` - Get proposal details
- `GET /api/proposals/company/{company_id}` - Proposals by company
- `GET /api/proposals/client/{client_id}` - Proposals by client
- `PUT /api/proposals/{proposal_id}` - Update proposal
- `DELETE /api/proposals/{proposal_id}` - Delete proposal
- `PATCH /api/proposals/{proposal_id}/status/{new_status}` - Update status

**Proposal Fields:**
- Title, Description
- Client reference
- Project type (Residential, Commercial, etc.)
- Area (sq. ft.)
- Material preferences
- Special requirements
- Total amount (calculated from items)
- Status tracking
- PDF URL for generated documents

---

### 5.7 Proposal Item Management Module
**Purpose:** Manage line items within proposals

**Features:**
- Add items to proposals with quantity and unit price
- Automatic total calculation (Qty × Unit Price)
- Update item details
- Remove items from proposals
- View all items for a proposal
- Computed total column (database-level calculation)

**API Endpoints:**
- `POST /api/proposal-items` - Add item to proposal
- `GET /api/proposal-items/proposal/{proposal_id}` - Get proposal items
- `GET /api/proposal-items/{item_id}` - Get item details
- `PUT /api/proposal-items/{item_id}` - Update item
- `DELETE /api/proposal-items/{item_id}` - Delete item

**Database Computed Column:**
```python
Total = Computed('Qty * UnitPrice', persisted=True)
```
This ensures data integrity and automatic calculation.

---

### 5.8 PDF Generation Module
**Purpose:** Create professional proposal documents

**Features:**
- Company branding integration
- Itemized BOQ listing
- Automatic total calculation
- Terms and conditions section
- Client information display
- Digital signature placeholders
- PDF storage in `/pdf_files` directory
- URL-based access to generated PDFs

**Technology:** ReportLab 4.0.7

---

## 6. Database Design

### 6.1 Database: PSEAutoProposal

**Host:** 34.100.231.86:3306  
**Engine:** MySQL  
**Connection:** SSL/TLS encrypted  
**Region:** asia-south1  

---

### 6.2 Table: CompanyDetails

**Purpose:** Store company master data

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| CompanyID | INT | PRIMARY KEY, AUTO_INCREMENT | Unique company identifier |
| CompanyName | VARCHAR(255) | NOT NULL, UNIQUE | Company name |
| IndustryType | VARCHAR(100) | | Industry category |
| CompanyEmail | VARCHAR(255) | UNIQUE | Official email |
| CompanyAddress | TEXT | | Physical address |
| ContactNumber | VARCHAR(20) | | Phone number |
| SubscriptionStartDate | DATE | | Subscription start |
| SubscriptionEndDate | DATE | | Subscription expiry |
| IsActive | BOOLEAN | DEFAULT TRUE | Active status |
| CreatedDate | DATETIME | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| ModifiedDate | DATETIME | ON UPDATE CURRENT_TIMESTAMP | Last modified |

---

### 6.3 Table: UserDetails

**Purpose:** Store user accounts and credentials

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| UserID | INT | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier |
| CompanyID | INT | FOREIGN KEY → CompanyDetails | Associated company |
| FullName | VARCHAR(255) | NOT NULL | User full name |
| Email | VARCHAR(255) | UNIQUE, NOT NULL | Email address |
| PasswordHash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| Role | VARCHAR(50) | DEFAULT 'User' | User role (Admin/User/Manager) |
| IsActive | BOOLEAN | DEFAULT TRUE | Account status |
| AutoProposalAccessEndDate | DATE | | Access expiry date |
| CreatedDate | DATETIME | DEFAULT CURRENT_TIMESTAMP | Account creation |
| ModifiedDate | DATETIME | ON UPDATE CURRENT_TIMESTAMP | Last update |

---

### 6.4 Table: ClientDetails

**Purpose:** Store client information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ClientID | INT | PRIMARY KEY, AUTO_INCREMENT | Unique client identifier |
| CompanyID | INT | FOREIGN KEY → CompanyDetails | Owning company |
| ClientName | VARCHAR(255) | NOT NULL | Client name |
| EmailAddress | VARCHAR(255) | | Client email |
| MobileNumber | VARCHAR(20) | | Contact number |
| ContactAddress | TEXT | | Client address |
| CreateDate | DATETIME | DEFAULT CURRENT_TIMESTAMP | Record creation |
| ModifiedDate | DATETIME | ON UPDATE CURRENT_TIMESTAMP | Last modified |
| IsActive | BOOLEAN | DEFAULT TRUE | Active status |

---

### 6.5 Table: PseApBoqItems

**Purpose:** Bill of Quantities item library

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| SNo | INT | PRIMARY KEY, AUTO_INCREMENT | Unique item ID |
| CompanyID | INT | FOREIGN KEY → CompanyDetails | Owning company |
| ProjectType | VARCHAR(100) | | Project category |
| Title | VARCHAR(255) | NOT NULL | Item title |
| Description | TEXT | | Detailed description |
| Unit | VARCHAR(50) | | Measurement unit (sq.ft, kg, etc.) |
| BasicRate | DECIMAL(10,2) | | Basic pricing |
| PremiumRate | DECIMAL(10,2) | | Premium pricing |

**Indexes:**
- `idx_company_project` on (CompanyID, ProjectType)
- `idx_title` on (Title)

---

### 6.6 Table: Proposal

**Purpose:** Store proposal master records

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| Id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique proposal ID |
| CompanyID | INT | FOREIGN KEY → CompanyDetails | Creating company |
| ClientId | INT | FOREIGN KEY → ClientDetails | Target client |
| Title | VARCHAR(255) | NOT NULL | Proposal title |
| Description | TEXT | | Proposal details |
| Amount | DECIMAL(15,2) | | Total proposal value |
| Status | VARCHAR(50) | DEFAULT 'Draft' | Current status |
| PdfUrl | VARCHAR(500) | | Generated PDF path |
| CreatedDate | DATETIME | DEFAULT CURRENT_TIMESTAMP | Creation date |
| ModifyDate | DATETIME | ON UPDATE CURRENT_TIMESTAMP | Last modified |
| ProjectType | VARCHAR(100) | | Project category |
| Area | DECIMAL(10,2) | | Project area (sq.ft) |
| MaterialPreferences | TEXT | | Material choices |
| SpecialRequirement | TEXT | | Special notes |

**Status Values:** Draft, Sent, Accepted, Rejected, Revised

---

### 6.7 Table: ProposalItem

**Purpose:** Line items within proposals

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| Id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique item ID |
| ProposalId | INT | FOREIGN KEY → Proposal | Parent proposal |
| ItemName | VARCHAR(255) | NOT NULL | Item name |
| Description | TEXT | | Item details |
| Qty | DECIMAL(10,2) | NOT NULL | Quantity |
| UnitPrice | DECIMAL(10,2) | NOT NULL | Rate per unit |
| Total | DECIMAL(15,2) | COMPUTED (Qty * UnitPrice) | Line total |

**Computed Column:** Total is automatically calculated and persisted in the database.

---

### 6.8 Entity Relationship Diagram (Text Format)

```
CompanyDetails (1) ──────< (∞) UserDetails
     │                              
     │ (1)                          
     │                              
     ├──────< (∞) ClientDetails    
     │                              
     │ (1)                          
     │                              
     ├──────< (∞) PseApBoqItems    
     │                              
     │ (1)                          
     │                              
     └──────< (∞) Proposal         
                   │                
                   │ (1)            
                   │                
                   └──────< (∞) ProposalItem

ClientDetails (1) ──────< (∞) Proposal
```

**Relationships:**
- One Company has many Users, Clients, BOQ Items, and Proposals
- One Client has many Proposals
- One Proposal has many Proposal Items

---

### 6.9 Database Security

- **SSL/TLS Encryption:** All connections use SSL certificates
- **IP Whitelisting:** Authorized IP ranges (106.200.0.0/16, specific IPs)
- **User Credentials:** Stored in `.env` file (not in version control)
- **Password Hashing:** bcrypt with salt rounds
- **Connection Pooling:** Managed by SQLAlchemy
- **Prepared Statements:** ORM prevents SQL injection

---

## 7. API Design

### 7.1 API Overview

**Base URL:** `http://<host>:8000`  
**Documentation:** `/docs` (Swagger UI), `/redoc` (ReDoc)  
**Format:** JSON  
**Protocol:** HTTP/HTTPS  

---

### 7.2 Authentication APIs

#### POST /api/auth/login
**Purpose:** Authenticate user and validate access

**Request:**
```json
{
  "company_name": "PSE Solutions",
  "username": "john.doe@pse.com",
  "password": "SecurePass123"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "user_id": 5,
  "company_id": 2,
  "full_name": "John Doe",
  "role": "Admin"
}
```

**Validation Steps:**
1. Company exists
2. User exists with email
3. User belongs to company
4. User is active
5. Password matches hash
6. Subscription is valid
7. Access end date not expired

**Error Responses:**
- 404: Company/User not found
- 401: Invalid credentials
- 403: Account inactive or expired

---

#### POST /api/auth/set-password/{user_id}
**Purpose:** Set or update user password

**Request:**
```json
{
  "password": "NewSecurePass456"
}
```

**Response (200):**
```json
{
  "message": "Password updated successfully"
}
```

---

### 7.3 User Management APIs

#### POST /api/users
**Request:**
```json
{
  "company_id": 2,
  "full_name": "Jane Smith",
  "email": "jane@pse.com",
  "password": "InitialPass123",
  "role": "User",
  "auto_proposal_access_end_date": "2025-12-31"
}
```

#### GET /api/users?is_active=true&role=Admin&skip=0&limit=50
**Response:** Array of user objects

#### PUT /api/users/{user_id}
**Request:** Partial update with changed fields only

---

### 7.4 Company Management APIs

#### POST /api/companies
**Request:**
```json
{
  "company_name": "XYZ Corporation",
  "industry_type": "Construction",
  "company_email": "contact@xyz.com",
  "company_address": "123 Main St",
  "contact_number": "+91-9876543210",
  "subscription_start_date": "2025-01-01",
  "subscription_end_date": "2025-12-31"
}
```

---

### 7.5 Client Management APIs

#### POST /api/clients
**Request:**
```json
{
  "company_id": 2,
  "client_name": "ABC Builders",
  "email_address": "abc@builders.com",
  "mobile_number": "+91-9988776655",
  "contact_address": "456 Park Avenue"
}
```

---

### 7.6 BOQ Item APIs

#### POST /api/boq-items
**Request:**
```json
{
  "company_id": 2,
  "project_type": "Residential",
  "title": "False Ceiling",
  "description": "Gypsum board false ceiling with aluminum frame",
  "unit": "sq.ft",
  "basic_rate": 45.00,
  "premium_rate": 65.00
}
```

#### POST /api/boq-items/import-excel/preview
**Request:** Multipart form data with Excel file
**Response:** Preview of parsed data

#### GET /api/boq-items/project-types/{company_id}
**Response:**
```json
{
  "project_types": ["Residential", "Commercial", "Industrial"]
}
```

---

### 7.7 Proposal APIs

#### POST /api/proposals
**Request:**
```json
{
  "company_id": 2,
  "client_id": 15,
  "title": "Residential Interior Project",
  "description": "Complete interior design for 3BHK apartment",
  "project_type": "Residential",
  "area": 1500.00,
  "material_preferences": "Premium grade materials",
  "special_requirement": "Must complete in 45 days",
  "status": "Draft"
}
```

#### PATCH /api/proposals/{proposal_id}/status/Sent
**Response:** Updated proposal with new status

---

### 7.8 Proposal Item APIs

#### POST /api/proposal-items
**Request:**
```json
{
  "proposal_id": 5,
  "item_name": "False Ceiling",
  "description": "Gypsum board false ceiling",
  "qty": 850.00,
  "unit_price": 55.00
}
```

**Response:**
```json
{
  "id": 23,
  "proposal_id": 5,
  "item_name": "False Ceiling",
  "description": "Gypsum board false ceiling",
  "qty": 850.00,
  "unit_price": 55.00,
  "total": 46750.00
}
```

---

### 7.9 API Design Principles

**RESTful Standards:**
- GET: Retrieve resources
- POST: Create new resources
- PUT: Update entire resource
- PATCH: Partial update
- DELETE: Remove resource

**Status Codes:**
- 200: Success
- 201: Created
- 400: Bad Request (validation error)
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

**Validation:**
- Pydantic schemas for request/response
- Email format validation
- Required field checking
- Data type enforcement
- Relationship integrity checks

**Error Handling:**
- Descriptive error messages
- Field-level validation errors
- HTTP exception raising
- Detailed error logging

---

## 8. Testing & Quality Assurance

### 8.1 Testing Strategy

**Framework:** pytest 7.4.3  
**HTTP Client:** httpx 0.25.1  

---

### 8.2 Unit Testing

**Coverage Areas:**
- Model validation (SQLAlchemy models)
- Schema validation (Pydantic)
- Business logic functions
- Utility functions (password hashing)

**Example Test:**
```python
def test_hash_password():
    password = "TestPass123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed) == True
```

---

### 8.3 Integration Testing

**API Endpoint Tests:**
- Authentication flow
- CRUD operations for all modules
- Error handling scenarios
- Database transactions
- Relationship integrity

**Test Files Created:**
- `test_api.py` - General API tests
- `test_login_simple.py` - Authentication tests
- `test_client_api.py` - Client module tests
- `test_proposal_api.py` - Proposal tests
- `test_boq_items.py` - BOQ item tests
- `test_proposalitem_api.py` - Proposal item tests

---

### 8.4 Database Testing

**Connection Tests:**
- SSL certificate validation
- IP authorization checks
- Connection pool management
- Query execution

**Test Scripts:**
- `test_db_connection.py`
- `test_direct_connection.py`
- `check_ip_and_db.py`

---

### 8.5 API Testing Tools

**Postman Collections:**
- `auto_proposal_complete.postman_collection.json`
- Organized by modules
- Pre-configured requests
- Environment variables

---

### 8.6 Performance Testing

**Metrics:**
- API response time (target: <500ms)
- Database query performance
- Concurrent user handling
- Memory usage monitoring

---

### 8.7 Quality Checks

**Code Quality:**
- Type hints throughout codebase
- Docstrings for functions
- Consistent naming conventions
- DRY principle adherence

**Security Testing:**
- Password hashing verification
- SQL injection prevention (ORM)
- Input sanitization
- SSL connection validation

---

## 9. Deployment

### 9.1 Deployment Options

**Option 1: Standalone Uvicorn Server (Recommended)**
- Direct Python execution
- Best performance for FastAPI
- Suitable for development and production

**Option 2: IIS with FastCGI**
- Windows Server integration
- Requires wfastcgi configuration
- More complex setup

---

### 9.2 Standalone Deployment

#### Prerequisites
- Python 3.9 or higher
- pip package manager
- Virtual environment (recommended)

#### Installation Steps

1. **Clone/Copy Project Files**
```powershell
cd D:\PSE\Projects\Auto\Coding\Auto_Proposal_WebAPI
```

2. **Install Dependencies**
```powershell
pip install -r requirements.txt
```

3. **Configure Environment Variables**

Create `.env` file:
```env
# Database Configuration
DB_HOST=34.100.231.86
DB_PORT=3306
DB_USER=Karthiga
DB_PASSWORD=Pranu@25BK
DB_NAME=PSEAutoProposal

# SSL Configuration
SSL_CA=./certs/server-ca.pem
SSL_CERT=./certs/client-cert.pem
SSL_KEY=./certs/client-key.pem

# Cloud SQL Connector
USE_CLOUD_SQL_CONNECTOR=false
```

4. **Place SSL Certificates**
```
certs/
├── server-ca.pem
├── client-cert.pem
└── client-key.pem
```

5. **Run Server**
```powershell
.\run_server.ps1
```

Or manually:
```powershell
python -m uvicorn src.auto_proposal.api.main:app --host 0.0.0.0 --port 8000
```

6. **Verify Deployment**
- Open browser: `http://localhost:8000/docs`
- Test login API
- Check database connectivity

---

### 9.3 IIS Deployment

#### Prerequisites
- Windows Server 2016+ or Windows 10/11 Pro
- IIS installed with CGI support
- Administrator privileges

#### Installation Steps

1. **Install IIS Features**
```powershell
# Run as Administrator
.\install_iis_features.ps1
```

This installs:
- IIS Web Server Role
- IIS Management Console
- CGI Module (FastCGI)
- ISAPI Extensions
- ISAPI Filters

2. **Run Deployment Script**
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\deploy_to_iis.ps1
```

This script:
- Checks Python installation
- Installs wfastcgi and dependencies
- Enables wfastcgi in IIS
- Updates web.config with correct paths
- Creates necessary directories
- Tests application import

3. **Configure IIS Manager**

Open IIS Manager (`inetmgr`) and:

**Create Application Pool:**
- Name: `AutoProposalAPI`
- .NET CLR Version: `No Managed Code`
- Managed pipeline mode: `Integrated`

**Create Website:**
- Site name: `AutoProposalAPI`
- Application pool: `AutoProposalAPI`
- Physical path: `D:\PSE\Projects\Auto\Coding\Auto_Proposal_WebAPI`
- Binding: `http` on port `8000`

**Set Permissions:**
```powershell
icacls "D:\PSE\Projects\Auto\Coding\Auto_Proposal_WebAPI" /grant "IIS AppPool\AutoProposalAPI:(OI)(CI)F" /T
```

4. **Start Website**
- In IIS Manager, select the website
- Click "Start" in the Actions panel

5. **Test Deployment**
- Browser: `http://localhost:8000/docs`

---

### 9.4 Network Configuration

#### Firewall Rules

**Allow inbound traffic on port 8000:**
```powershell
# Run as Administrator
New-NetFirewallRule -DisplayName "FastAPI Port 8000" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

#### External Access

For access from other devices on the network:
1. Find your local IP: `ipconfig`
2. Access: `http://<your-ip>:8000/docs`
3. Example: `http://172.20.10.9:8000/docs`

---

### 9.5 Google Cloud SQL Configuration

#### IP Authorization

Add your public IP to Google Cloud SQL authorized networks:

1. **Find your public IP:**
```powershell
Invoke-RestMethod "https://api.ipify.org?format=json"
```

2. **Add to Google Cloud Console:**
- Navigate to: Cloud SQL → Instances → psedb1
- Connections → Networking
- Add authorized network
- Enter IP: `<your-ip>/32`
- Save

**Current Authorized IPs:**
- `106.200.0.0/16` (Subnet)
- `106.219.177.25/32` (Specific IP)

#### SSL Certificates

Certificates must be placed in `./certs/` directory:
- `server-ca.pem` - Server CA certificate
- `client-cert.pem` - Client certificate
- `client-key.pem` - Client private key

Download from Google Cloud Console:
- Cloud SQL → Instances → psedb1
- Connections → Security
- Download certificates

---

### 9.6 Troubleshooting Deployment

#### Check Server Status
```powershell
# Check if port is in use
Get-NetTCPConnection -LocalPort 8000

# Check running processes
Get-Process | Where-Object {$_.ProcessName -like "*python*"}
```

#### Test Database Connection
```powershell
python check_ip_and_db.py
```

#### View Application Logs
```
logs/
└── wfastcgi.log  (IIS deployment)
```

#### Common Issues

**Port Already in Use:**
```powershell
# Stop IIS
iisreset /stop

# Or kill process
Stop-Process -Id <PID>
```

**Module Import Errors:**
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Database Connection Timeout:**
- Verify IP is authorized in Google Cloud SQL
- Check SSL certificates exist
- Verify firewall rules

---

### 9.7 Production Deployment Checklist

- [ ] Update `.env` with production credentials
- [ ] Change database user password
- [ ] Enable HTTPS with SSL certificate
- [ ] Configure CORS for specific origins only
- [ ] Set up automatic backups for database
- [ ] Configure error logging and monitoring
- [ ] Set up health check endpoint
- [ ] Disable debug mode in FastAPI
- [ ] Configure rate limiting
- [ ] Set up load balancer (if multiple instances)
- [ ] Document recovery procedures
- [ ] Train support team on troubleshooting

---

## 10. Future Enhancements

### 10.1 AI-Powered Features

**Auto BOQ Suggestion:**
- Machine learning model trained on historical proposals
- Suggest BOQ items based on project type and area
- Predict pricing based on market trends
- Automatic material optimization

**Natural Language Processing:**
- Convert client requirements (text/voice) to proposal draft
- Extract project details from emails
- Sentiment analysis on proposal feedback

---

### 10.2 Advanced Analytics

**Dashboard Features:**
- Proposal win/loss ratio
- Revenue forecasting
- Client acquisition trends
- BOQ item usage analytics
- User performance metrics

**Reporting:**
- Export to Excel, PDF, CSV
- Custom report builder
- Scheduled email reports
- Real-time KPI monitoring

---

### 10.3 Collaboration Features

**Multi-User Editing:**
- Real-time proposal collaboration
- Comment and review system
- Version history and rollback
- Activity timeline

**Workflow Automation:**
- Approval workflows
- Email notifications
- Status change triggers
- Scheduled proposal sending

---

### 10.4 Integration Capabilities

**Third-Party Integrations:**
- Accounting software (QuickBooks, Tally)
- CRM systems (Salesforce, HubSpot)
- Email marketing platforms
- E-signature services (DocuSign)
- Cloud storage (Google Drive, Dropbox)

**API Enhancements:**
- Webhook support
- GraphQL API option
- Rate limiting and API keys
- Developer portal

---

### 10.5 Mobile & Web Applications

**Mobile App (iOS/Android):**
- Native mobile UI
- Offline mode with sync
- Push notifications
- Camera integration for site photos

**Web Application:**
- React/Vue.js frontend
- Progressive Web App (PWA)
- Responsive design
- Cross-browser compatibility

---

### 10.6 Enhanced PDF Generation

**Templates:**
- Multiple proposal templates
- Company branding customization
- Dynamic content blocks
- Interactive PDFs with embedded forms

**Features:**
- Digital signature integration
- QR code for verification
- Watermarking
- Password protection

---

### 10.7 Multi-Language Support

**Internationalization:**
- English, Hindi, Tamil, Telugu, Kannada
- Regional date/currency formats
- RTL language support
- Language-specific PDFs

---

### 10.8 Security Enhancements

**Advanced Authentication:**
- Two-factor authentication (2FA)
- Single Sign-On (SSO)
- OAuth integration
- Biometric authentication (mobile)

**Data Protection:**
- End-to-end encryption
- Data masking for sensitive fields
- Audit logging
- GDPR compliance tools

---

### 10.9 Performance Optimization

**Scalability:**
- Microservices architecture
- Kubernetes deployment
- Redis caching layer
- CDN for static files
- Database read replicas

**Monitoring:**
- Application Performance Monitoring (APM)
- Error tracking (Sentry)
- Uptime monitoring
- Automated alerting

---

### 10.10 Customer Portal

**Client Self-Service:**
- View proposals online
- Accept/reject proposals
- Request revisions
- Download PDF
- Payment integration

---

## 11. Conclusion

### 11.1 Business Impact

The **Auto Proposal Application** revolutionizes the proposal creation process by:

**Time Savings:**
- Reduces proposal creation time from days to minutes
- Eliminates manual data entry and calculations
- Automates repetitive tasks

**Cost Reduction:**
- Minimizes errors and rework
- Reduces paper and printing costs
- Optimizes resource utilization

**Revenue Growth:**
- Faster proposal turnaround increases win rate
- Professional presentation builds client trust
- Data-driven insights improve pricing strategy

**Competitive Advantage:**
- Modern, tech-driven approach
- Consistent quality across all proposals
- Scalable solution for business growth

---

### 11.2 Value Proposition

**For Project Managers:**
- Quick access to BOQ libraries
- Easy client management
- Status tracking and reporting
- Professional PDF generation

**For Sales Teams:**
- Faster response to client inquiries
- Data-driven pricing recommendations
- Historical proposal reference
- Mobile access (future)

**For Business Owners:**
- Multi-company management
- Subscription-based revenue model
- Scalable architecture
- Cloud-based accessibility

**For Clients:**
- Professional, detailed proposals
- Quick turnaround time
- Clear itemization and pricing
- Digital delivery

---

### 11.3 Success Metrics

**Quantitative:**
- 80% reduction in proposal creation time
- 50% increase in proposal volume
- 30% improvement in win rate
- 99.9% system uptime

**Qualitative:**
- Improved client satisfaction
- Enhanced team collaboration
- Consistent brand presentation
- Reduced human errors

---

### 11.4 Technology Excellence

The application demonstrates best practices in:
- **Architecture:** Three-tier, RESTful design
- **Security:** Encryption, hashing, IP whitelisting
- **Scalability:** Cloud database, stateless API
- **Maintainability:** Clean code, documentation, testing
- **Performance:** Optimized queries, connection pooling
- **User Experience:** Intuitive API, comprehensive documentation

---

### 11.5 Roadmap Summary

**Short-term (3-6 months):**
- Mobile app development
- Advanced analytics dashboard
- Email integration
- Multi-language support

**Medium-term (6-12 months):**
- AI-powered BOQ suggestions
- Customer portal
- Third-party integrations
- Advanced reporting

**Long-term (12+ months):**
- Microservices architecture
- Global expansion
- Industry-specific modules
- Enterprise features

---

### 11.6 Final Notes

The Auto Proposal Application is a comprehensive, production-ready solution built with modern technologies and best practices. Its modular architecture allows for continuous enhancement while maintaining stability and performance.

**Key Strengths:**
- Robust backend with FastAPI and SQLAlchemy
- Secure cloud database with Google Cloud SQL
- Complete API coverage for all operations
- Comprehensive testing and validation
- Multiple deployment options
- Detailed documentation

**Commitment to Quality:**
- Regular security updates
- Performance monitoring
- User feedback integration
- Continuous improvement

---

**Document Version:** 1.0  
**Last Updated:** November 14, 2025  
**Prepared by:** Development Team  
**Status:** Production Ready  

---

*This specification document serves as a comprehensive guide for the Auto Proposal Application. For technical implementation details, refer to the API documentation at `/docs` endpoint.*
