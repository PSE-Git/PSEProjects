"""
Test ClientDetails API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/clients"

def test_get_all_clients():
    """Test GET all clients"""
    print("\n=== Testing GET /api/clients/ ===")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")

def test_get_clients_by_company(company_id=1):
    """Test GET clients by company ID"""
    print(f"\n=== Testing GET /api/clients/company/{company_id} ===")
    try:
        response = requests.get(f"{BASE_URL}/company/{company_id}")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")

def test_create_client():
    """Test POST create client"""
    print("\n=== Testing POST /api/clients/ ===")
    
    client_data = {
        "company_id": 1,
        "client_name": "Test Client",
        "email_address": "test@example.com",
        "mobile_number": "9876543210",
        "contact_address": "123 Test Street, Test City",
        "is_active": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/", json=client_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return response.json().get('id')
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")
    
    return None

def test_get_client_by_id(client_id):
    """Test GET client by ID"""
    print(f"\n=== Testing GET /api/clients/{client_id} ===")
    try:
        response = requests.get(f"{BASE_URL}/{client_id}")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")

if __name__ == "__main__":
    print("Testing ClientDetails API Endpoints")
    print("=" * 50)
    
    # Test each endpoint
    test_get_all_clients()
    test_get_clients_by_company(1)
    
    # Create a new client and test other operations
    client_id = test_create_client()
    
    if client_id:
        test_get_client_by_id(client_id)
    
    print("\n" + "=" * 50)
    print("Testing completed!")
