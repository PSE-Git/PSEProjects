"""Test ProposalItem model query"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

print("Importing modules...")
from src.auto_proposal.db.database import SessionLocal
from src.auto_proposal.core.models import ProposalItem

print("Testing ProposalItem model query...")

try:
    db = SessionLocal()
    print("✓ Database session created")
    
    # Try to query ProposalItem
    print("Querying ProposalItem...")
    items = db.query(ProposalItem).limit(5).all()
    print(f"✓ Query successful! Found {len(items)} proposal items")
    
    if items:
        for item in items:
            print(f"  - Item ID: {item.id}, Name: {item.item_name}, Proposal ID: {item.proposal_id}, Qty: {item.qty}, Total: {item.total}")
    else:
        print("  No proposal items found in database")
    
    db.close()
    print("✓ Test completed successfully!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
