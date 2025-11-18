"""
Add sample data to the database for testing
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from auto_proposal.db.database import SessionLocal, engine
from auto_proposal.core.models import Base, CompanyDetails, UserDetails, Client, Proposal, ProposalItem
import hashlib
from datetime import datetime

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def add_sample_data():
    """Add sample data to database"""
    db = SessionLocal()
    
    try:
        print("Adding sample data...")
        
        # Create Companies
        print("\n1. Creating companies...")
        company1 = CompanyDetails(
            company_name="Tech Solutions Inc",
            company_email="info@techsolutions.com",
            company_phone="+1234567890",
            address="123 Main Street",
            city="New York",
            state="NY",
            country="USA",
            postal_code="10001",
            website="https://techsolutions.com",
            tax_id="12-3456789",
            industry="Technology",
            description="Leading technology solutions provider",
            is_active=True
        )
        
        company2 = CompanyDetails(
            company_name="Creative Designs Ltd",
            company_email="hello@creativedesigns.com",
            company_phone="+9876543210",
            address="456 Design Avenue",
            city="Los Angeles",
            state="CA",
            country="USA",
            postal_code="90001",
            website="https://creativedesigns.com",
            tax_id="98-7654321",
            industry="Design",
            description="Creative design agency",
            is_active=True
        )
        
        db.add(company1)
        db.add(company2)
        db.commit()
        db.refresh(company1)
        db.refresh(company2)
        print(f"   ✅ Created company: {company1.company_name} (ID: {company1.id})")
        print(f"   ✅ Created company: {company2.company_name} (ID: {company2.id})")
        
        # Create Users
        print("\n2. Creating users...")
        user1 = UserDetails(
            username="admin",
            email="admin@techsolutions.com",
            full_name="Admin User",
            password_hash=hash_password("admin123"),
            phone="+1111111111",
            role="admin",
            is_active=True,
            company_id=company1.id
        )
        
        user2 = UserDetails(
            username="johndoe",
            email="john.doe@techsolutions.com",
            full_name="John Doe",
            password_hash=hash_password("password123"),
            phone="+2222222222",
            role="user",
            is_active=True,
            company_id=company1.id
        )
        
        user3 = UserDetails(
            username="janedoe",
            email="jane.doe@creativedesigns.com",
            full_name="Jane Doe",
            password_hash=hash_password("password123"),
            phone="+3333333333",
            role="manager",
            is_active=True,
            company_id=company2.id
        )
        
        db.add(user1)
        db.add(user2)
        db.add(user3)
        db.commit()
        db.refresh(user1)
        db.refresh(user2)
        db.refresh(user3)
        print(f"   ✅ Created user: {user1.username} (ID: {user1.id})")
        print(f"   ✅ Created user: {user2.username} (ID: {user2.id})")
        print(f"   ✅ Created user: {user3.username} (ID: {user3.id})")
        
        # Create Clients
        print("\n3. Creating clients...")
        client1 = Client(
            name="ABC Salon",
            business_type="Salon",
            fee=1500.0,
            pricing_plan="Premium",
            notes="VIP customer",
            email="contact@abcsalon.com",
            phone="+4444444444",
            address="789 Beauty Lane"
        )
        
        client2 = Client(
            name="XYZ Restaurant",
            business_type="Restaurant",
            fee=2000.0,
            pricing_plan="Enterprise",
            notes="High-value client",
            email="info@xyzrestaurant.com",
            phone="+5555555555",
            address="321 Food Street"
        )
        
        db.add(client1)
        db.add(client2)
        db.commit()
        db.refresh(client1)
        db.refresh(client2)
        print(f"   ✅ Created client: {client1.name} (ID: {client1.id})")
        print(f"   ✅ Created client: {client2.name} (ID: {client2.id})")
        
        # Create Proposals
        print("\n4. Creating proposals...")
        proposal1 = Proposal(
            client_id=client1.id,
            title="Website Redesign Proposal",
            description="Complete website redesign and modernization",
            amount=5000.0,
            items={},
            status="Draft"
        )
        
        db.add(proposal1)
        db.commit()
        db.refresh(proposal1)
        print(f"   ✅ Created proposal: {proposal1.title} (ID: {proposal1.id})")
        
        # Create Proposal Items
        print("\n5. Creating proposal items...")
        item1 = ProposalItem(
            proposal_id=proposal1.id,
            item_name="Design",
            description="UI/UX Design",
            quantity=1,
            unit_price=2000.0,
            total=2000.0
        )
        
        item2 = ProposalItem(
            proposal_id=proposal1.id,
            item_name="Development",
            description="Frontend and Backend Development",
            quantity=1,
            unit_price=3000.0,
            total=3000.0
        )
        
        db.add(item1)
        db.add(item2)
        db.commit()
        print(f"   ✅ Created {2} proposal items")
        
        print("\n" + "=" * 60)
        print("✅ Sample data added successfully!")
        print("=" * 60)
        
        print("\nSummary:")
        print(f"  - Companies: 2")
        print(f"  - Users: 3")
        print(f"  - Clients: 2")
        print(f"  - Proposals: 1")
        print(f"  - Proposal Items: 2")
        
        print("\nYou can now test the API at: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"\n❌ Error adding sample data: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_data()
