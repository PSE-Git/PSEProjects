"""Simple test for ProposalItem creation"""
import requests
import json

data = {
    "proposal_id": 1,
    "item_name": "Test Item",
    "qty": 2,
    "unit_price": 100.50
}

print("Testing POST /api/proposal-items/")
print(f"Data: {json.dumps(data, indent=2)}")

response = requests.post(
    "http://localhost:8000/api/proposal-items/",
    json=data
)

print(f"\nStatus Code: {response.status_code}")
print(f"Response: {response.text}")
