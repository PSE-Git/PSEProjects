import requests
import json

print("Testing login endpoint...")

# Test 1: Set password
try:
    print("\n1. Setting password...")
    resp = requests.post("http://localhost:8000/api/auth/set-password/1?password=Test123", timeout=5)
    print(f"   Status: {resp.status_code}")
    print(f"   Response: {resp.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Valid login
try:
    print("\n2. Testing valid login...")
    data = {
        "company_name": "Sky Interiors",
        "email": "bagavath@pseconsulting.in",
        "password": "Test123"
    }
    resp = requests.post("http://localhost:8000/api/auth/login", json=data, timeout=10)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        result = resp.json()
        print(f"   Success: {result['message']}")
        print(f"   User: {result['user']['full_name']}")
    else:
        print(f"   Error: {resp.text}")
except Exception as e:
    print(f"   Error: {e}")
    import traceback
    traceback.print_exc()

print("\nDone!")
