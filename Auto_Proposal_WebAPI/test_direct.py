"""Direct test with TestClient to see errors"""
import sys
sys.path.insert(0, 'src')

from fastapi.testclient import TestClient
from auto_proposal.api.main import app

client = TestClient(app)

print("Testing GET /api/users...")
response = client.get("/api/users/")
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    print(f"Success! Response: {response.json()}")
else:
    print(f"Error! Response: {response.text}")
    
print("\n\nTesting GET /api/companies...")
response = client.get("/api/companies/")
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    print(f"Success! Response: {response.json()}")
else:
    print(f"Error! Response: {response.text}")
