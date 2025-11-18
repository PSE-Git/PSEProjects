"""Test creating ProposalItem directly"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from src.auto_proposal.db.database import SessionLocal
from src.auto_proposal.core.models import ProposalItem

print("Testing ProposalItem creation...")

try:
    db = SessionLocal()
    print("✓ Database session created")
    
    # Create a test item
    item = ProposalItem(
        proposal_id=1,
        item_name="Test Item",
        description="Test Description",
        qty=2,
        unit_price=100.50
    )
    
    print("Adding item to session...")
    db.add(item)
    
    print("Committing...")
    db.commit()
    
    print("Refreshing...")
    db.refresh(item)
    
    print(f"✓ Successfully created item!")
    print(f"  ID: {item.id}")
    print(f"  Name: {item.item_name}")
    print(f"  Qty: {item.qty}")
    print(f"  Unit Price: {item.unit_price}")
    print(f"  Total: {item.total}")
    
    db.close()
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
