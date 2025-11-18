"""Detailed error checking for ClientDetails API"""
import requests
import json

BASE_URL = "http://localhost:8000/api/clients"

print("Testing GET /api/clients/")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print(f"Headers: {dict(response.headers)}")
except Exception as e:
    print(f"Error: {e}")
