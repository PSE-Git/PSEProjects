"""
Test login endpoint - run this in a separate terminal while server is running
"""
import requests
import json

print("Testing Login API at http://localhost:8000/api/auth/login")
print("-" * 60)

try:
    response = requests.post(
        "http://localhost:8000/api/auth/login",
        json={
            "company_name": "PSE",
            "email": "karthi@pse.com", 
            "password": "karthi1212"
        },
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}\n")
    
    if response.status_code == 200:
        print("✅ SUCCESS - Login working!")
        result = response.json()
        print(json.dumps(result, indent=2))
    elif response.status_code == 401:
        print("❌ Invalid password")
        print(json.dumps(response.json(), indent=2))
    elif response.status_code == 404:
        print("❌ User or company not found")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except requests.exceptions.Timeout:
    print("❌ TIMEOUT - Database connection issue (IP not whitelisted?)")
except requests.exceptions.ConnectionError:
    print("❌ CONNECTION ERROR - Is server running?")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
