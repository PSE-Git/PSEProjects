"""Test Proposal model query"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

print("Importing modules...")
from src.auto_proposal.db.database import SessionLocal
from src.auto_proposal.core.models import Proposal

print("Testing Proposal model query...")

try:
    db = SessionLocal()
    print("✓ Database session created")
    
    # Try to query Proposal
    print("Querying Proposal...")
    proposals = db.query(Proposal).limit(5).all()
    print(f"✓ Query successful! Found {len(proposals)} proposals")
    
    if proposals:
        for proposal in proposals:
            print(f"  - Proposal ID: {proposal.id}, Title: {proposal.title}, Company ID: {proposal.company_id}, Status: {proposal.status}")
    else:
        print("  No proposals found in database")
    
    db.close()
    print("✓ Test completed successfully!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
