"""
ClientDetails API routes - CRUD operations for ClientDetails table
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from ...core import schemas, models
from ...db.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.ClientDetailsResponse, status_code=status.HTTP_201_CREATED)
def create_client(
    client: schemas.ClientDetailsCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new client.
    
    - **company_id**: Company ID (required)
    - **client_name**: Client name (required)
    - **email_address**: Email address
    - **mobile_number**: Mobile number
    - **contact_address**: Contact address
    - **is_active**: Active status (default: true)
    """
    db_client = models.ClientDetails(
        company_id=client.company_id,
        client_name=client.client_name,
        email_address=client.email_address,
        mobile_number=client.mobile_number,
        contact_address=client.contact_address,
        is_active=client.is_active if client.is_active is not None else True
    )
    
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    
    return db_client


@router.get("/{client_id}", response_model=schemas.ClientDetailsResponse)
def get_client_by_id(
    client_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific client by Client ID.
    """
    client = db.query(models.ClientDetails).filter(models.ClientDetails.id == client_id).first()
    
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} not found"
        )
    
    return client


@router.get("/company/{company_id}", response_model=List[schemas.ClientDetailsResponse])
def get_clients_by_company(
    company_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """
    Get all clients for a specific company.
    
    - **company_id**: Company ID to filter clients
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **is_active**: Filter by active status (true/false)
    """
    query = db.query(models.ClientDetails).filter(models.ClientDetails.company_id == company_id)
    
    if is_active is not None:
        query = query.filter(models.ClientDetails.is_active == is_active)
    
    clients = query.offset(skip).limit(limit).all()
    
    return clients


@router.put("/{client_id}", response_model=schemas.ClientDetailsResponse)
def update_client(
    client_id: int,
    client_update: schemas.ClientDetailsUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a client's information.
    
    Only provided fields will be updated. Fields set to None will be ignored.
    """
    db_client = db.query(models.ClientDetails).filter(models.ClientDetails.id == client_id).first()
    
    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} not found"
        )
    
    # Update only provided fields
    update_data = client_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_client, field, value)
    
    db.commit()
    db.refresh(db_client)
    
    return db_client


@router.delete("/{client_id}", status_code=status.HTTP_200_OK)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a client by Client ID.
    """
    db_client = db.query(models.ClientDetails).filter(models.ClientDetails.id == client_id).first()
    
    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} not found"
        )
    
    db.delete(db_client)
    db.commit()
    
    return {
        "success": True,
        "message": f"Client with ID {client_id} deleted successfully"
    }


@router.get("/", response_model=List[schemas.ClientDetailsResponse])
def get_all_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """
    Get all clients across all companies.
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **is_active**: Filter by active status
    """
    query = db.query(models.ClientDetails)
    
    if is_active is not None:
        query = query.filter(models.ClientDetails.is_active == is_active)
    
    clients = query.offset(skip).limit(limit).all()
    
    return clients


@router.patch("/{client_id}/activate", response_model=schemas.ClientDetailsResponse)
def activate_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    """
    Activate a client.
    """
    db_client = db.query(models.ClientDetails).filter(models.ClientDetails.id == client_id).first()
    
    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} not found"
        )
    
    db_client.is_active = True
    db.commit()
    db.refresh(db_client)
    
    return db_client


@router.patch("/{client_id}/deactivate", response_model=schemas.ClientDetailsResponse)
def deactivate_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    """
    Deactivate a client.
    """
    db_client = db.query(models.ClientDetails).filter(models.ClientDetails.id == client_id).first()
    
    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} not found"
        )
    
    db_client.is_active = False
    db.commit()
    db.refresh(db_client)
    
    return db_client
