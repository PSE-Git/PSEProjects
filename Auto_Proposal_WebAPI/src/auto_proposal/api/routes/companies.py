from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...db.database import get_db
from ...core import schemas, models

router = APIRouter(
    prefix="/api/companies",
    tags=["Companies"]
)

@router.post("/", response_model=schemas.CompanyDetailsResponse, status_code=status.HTTP_201_CREATED)
def create_company(company: schemas.CompanyDetailsCreate, db: Session = Depends(get_db)):
    """
    Create a new company
    """
    # Check if company email already exists
    existing_company = db.query(models.CompanyDetails).filter(
        models.CompanyDetails.company_email == company.company_email
    ).first()
    
    if existing_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company email already exists"
        )
    
    # Create company
    db_company = models.CompanyDetails(**company.model_dump())
    
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    
    return db_company

@router.get("/", response_model=List[schemas.CompanyDetailsResponse])
def get_companies(
    skip: int = 0,
    limit: int = 100,
    is_active: bool = None,
    industry: str = None,
    city: str = None,
    db: Session = Depends(get_db)
):
    """
    Get all companies with optional filtering
    """
    query = db.query(models.CompanyDetails)
    
    if is_active is not None:
        query = query.filter(models.CompanyDetails.is_active == is_active)
    
    if industry:
        query = query.filter(models.CompanyDetails.industry == industry)
    
    if city:
        query = query.filter(models.CompanyDetails.city == city)
    
    companies = query.offset(skip).limit(limit).all()
    return companies

@router.get("/{company_id}", response_model=schemas.CompanyDetailsWithUsers)
def get_company(company_id: int, db: Session = Depends(get_db)):
    """
    Get a specific company by ID with associated users
    """
    company = db.query(models.CompanyDetails).filter(
        models.CompanyDetails.id == company_id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {company_id} not found"
        )
    
    return company

@router.put("/{company_id}", response_model=schemas.CompanyDetailsResponse)
def update_company(
    company_id: int,
    company_update: schemas.CompanyDetailsUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a company
    """
    db_company = db.query(models.CompanyDetails).filter(
        models.CompanyDetails.id == company_id
    ).first()
    
    if not db_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {company_id} not found"
        )
    
    # Update fields
    update_data = company_update.model_dump(exclude_unset=True)
    
    # Check email uniqueness if being updated
    if "company_email" in update_data and update_data["company_email"] != db_company.company_email:
        existing_email = db.query(models.CompanyDetails).filter(
            models.CompanyDetails.company_email == update_data["company_email"],
            models.CompanyDetails.id != company_id
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company email already exists"
            )
    
    for field, value in update_data.items():
        setattr(db_company, field, value)
    
    db.commit()
    db.refresh(db_company)
    
    return db_company

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    """
    Delete a company
    """
    db_company = db.query(models.CompanyDetails).filter(
        models.CompanyDetails.id == company_id
    ).first()
    
    if not db_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {company_id} not found"
        )
    
    # Check if company has associated users
    user_count = db.query(models.UserDetails).filter(
        models.UserDetails.company_id == company_id
    ).count()
    
    if user_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete company with {user_count} associated users. Please remove or reassign users first."
        )
    
    db.delete(db_company)
    db.commit()
    
    return None

@router.patch("/{company_id}/deactivate", response_model=schemas.CompanyDetailsResponse)
def deactivate_company(company_id: int, db: Session = Depends(get_db)):
    """
    Deactivate a company
    """
    db_company = db.query(models.CompanyDetails).filter(
        models.CompanyDetails.id == company_id
    ).first()
    
    if not db_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {company_id} not found"
        )
    
    db_company.is_active = False
    db.commit()
    db.refresh(db_company)
    
    return db_company

@router.patch("/{company_id}/activate", response_model=schemas.CompanyDetailsResponse)
def activate_company(company_id: int, db: Session = Depends(get_db)):
    """
    Activate a company
    """
    db_company = db.query(models.CompanyDetails).filter(
        models.CompanyDetails.id == company_id
    ).first()
    
    if not db_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {company_id} not found"
        )
    
    db_company.is_active = True
    db.commit()
    db.refresh(db_company)
    
    return db_company

@router.get("/{company_id}/users", response_model=List[schemas.UserDetailsResponse])
def get_company_users(company_id: int, db: Session = Depends(get_db)):
    """
    Get all users belonging to a specific company
    """
    # Check if company exists
    company = db.query(models.CompanyDetails).filter(
        models.CompanyDetails.id == company_id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {company_id} not found"
        )
    
    users = db.query(models.UserDetails).filter(
        models.UserDetails.company_id == company_id
    ).all()
    
    return users

@router.get("/search/name/{name}", response_model=List[schemas.CompanyDetailsResponse])
def search_companies_by_name(name: str, db: Session = Depends(get_db)):
    """
    Search companies by name (partial match)
    """
    companies = db.query(models.CompanyDetails).filter(
        models.CompanyDetails.company_name.ilike(f"%{name}%")
    ).all()
    
    return companies
