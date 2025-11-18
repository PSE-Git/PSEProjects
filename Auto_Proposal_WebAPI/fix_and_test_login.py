"""Fix password and test login"""
import sys
sys.path.insert(0, 'src')

from fastapi.testclient import TestClient
from auto_proposal.api.main import app

client = TestClient(app)

print("=" * 60)
print("Fixing Password Hash and Testing Login")
print("=" * 60)

# Step 1: Set the password using the API (this will hash it)
print("\n1. Setting password 'karthi1212' for user 1...")
response = client.post("/api/auth/set-password/1?password=karthi1212")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   ✓ {response.json()['message']}")
else:
    print(f"   Error: {response.text}")

# Step 2: Try login with the correct password
print("\n2. Testing login with correct password...")
login_data = {
    "company_name": "Sky Interiors",
    "email": "bagavath@pseconsulting.in",
    "password": "karthi1212"
}
response = client.post("/api/auth/login", json=login_data)
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print(f"   ✓ SUCCESS: {result['message']}")
    print(f"   ✓ User: {result['user']['full_name']}")
    print(f"   ✓ Email: {result['user']['email']}")
    print(f"   ✓ Role: {result['user']['role']}")
    print(f"   ✓ Access Granted: {result['access_granted']}")
    if result.get('access_end_date'):
        print(f"   ✓ Access Until: {result['access_end_date']}")
else:
    error = response.json()
    print(f"   ✗ FAILED: {error}")

print("\n" + "=" * 60)
print("✓ Password fixed! You can now login with:")
print("   Company: Sky Interiors")
print("   Email: bagavath@pseconsulting.in")
print("   Password: karthi1212")
print("=" * 60)
