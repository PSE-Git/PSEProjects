"""
Test BOQ Items Project Types API endpoint
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/boq-items"

def test_get_project_types(company_id=1):
    """Test GET project types by company ID"""
    print(f"\n=== Testing GET /api/boq-items/project-types/{company_id} ===")
    try:
        response = requests.get(f"{BASE_URL}/project-types/{company_id}")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            project_types = response.json()
            print(f"Found {len(project_types)} distinct project types")
            print(f"Project Types: {json.dumps(project_types, indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")

def test_get_boq_items_by_project_type(company_id=1, project_type=None):
    """Test GET BOQ items filtered by company and project type"""
    print(f"\n=== Testing GET /api/boq-items/ (company_id={company_id}, project_type={project_type}) ===")
    try:
        params = {"company_id": company_id}
        if project_type:
            params["project_type"] = project_type
        
        response = requests.get(f"{BASE_URL}/", params=params)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            items = response.json()
            print(f"Found {len(items)} BOQ items")
            if items:
                print(f"First item: Title='{items[0]['title']}', ProjectType='{items[0]['project_type']}'")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")

if __name__ == "__main__":
    print("Testing BOQ Items Project Types API")
    print("=" * 50)
    
    # Test getting project types for company 1
    test_get_project_types(1)
    
    # Test getting BOQ items for first project type
    print("\n" + "=" * 50)
    
    # Get project types first, then test filtering by one
    response = requests.get(f"{BASE_URL}/project-types/1")
    if response.status_code == 200:
        project_types = response.json()
        if project_types:
            print(f"\nTesting with first project type: '{project_types[0]}'")
            test_get_boq_items_by_project_type(1, project_types[0])
    
    print("\n" + "=" * 50)
    print("Testing completed!")
