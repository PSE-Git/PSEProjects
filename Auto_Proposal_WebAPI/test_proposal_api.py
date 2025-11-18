"""
Test Proposal API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/proposals"

def test_create_proposal():
    """Test POST create proposal"""
    print("\n=== Testing POST /api/proposals/ ===")
    
    proposal_data = {
        "company_id": 1,
        "client_id": 1,
        "title": "Residential Interior Design - Anna's Home",
        "description": "Complete interior design for 3BHK apartment",
        "amount": 250000.00,
        "status": "Draft",
        "project_type": "Residential",
        "area": "1500 sqft",
        "material_preferences": "Premium quality, eco-friendly materials",
        "special_requirement": "Modern contemporary style with minimalist approach"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/", json=proposal_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return response.json().get('id')
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")
    
    return None

def test_get_proposal_by_id(proposal_id):
    """Test GET proposal by ID"""
    print(f"\n=== Testing GET /api/proposals/{proposal_id} ===")
    try:
        response = requests.get(f"{BASE_URL}/{proposal_id}")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")

def test_get_proposals_by_company(company_id=1):
    """Test GET proposals by company ID"""
    print(f"\n=== Testing GET /api/proposals/company/{company_id} ===")
    try:
        response = requests.get(f"{BASE_URL}/company/{company_id}")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            proposals = response.json()
            print(f"Found {len(proposals)} proposals")
            print(f"Response: {json.dumps(proposals, indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")

def test_update_proposal(proposal_id):
    """Test PUT update proposal"""
    print(f"\n=== Testing PUT /api/proposals/{proposal_id} ===")
    
    update_data = {
        "amount": 275000.00,
        "status": "Sent"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/{proposal_id}", json=update_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")

def test_update_status(proposal_id, new_status="Approved"):
    """Test PATCH update proposal status"""
    print(f"\n=== Testing PATCH /api/proposals/{proposal_id}/status/{new_status} ===")
    try:
        response = requests.patch(f"{BASE_URL}/{proposal_id}/status/{new_status}")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")

def test_get_all_proposals():
    """Test GET all proposals"""
    print("\n=== Testing GET /api/proposals/ ===")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            proposals = response.json()
            print(f"Found {len(proposals)} proposals")
            if proposals:
                print(f"First proposal: {json.dumps(proposals[0], indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")

if __name__ == "__main__":
    print("Testing Proposal API Endpoints")
    print("=" * 50)
    
    # Test creating a proposal
    proposal_id = test_create_proposal()
    
    # Test other operations
    if proposal_id:
        test_get_proposal_by_id(proposal_id)
        test_update_proposal(proposal_id)
        test_update_status(proposal_id, "Approved")
    
    # Test getting proposals by company
    test_get_proposals_by_company(1)
    
    # Test getting all proposals
    test_get_all_proposals()
    
    print("\n" + "=" * 50)
    print("Testing completed!")
