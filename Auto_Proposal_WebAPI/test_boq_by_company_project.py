"""Test BOQ Items by Company and Project Type"""
import requests
import json

response = requests.get(
    'http://localhost:8000/api/boq-items/',
    params={'company_id': 1, 'project_type': 'Gym'}
)

print(f"Status Code: {response.status_code}")
print(f"\nQuery: SELECT * FROM PseApBoqItems WHERE CompanyID = 1 AND ProjectType = 'Gym'")
print("=" * 80)

if response.status_code == 200:
    items = response.json()
    print(f"\nFound {len(items)} BOQ items")
    print("\nItems Details:")
    print("-" * 80)
    
    for i, item in enumerate(items, 1):
        print(f"\n{i}. {item['title']}")
        print(f"   SNo: {item['sno']}")
        print(f"   Description: {item['description'][:100]}..." if len(item['description']) > 100 else f"   Description: {item['description']}")
        print(f"   Unit: {item['unit']}")
        print(f"   Basic Rate: ₹{item['basic_rate']}")
        print(f"   Premium Rate: ₹{item['premium_rate']}")
        print(f"   Company ID: {item['company_id']}")
        print(f"   Project Type: {item['project_type']}")
else:
    print(f"Error: {response.text}")

print("\n" + "=" * 80)
