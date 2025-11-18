# BOQ Items API Documentation

## Overview
CRUD API endpoints for managing Bill of Quantities (BOQ) items in the PSEAutoProposal system.

## Base URL
```
http://localhost:8000/api/boq-items
```

## Database Table
**Table Name:** `PseApBoqItems`

**Schema:**
- `SNo` (int, Primary Key, Auto Increment) - Serial Number
- `CompanyID` (int, Foreign Key to CompanyDetails) - Company ID (optional)
- `ProjectType` (varchar 100) - Type of project (e.g., "Residential", "Commercial", "Saloon")
- `Title` (varchar 150) - Item title/name
- `Description` (text) - Detailed description of the item
- `Unit` (varchar 50) - Unit of measurement (e.g., "sqft", "piece", "running meter", "point")
- `BasicRate` (decimal 10,2) - Basic rate per unit
- `PremiumRate` (decimal 10,2) - Premium rate per unit

## API Endpoints

### 1. Create BOQ Item
**POST** `/api/boq-items/`

Creates a new BOQ item.

**Request Body:**
```json
{
  "company_id": 1,
  "project_type": "Residential",
  "title": "PVC Plumbing Pipes",
  "description": "110mm PVC plumbing pipes for drainage system",
  "unit": "running meter",
  "basic_rate": 150.00,
  "premium_rate": 185.00
}
```

**Response (201 Created):**
```json
{
  "sno": 3,
  "company_id": 1,
  "project_type": "Residential",
  "title": "PVC Plumbing Pipes",
  "description": "110mm PVC plumbing pipes for drainage system",
  "unit": "running meter",
  "basic_rate": 150.0,
  "premium_rate": 185.0
}
```

---

### 2. Get All BOQ Items (with filtering)
**GET** `/api/boq-items/`

Retrieves all BOQ items with optional filtering.

**Query Parameters:**
- `skip` (int, default=0) - Number of records to skip (pagination)
- `limit` (int, default=100, max=500) - Maximum number of records to return
- `company_id` (int, optional) - Filter by company ID
- `project_type` (string, optional) - Filter by project type

**Examples:**
```
GET /api/boq-items/
GET /api/boq-items/?company_id=1
GET /api/boq-items/?project_type=Residential
GET /api/boq-items/?company_id=1&project_type=Commercial
GET /api/boq-items/?skip=0&limit=50
```

**Response (200 OK):**
```json
[
  {
    "sno": 1,
    "company_id": 1,
    "project_type": "Saloon",
    "title": "False Ceiling",
    "description": "Providing and fixing suspended false ceiling...",
    "unit": "sft",
    "basic_rate": 70.0,
    "premium_rate": 80.0
  },
  {
    "sno": 2,
    "company_id": 1,
    "project_type": "Saloon",
    "title": "Gypsum board",
    "description": "Providing and fixing of 12mm thick gypsum board...",
    "unit": "sft",
    "basic_rate": 130.0,
    "premium_rate": 150.0
  }
]
```

---

### 3. Get BOQ Item by SNo
**GET** `/api/boq-items/{sno}`

Retrieves a specific BOQ item by its Serial Number.

**Path Parameters:**
- `sno` (int) - Serial Number of the BOQ item

**Example:**
```
GET /api/boq-items/1
```

**Response (200 OK):**
```json
{
  "sno": 1,
  "company_id": 1,
  "project_type": "Saloon",
  "title": "False Ceiling",
  "description": "Providing and fixing suspended false ceiling...",
  "unit": "sft",
  "basic_rate": 70.0,
  "premium_rate": 80.0
}
```

**Response (404 Not Found):**
```json
{
  "detail": "BOQ item with SNo 999 not found"
}
```

---

### 4. Update BOQ Item
**PUT** `/api/boq-items/{sno}`

Updates an existing BOQ item. Only provided fields will be updated.

**Path Parameters:**
- `sno` (int) - Serial Number of the BOQ item

**Request Body (all fields optional):**
```json
{
  "basic_rate": 165.00,
  "premium_rate": 200.00,
  "description": "110mm PVC plumbing pipes for drainage system - Updated rate"
}
```

**Response (200 OK):**
```json
{
  "sno": 3,
  "company_id": 1,
  "project_type": "Residential",
  "title": "PVC Plumbing Pipes",
  "description": "110mm PVC plumbing pipes for drainage system - Updated rate",
  "unit": "running meter",
  "basic_rate": 165.0,
  "premium_rate": 200.0
}
```

**Response (404 Not Found):**
```json
{
  "detail": "BOQ item with SNo 999 not found"
}
```

---

### 5. Delete BOQ Item
**DELETE** `/api/boq-items/{sno}`

Deletes a BOQ item by its Serial Number.

**Path Parameters:**
- `sno` (int) - Serial Number of the BOQ item

**Example:**
```
DELETE /api/boq-items/3
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "BOQ item with SNo 3 deleted successfully"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "BOQ item with SNo 999 not found"
}
```

---

### 6. Search BOQ Items
**GET** `/api/boq-items/search/`

Searches BOQ items by title or description.

**Query Parameters:**
- `query` (string, required, min_length=1) - Search term

**Example:**
```
GET /api/boq-items/search/?query=PVC
GET /api/boq-items/search/?query=ceiling
```

**Response (200 OK):**
```json
[
  {
    "sno": 3,
    "company_id": 1,
    "project_type": "Residential",
    "title": "PVC Plumbing Pipes",
    "description": "110mm PVC plumbing pipes for drainage system",
    "unit": "running meter",
    "basic_rate": 150.0,
    "premium_rate": 185.0
  }
]
```

---

## Data Models

### BoqItemCreate
```python
{
  "company_id": int (optional),
  "project_type": str (optional, max 100 chars),
  "title": str (optional, max 150 chars),
  "description": str (optional),
  "unit": str (optional, max 50 chars),
  "basic_rate": float (optional, >= 0),
  "premium_rate": float (optional, >= 0)
}
```

### BoqItemUpdate
```python
{
  "company_id": int (optional),
  "project_type": str (optional, max 100 chars),
  "title": str (optional, max 150 chars),
  "description": str (optional),
  "unit": str (optional, max 50 chars),
  "basic_rate": float (optional, >= 0),
  "premium_rate": float (optional, >= 0)
}
```

### BoqItemResponse
```python
{
  "sno": int (auto-generated),
  "company_id": int (optional),
  "project_type": str (optional),
  "title": str (optional),
  "description": str (optional),
  "unit": str (optional),
  "basic_rate": float (optional),
  "premium_rate": float (optional)
}
```

---

## Testing

### Using Swagger UI
1. Start the server: `python run.py`
2. Open browser: http://localhost:8000/docs
3. Navigate to "BOQ Items" section
4. Click on any endpoint to test it interactively

### Using Python Requests
```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Create a new BOQ item
response = requests.post(
    f"{BASE_URL}/api/boq-items/",
    json={
        "company_id": 1,
        "project_type": "Commercial",
        "title": "Electrical Wiring",
        "description": "Complete electrical wiring work",
        "unit": "point",
        "basic_rate": 250.0,
        "premium_rate": 300.0
    }
)
print(f"Created: {response.json()}")

# Get all BOQ items for a company
response = requests.get(f"{BASE_URL}/api/boq-items/?company_id=1")
print(f"All items: {response.json()}")

# Update a BOQ item
response = requests.put(
    f"{BASE_URL}/api/boq-items/3",
    json={"basic_rate": 275.0}
)
print(f"Updated: {response.json()}")

# Delete a BOQ item
response = requests.delete(f"{BASE_URL}/api/boq-items/3")
print(f"Deleted: {response.json()}")
```

### Using Test Script
Run the comprehensive test suite:
```bash
python test_boq_items.py
```

---

## Files Created/Modified

1. **src/auto_proposal/core/models.py**
   - Added `PseApBoqItems` model with proper column mappings

2. **src/auto_proposal/core/schemas.py**
   - Added `BoqItemBase`, `BoqItemCreate`, `BoqItemUpdate`, `BoqItemResponse` schemas

3. **src/auto_proposal/api/routes/boq_items.py**
   - Created complete CRUD routes for BOQ items
   - 6 endpoints: Create, GetAll, GetByID, Update, Delete, Search

4. **src/auto_proposal/api/routes/__init__.py**
   - Added `boq_items` to module exports

5. **src/auto_proposal/api/main.py**
   - Registered `boq_items.router` in the application

6. **test_boq_items.py**
   - Comprehensive test suite for all BOQ endpoints

---

## Common Use Cases

### 1. Adding Items for a New Project Type
```bash
POST /api/boq-items/
{
  "company_id": 1,
  "project_type": "Hospital",
  "title": "Medical Gas Pipeline",
  "description": "Complete medical gas pipeline installation",
  "unit": "point",
  "basic_rate": 5000.0,
  "premium_rate": 6000.0
}
```

### 2. Listing All Items for a Specific Project Type
```bash
GET /api/boq-items/?project_type=Hospital
```

### 3. Updating Rates for Existing Items
```bash
PUT /api/boq-items/5
{
  "basic_rate": 5500.0,
  "premium_rate": 6500.0
}
```

### 4. Finding Items by Search Term
```bash
GET /api/boq-items/search/?query=pipeline
```

---

## Error Responses

### 404 Not Found
```json
{
  "detail": "BOQ item with SNo 999 not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "basic_rate"],
      "msg": "ensure this value is greater than or equal to 0",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Notes

- All fields except `sno` are optional when creating/updating BOQ items
- `sno` is auto-generated and cannot be manually set
- `basic_rate` and `premium_rate` must be >= 0 if provided
- The relationship with `CompanyDetails` table is established via `company_id`
- Existing data: 2 items already exist (SNo 1, 2) for Company 1, Project Type "Saloon"

---

## Server Information

- **Host:** localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Database:** PSEAutoProposal (Google Cloud SQL MySQL)
- **Table:** PseApBoqItems
