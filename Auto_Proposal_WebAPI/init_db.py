"""
Initialize the database with all tables
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from auto_proposal.db.database import engine
from auto_proposal.core.models import Base

def init_db():
    """Create all database tables"""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        print("\nCreated tables:")
        print("  - clients")
        print("  - proposals")
        print("  - proposal_items")
        print("  - user_details")
        print("  - company_details")
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        raise

if __name__ == "__main__":
    init_db()
