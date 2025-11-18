"""
Simple BOQ test to debug the 500 error
"""
import requests
import json
import traceback

BASE_URL = "http://localhost:8000"

try:
    print("Testing POST /api/boq-items/")
    payload = {
        "company_id": 1,
        "project_type": "Residential",
        "title": "Test Item",
        "description": "Test Description",
        "unit": "sqft",
        "basic_rate": 100.0,
        "premium_rate": 120.0
    }
    
    print(f"\nPayload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/api/boq-items/", json=payload)
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"\nResponse Text: {response.text}")
    
    if response.status_code == 201:
        print("\nSuccess! Response JSON:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"\nError occurred. Status: {response.status_code}")
        try:
            error_detail = response.json()
            print(f"Error Detail: {json.dumps(error_detail, indent=2)}")
        except:
            print(f"Raw Response: {response.text}")

except Exception as e:
    print(f"\nException occurred: {str(e)}")
    traceback.print_exc()
