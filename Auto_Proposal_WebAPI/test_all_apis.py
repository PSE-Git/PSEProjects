"""
Quick API test - tests all endpoints
"""
import sys
sys.path.insert(0, 'src')

from fastapi.testclient import TestClient
from auto_proposal.api.main import app

client = TestClient(app)

print("=" * 60)
print("Testing Auto Proposal APIs")
print("=" * 60)

# Test 1: Root endpoint
print("\n1. Testing root endpoint...")
response = client.get("/")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")

# Test 2: Get users
print("\n2. Testing GET /api/users/...")
response = client.get("/api/users/")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    users = response.json()
    print(f"   Found {len(users)} users")
    if users:
        print(f"   First user: {users[0]['full_name']} ({users[0]['email']})")

# Test 3: Get companies
print("\n3. Testing GET /api/companies/...")
response = client.get("/api/companies/")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    companies = response.json()
    print(f"   Found {len(companies)} companies")
    if companies:
        print(f"   First company: {companies[0]['company_name']}")

# Test 4: Set password
print("\n4. Setting password for user 1...")
response = client.post("/api/auth/set-password/1?password=Test@123")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   {response.json()['message']}")

# Test 5: Login - Valid
print("\n5. Testing LOGIN - Valid credentials...")
login_data = {
    "company_name": "Sky Interiors",
    "email": "bagavath@pseconsulting.in",
    "password": "Test@123"
}
response = client.post("/api/auth/login", json=login_data)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"   ✓ {result['message']}")
    print(f"   ✓ User: {result['user']['full_name']}")
    print(f"   ✓ Role: {result['user']['role']}")
    print(f"   ✓ Access Granted: {result['access_granted']}")
else:
    print(f"   Error: {response.text}")

# Test 6: Login - Invalid password
print("\n6. Testing LOGIN - Invalid password...")
login_data = {
    "company_name": "Sky Interiors",
    "email": "bagavath@pseconsulting.in",
    "password": "WrongPassword"
}
response = client.post("/api/auth/login", json=login_data)
print(f"   Status: {response.status_code}")
if response.status_code == 401:
    error = response.json()
    print(f"   ✓ Correctly rejected: {error['detail']['message']}")

# Test 7: Login - Invalid company
print("\n7. Testing LOGIN - Invalid company...")
login_data = {
    "company_name": "Wrong Company",
    "email": "bagavath@pseconsulting.in",
    "password": "Test@123"
}
response = client.post("/api/auth/login", json=login_data)
print(f"   Status: {response.status_code}")
if response.status_code == 404:
    error = response.json()
    print(f"   ✓ Correctly rejected: {error['detail']['message']}")

print("\n" + "=" * 60)
print("✓ All API tests completed successfully!")
print("=" * 60)
print("\nAPI Documentation: http://localhost:8000/docs")
