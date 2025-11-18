import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from auto_proposal.api.main import app
from auto_proposal.db.database import Base, get_db
from auto_proposal.core.schemas import ClientCreate, ProposalCreate, ProposalItemCreate

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

def test_create_client(client):
    client_data = {
        "name": "Test Client",
        "business_type": "Salon",
        "fee": 1000.0,
        "pricing_plan": "Premium",
        "notes": "Test notes",
        "email": "test@example.com",
        "phone": "1234567890",
        "address": "Test Address"
    }
    response = client.post("/api/clients/", json=client_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == client_data["name"]
    assert data["email"] == client_data["email"]

def test_create_proposal(client):
    # First create a client
    client_data = {
        "name": "Test Client",
        "business_type": "Salon",
        "fee": 1000.0,
        "pricing_plan": "Premium",
        "notes": "Test notes",
        "email": "test@example.com",
        "phone": "1234567890",
        "address": "Test Address"
    }
    client_response = client.post("/api/clients/", json=client_data)
    client_id = client_response.json()["id"]

    # Create proposal
    proposal_data = {
        "client_id": client_id,
        "title": "Test Proposal",
        "description": "Test Description",
        "amount": 5000.0,
        "items": {},
        "status": "Draft",
        "proposal_items": [
            {
                "item_name": "Test Item",
                "description": "Test Item Description",
                "quantity": 2,
                "unit_price": 2500.0
            }
        ]
    }
    response = client.post("/api/proposals/", json=proposal_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == proposal_data["title"]
    assert data["amount"] == proposal_data["amount"]
    assert len(data["proposal_items"]) == 1