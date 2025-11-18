"""
Proposal API routes - CRUD operations for Proposal table
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from ...core import schemas, models
from ...db.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.ProposalResponse, status_code=status.HTTP_201_CREATED)
def create_proposal(
    proposal: schemas.ProposalCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new proposal.
    
    - **company_id**: Company ID (required)
    - **client_id**: Client ID (required)
    - **title**: Proposal title (required)
    - **description**: Proposal description
    - **amount**: Total amount (default: 0.00)
    - **status**: Status (default: 'Draft')
    - **project_type**: Type of project
    - **area**: Area details
    - **material_preferences**: Material preferences
    - **special_requirement**: Special requirements
    """
    db_proposal = models.Proposal(
        company_id=proposal.company_id,
        client_id=proposal.client_id,
        title=proposal.title,
        description=proposal.description,
        amount=proposal.amount,
        status=proposal.status or 'Draft',
        project_type=proposal.project_type,
        area=proposal.area,
        material_preferences=proposal.material_preferences,
        special_requirement=proposal.special_requirement
    )
    
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    
    return db_proposal


@router.get("/{proposal_id}", response_model=schemas.ProposalResponse)
def get_proposal_by_id(
    proposal_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific proposal by Proposal ID.
    """
    proposal = db.query(models.Proposal).filter(models.Proposal.id == proposal_id).first()
    
    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proposal with ID {proposal_id} not found"
        )
    
    return proposal


@router.get("/company/{company_id}", response_model=List[schemas.ProposalResponse])
def get_proposals_by_company(
    company_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = Query(None, description="Filter by status (Draft, Sent, Approved, Rejected)"),
    db: Session = Depends(get_db)
):
    """
    Get all proposals for a specific company.
    
    - **company_id**: Company ID to filter proposals
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **status**: Filter by status
    """
    query = db.query(models.Proposal).filter(models.Proposal.company_id == company_id)
    
    if status:
        query = query.filter(models.Proposal.status == status)
    
    proposals = query.order_by(models.Proposal.created_date.desc()).offset(skip).limit(limit).all()
    
    return proposals


@router.get("/client/{client_id}", response_model=List[schemas.ProposalResponse])
def get_proposals_by_client(
    client_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Get all proposals for a specific client.
    
    - **client_id**: Client ID to filter proposals
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    proposals = db.query(models.Proposal).filter(
        models.Proposal.client_id == client_id
    ).order_by(models.Proposal.created_date.desc()).offset(skip).limit(limit).all()
    
    return proposals


@router.put("/{proposal_id}", response_model=schemas.ProposalResponse)
def update_proposal(
    proposal_id: int,
    proposal_update: schemas.ProposalUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a proposal's information.
    
    Only provided fields will be updated. Fields set to None will be ignored.
    """
    db_proposal = db.query(models.Proposal).filter(models.Proposal.id == proposal_id).first()
    
    if not db_proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proposal with ID {proposal_id} not found"
        )
    
    # Update only provided fields
    update_data = proposal_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_proposal, field, value)
    
    db.commit()
    db.refresh(db_proposal)
    
    return db_proposal


@router.delete("/{proposal_id}", status_code=status.HTTP_200_OK)
def delete_proposal(
    proposal_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a proposal by Proposal ID.
    """
    db_proposal = db.query(models.Proposal).filter(models.Proposal.id == proposal_id).first()
    
    if not db_proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proposal with ID {proposal_id} not found"
        )
    
    db.delete(db_proposal)
    db.commit()
    
    return {
        "success": True,
        "message": f"Proposal with ID {proposal_id} deleted successfully"
    }


@router.get("/", response_model=List[schemas.ProposalResponse])
def get_all_proposals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """
    Get all proposals across all companies.
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **status**: Filter by status
    """
    query = db.query(models.Proposal)
    
    if status:
        query = query.filter(models.Proposal.status == status)
    
    proposals = query.order_by(models.Proposal.created_date.desc()).offset(skip).limit(limit).all()
    
    return proposals


@router.patch("/{proposal_id}/status/{new_status}", response_model=schemas.ProposalResponse)
def update_proposal_status(
    proposal_id: int,
    new_status: str,
    db: Session = Depends(get_db)
):
    """
    Update proposal status.
    
    Valid statuses: Draft, Sent, Approved, Rejected
    """
    valid_statuses = ['Draft', 'Sent', 'Approved', 'Rejected']
    
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    db_proposal = db.query(models.Proposal).filter(models.Proposal.id == proposal_id).first()
    
    if not db_proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proposal with ID {proposal_id} not found"
        )
    
    db_proposal.status = new_status
    db.commit()
    db.refresh(db_proposal)
    
    return db_proposal

    if db_proposal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposal not found"
        )
    
    if not db_proposal.pdf_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF not generated for this proposal"
        )

    pdf_path = os.path.join(pdf_service.output_dir, os.path.basename(db_proposal.pdf_url))
    if not os.path.exists(pdf_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF file not found"
        )

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"proposal_{proposal_id}.pdf"
    )