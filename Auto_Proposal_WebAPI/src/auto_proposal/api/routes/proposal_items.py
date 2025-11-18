"""
ProposalItem API routes - CRUD operations for ProposalItem table
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from ...core import schemas, models
from ...db.database import get_db

router = APIRouter(prefix="/api/proposal-items", tags=["Proposal Items"])


@router.post("/", response_model=schemas.ProposalItemResponse, status_code=status.HTTP_201_CREATED)
def create_proposal_item(
    item: schemas.ProposalItemCreate,
    db: Session = Depends(get_db)
):
    """
    Add a new item to a proposal.
    
    - **proposal_id**: Proposal ID (required)
    - **item_name**: Item name (required)
    - **description**: Item description
    - **qty**: Quantity (default: 1)
    - **unit_price**: Unit price (required)
    
    Note: Total is auto-calculated in the database (Qty * UnitPrice)
    """
    # Verify proposal exists
    proposal = db.query(models.Proposal).filter(models.Proposal.id == item.proposal_id).first()
    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proposal with ID {item.proposal_id} not found"
        )
    
    db_item = models.ProposalItem(
        proposal_id=item.proposal_id,
        item_name=item.item_name,
        description=item.description,
        qty=item.qty,
        unit_price=item.unit_price
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return db_item


@router.get("/proposal/{proposal_id}", response_model=List[schemas.ProposalItemResponse])
def get_proposal_items(
    proposal_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all items for a specific proposal.
    
    - **proposal_id**: Proposal ID to get items for
    """
    # Verify proposal exists
    proposal = db.query(models.Proposal).filter(models.Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proposal with ID {proposal_id} not found"
        )
    
    items = db.query(models.ProposalItem).filter(
        models.ProposalItem.proposal_id == proposal_id
    ).all()
    
    return items


@router.get("/{item_id}", response_model=schemas.ProposalItemResponse)
def get_proposal_item_by_id(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific proposal item by ID.
    """
    item = db.query(models.ProposalItem).filter(models.ProposalItem.id == item_id).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proposal item with ID {item_id} not found"
        )
    
    return item


@router.put("/{item_id}", response_model=schemas.ProposalItemResponse)
def update_proposal_item(
    item_id: int,
    item_update: schemas.ProposalItemUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a proposal item.
    
    Only provided fields will be updated. Total will be recalculated automatically.
    """
    db_item = db.query(models.ProposalItem).filter(models.ProposalItem.id == item_id).first()
    
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proposal item with ID {item_id} not found"
        )
    
    # Update only provided fields
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def delete_proposal_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a proposal item.
    """
    db_item = db.query(models.ProposalItem).filter(models.ProposalItem.id == item_id).first()
    
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proposal item with ID {item_id} not found"
        )
    
    db.delete(db_item)
    db.commit()
    
    return {
        "success": True,
        "message": f"Proposal item with ID {item_id} deleted successfully"
    }
