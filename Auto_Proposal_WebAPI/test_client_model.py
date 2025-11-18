"""Test ClientDetails model query"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

print("Importing modules...")
from src.auto_proposal.db.database import SessionLocal
from src.auto_proposal.core.models import ClientDetails

print("Testing ClientDetails model query...")

try:
    db = SessionLocal()
    print("✓ Database session created")
    
    # Try to query ClientDetails
    print("Querying ClientDetails...")
    clients = db.query(ClientDetails).limit(5).all()
    print(f"✓ Query successful! Found {len(clients)} clients")
    
    if clients:
        for client in clients:
            print(f"  - Client ID: {client.id}, Name: {client.client_name}, Company ID: {client.company_id}")
    else:
        print("  No clients found in database")
    
    db.close()
    print("✓ Test completed successfully!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
