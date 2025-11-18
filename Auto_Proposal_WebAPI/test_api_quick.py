"""
Quick API test to check if endpoints are working
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("Testing Auto Proposal API")
print("=" * 60)

# Test 1: Root endpoint
print("\n1. Testing root endpoint...")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {str(e)}")

# Test 2: Get all companies
print("\n2. Testing GET /api/companies/...")
try:
    response = requests.get(f"{BASE_URL}/api/companies/")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.json()}")
    else:
        print(f"   Error Response: {response.text}")
except Exception as e:
    print(f"   Error: {str(e)}")

# Test 3: Get all users
print("\n3. Testing GET /api/users/...")
try:
    response = requests.get(f"{BASE_URL}/api/users/")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.json()}")
    else:
        print(f"   Error Response: {response.text}")
except Exception as e:
    print(f"   Error: {str(e)}")

# Test 4: Create a company
print("\n4. Testing POST /api/companies/ (Create Company)...")
try:
    company_data = {
        "company_name": "Test Company",
        "company_email": "test@company.com",
        "company_phone": "+1234567890",
        "address": "123 Test St",
        "city": "Test City",
        "state": "TS",
        "country": "Test Country",
        "postal_code": "12345",
        "website": "https://testcompany.com",
        "tax_id": "123456789",
        "industry": "Technology",
        "description": "A test company",
        "is_active": True
    }
    response = requests.post(f"{BASE_URL}/api/companies/", json=company_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        print(f"   Created Company: {response.json()}")
    else:
        print(f"   Error Response: {response.text}")
except Exception as e:
    print(f"   Error: {str(e)}")

# Test 5: Create a user
print("\n5. Testing POST /api/users/ (Create User)...")
try:
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "password123",
        "phone": "+9876543210",
        "role": "user",
        "is_active": True,
        "company_id": None
    }
    response = requests.post(f"{BASE_URL}/api/users/", json=user_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        print(f"   Created User: {response.json()}")
    else:
        print(f"   Error Response: {response.text}")
except Exception as e:
    print(f"   Error: {str(e)}")

# Test 6: API Documentation
print("\n6. API Documentation Available at:")
print(f"   Swagger UI: {BASE_URL}/docs")
print(f"   ReDoc: {BASE_URL}/redoc")

print("\n" + "=" * 60)
print("Test completed!")
print("=" * 60)
