"""Quick login test"""
import sys
import os
sys.path.insert(0, 'src')
os.chdir('D:/PSE/Projects/Auto/Coding/Auto_Proposal_WebAPI')

print("Loading app...")
from fastapi.testclient import TestClient
from auto_proposal.api.main import app

client = TestClient(app)

print("\n1. Setting password...")
try:
    resp = client.post("/api/auth/set-password/1?password=Test123")
    print(f"   Status: {resp.status_code}, {resp.json()}")
except Exception as e:
    print(f"   Error: {e}")

print("\n2. Testing valid login...")
try:
    data = {
        "company_name": "Sky Interiors",
        "email": "bagavath@pseconsulting.in",
        "password": "Test123"
    }
    resp = client.post("/api/auth/login", json=data)
    print(f"   Status: {resp.status_code}")
    result = resp.json()
    if resp.status_code == 200:
        print(f"   ✓ Success: {result['message']}")
        print(f"   ✓ User: {result['user']['full_name']}")
        print(f"   ✓ Access: {result['access_granted']}")
    else:
        print(f"   Error: {result}")
except Exception as e:
    print(f"   Error: {e}")

print("\n3. Testing invalid company...")
try:
    data = {
        "company_name": "Wrong Company",
        "email": "bagavath@pseconsulting.in",
        "password": "Test123"
    }
    resp = client.post("/api/auth/login", json=data)
    print(f"   Status: {resp.status_code}")
    print(f"   Response: {resp.json()['detail']['message']}")
except Exception as e:
    print(f"   Error: {e}")

print("\n4. Testing invalid password...")
try:
    data = {
        "company_name": "Sky Interiors",
        "email": "bagavath@pseconsulting.in",
        "password": "WrongPass"
    }
    resp = client.post("/api/auth/login", json=data)
    print(f"   Status: {resp.status_code}")
    print(f"   Response: {resp.json()['detail']['message']}")
except Exception as e:
    print(f"   Error: {e}")

print("\n✓ Tests complete!")
