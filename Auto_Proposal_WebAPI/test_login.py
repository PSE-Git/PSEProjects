"""Test login endpoint"""
import sys
sys.path.insert(0, 'src')

from fastapi.testclient import TestClient
from auto_proposal.api.main import app
import json

client = TestClient(app)

print("=" * 70)
print("Testing Login API")
print("=" * 70)

# First, let's set a password for the existing user
print("\n1. Setting password for user ID 1...")
response = client.post("/api/auth/set-password/1?password=Test@123")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 1: Valid login
print("\n2. Testing VALID login...")
login_data = {
    "company_name": "Sky Interiors",
    "email": "bagavath@pseconsulting.in",
    "password": "Test@123"
}
response = client.post("/api/auth/login", json=login_data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 2: Invalid company
print("\n3. Testing INVALID company...")
login_data = {
    "company_name": "Non Existent Company",
    "email": "bagavath@pseconsulting.in",
    "password": "Test@123"
}
response = client.post("/api/auth/login", json=login_data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 3: Invalid email
print("\n4. Testing INVALID email...")
login_data = {
    "company_name": "Sky Interiors",
    "email": "nonexistent@example.com",
    "password": "Test@123"
}
response = client.post("/api/auth/login", json=login_data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 4: Invalid password
print("\n5. Testing INVALID password...")
login_data = {
    "company_name": "Sky Interiors",
    "email": "bagavath@pseconsulting.in",
    "password": "WrongPassword"
}
response = client.post("/api/auth/login", json=login_data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 5: Missing fields
print("\n6. Testing MISSING fields (validation error)...")
login_data = {
    "company_name": "Sky Interiors",
    "email": "bagavath@pseconsulting.in"
    # password missing
}
response = client.post("/api/auth/login", json=login_data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

print("\n" + "=" * 70)
print("Login API Testing Complete!")
print("=" * 70)
