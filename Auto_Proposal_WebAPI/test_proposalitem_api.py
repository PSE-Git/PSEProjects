"""
Test ProposalItem API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/proposal-items"
PROPOSAL_URL = "http://localhost:8000/api/proposals"

def create_test_proposal():
    """Create a test proposal to work with"""
    print("\n=== Creating Test Proposal ===")
    proposal_data = {
        "company_id": 1,
        "client_id": 1,
        "title": "Test Proposal for Items",
        "description": "Testing proposal items",
        "amount": 0.00,
        "status": "Draft"
    }
    
    try:
        response = requests.post(f"{PROPOSAL_URL}/", json=proposal_data)
        if response.status_code == 201:
            proposal = response.json()
            print(f"✓ Created proposal ID: {proposal['id']}")
            return proposal['id']
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")
    
    return None

def test_add_proposal_item(proposal_id, item_name, qty, unit_price):
    """Test POST - Add item to proposal"""
    print(f"\n=== Testing POST /api/proposal-items/ ===")
    print(f"Adding: {item_name} (Qty: {qty}, Price: ₹{unit_price})")
    
    item_data = {
        "proposal_id": proposal_id,
        "item_name": item_name,
        "description": f"Description for {item_name}",
        "qty": qty,
        "unit_price": unit_price
    }
    
    try:
        response = requests.post(f"{BASE_URL}/", json=item_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            item = response.json()
            print(f"Response: {json.dumps(item, indent=2)}")
            print(f"✓ Item ID: {item['id']}, Total: ₹{item['total']}")
            return item['id']
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")
    
    return None

def test_get_proposal_items(proposal_id):
    """Test GET - Get all items for a proposal"""
    print(f"\n=== Testing GET /api/proposal-items/proposal/{proposal_id} ===")
    
    try:
        response = requests.get(f"{BASE_URL}/proposal/{proposal_id}")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            items = response.json()
            print(f"Found {len(items)} items for Proposal {proposal_id}")
            print("\nItems List:")
            print("-" * 80)
            total_amount = 0
            for idx, item in enumerate(items, 1):
                print(f"\n{idx}. {item['item_name']}")
                print(f"   ID: {item['id']}")
                print(f"   Description: {item['description']}")
                print(f"   Quantity: {item['qty']}")
                print(f"   Unit Price: ₹{item['unit_price']}")
                print(f"   Total: ₹{item['total']}")
                total_amount += item['total'] if item['total'] else 0
            
            print("\n" + "-" * 80)
            print(f"Grand Total: ₹{total_amount}")
            return items
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")
    
    return None

def test_update_proposal_item(item_id):
    """Test PUT - Update proposal item"""
    print(f"\n=== Testing PUT /api/proposal-items/{item_id} ===")
    
    update_data = {
        "qty": 3,
        "unit_price": 1500.00
    }
    
    try:
        response = requests.put(f"{BASE_URL}/{item_id}", json=update_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            item = response.json()
            print(f"✓ Updated successfully")
            print(f"New Qty: {item['qty']}, New Price: ₹{item['unit_price']}, New Total: ₹{item['total']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")

def test_delete_proposal_item(item_id):
    """Test DELETE - Delete proposal item"""
    print(f"\n=== Testing DELETE /api/proposal-items/{item_id} ===")
    
    try:
        response = requests.delete(f"{BASE_URL}/{item_id}")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"✓ {response.json()['message']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")

if __name__ == "__main__":
    print("Testing ProposalItem API Endpoints")
    print("=" * 80)
    
    # Create a test proposal
    proposal_id = create_test_proposal()
    
    if proposal_id:
        # Add multiple items
        item1_id = test_add_proposal_item(proposal_id, "False Ceiling", 1500, 75.00)
        item2_id = test_add_proposal_item(proposal_id, "Gypsum Board", 800, 140.00)
        item3_id = test_add_proposal_item(proposal_id, "Flush Door", 4, 700.00)
        
        # Get all items for the proposal
        test_get_proposal_items(proposal_id)
        
        # Update an item
        if item1_id:
            test_update_proposal_item(item1_id)
        
        # Get items again to see the update
        test_get_proposal_items(proposal_id)
        
        # Delete an item
        if item3_id:
            test_delete_proposal_item(item3_id)
        
        # Final list
        test_get_proposal_items(proposal_id)
    
    print("\n" + "=" * 80)
    print("Testing completed!")
