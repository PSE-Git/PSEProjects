"""
Test script for BOQ Items API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_boq_item():
    """Test creating a new BOQ item"""
    print("\n=== Testing Create BOQ Item ===")
    
    payload = {
        "company_id": 1,
        "project_type": "Residential",
        "title": "PVC Plumbing Pipes",
        "description": "110mm PVC plumbing pipes for drainage system",
        "unit": "running meter",
        "basic_rate": 150.00,
        "premium_rate": 185.00
    }
    
    response = requests.post(f"{BASE_URL}/api/boq-items/", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        return response.json()["sno"]
    return None


def test_get_all_boq_items():
    """Test getting all BOQ items"""
    print("\n=== Testing Get All BOQ Items ===")
    
    response = requests.get(f"{BASE_URL}/api/boq-items/")
    print(f"Status Code: {response.status_code}")
    print(f"Number of items: {len(response.json())}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_get_boq_item_by_sno(sno):
    """Test getting a BOQ item by SNo"""
    print(f"\n=== Testing Get BOQ Item by SNo ({sno}) ===")
    
    response = requests.get(f"{BASE_URL}/api/boq-items/{sno}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_update_boq_item(sno):
    """Test updating a BOQ item"""
    print(f"\n=== Testing Update BOQ Item ({sno}) ===")
    
    payload = {
        "basic_rate": 165.00,
        "premium_rate": 200.00,
        "description": "110mm PVC plumbing pipes for drainage system - Updated rate"
    }
    
    response = requests.put(f"{BASE_URL}/api/boq-items/{sno}", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_search_boq_items():
    """Test searching BOQ items"""
    print("\n=== Testing Search BOQ Items ===")
    
    response = requests.get(f"{BASE_URL}/api/boq-items/search/?query=PVC")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_filter_boq_items():
    """Test filtering BOQ items by company_id and project_type"""
    print("\n=== Testing Filter BOQ Items (company_id=1, project_type=Residential) ===")
    
    response = requests.get(f"{BASE_URL}/api/boq-items/?company_id=1&project_type=Residential")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_delete_boq_item(sno):
    """Test deleting a BOQ item"""
    print(f"\n=== Testing Delete BOQ Item ({sno}) ===")
    
    response = requests.delete(f"{BASE_URL}/api/boq-items/{sno}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def main():
    """Run all tests"""
    print("=" * 60)
    print("BOQ Items API Test Suite")
    print("=" * 60)
    
    try:
        # Test 1: Create BOQ item
        sno = test_create_boq_item()
        
        # Test 2: Get all BOQ items
        test_get_all_boq_items()
        
        if sno:
            # Test 3: Get specific BOQ item
            test_get_boq_item_by_sno(sno)
            
            # Test 4: Update BOQ item
            test_update_boq_item(sno)
            
            # Test 5: Get updated item
            test_get_boq_item_by_sno(sno)
        
        # Test 6: Search BOQ items
        test_search_boq_items()
        
        # Test 7: Filter BOQ items
        test_filter_boq_items()
        
        if sno:
            # Test 8: Delete BOQ item
            test_delete_boq_item(sno)
            
            # Verify deletion
            print("\n=== Verifying Deletion ===")
            response = requests.get(f"{BASE_URL}/api/boq-items/{sno}")
            print(f"Status Code: {response.status_code} (should be 404)")
        
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\nError: Cannot connect to API server.")
        print("Please ensure the server is running at http://localhost:8000")
    except Exception as e:
        print(f"\nError: {str(e)}")


if __name__ == "__main__":
    main()
