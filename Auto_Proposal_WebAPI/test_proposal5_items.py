"""Test the proposal items API endpoint"""
import requests

response = requests.get('http://localhost:8000/api/proposal-items/proposal/5')

print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    items = response.json()
    print(f"\n✓ Successfully retrieved {len(items)} items for Proposal ID 5")
    print("\nItems Details:")
    print("-" * 60)
    
    for i, item in enumerate(items, 1):
        print(f"\n{i}. {item['item_name']}")
        print(f"   Quantity: {item['qty']}")
        print(f"   Unit Price: ₹{item['unit_price']}")
        print(f"   Total: ₹{item['total']}")
else:
    print(f"\n✗ Error: {response.text}")
