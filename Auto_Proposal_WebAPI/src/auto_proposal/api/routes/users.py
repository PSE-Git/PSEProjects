from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import hashlib

from ...db.database import get_db
from ...core import schemas, models

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

def hash_password(password: str) -> str:
    """Simple password hashing - in production use bcrypt or passlib"""
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/", response_model=schemas.UserDetailsResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserDetailsCreate, db: Session = Depends(get_db)):
    """
    Create a new user
    """
    # Check if username already exists
    existing_user = db.query(models.UserDetails).filter(
        models.UserDetails.username == user.username
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Check if email already exists
    existing_email = db.query(models.UserDetails).filter(
        models.UserDetails.email == user.email
    ).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    # Hash the password
    password_hash = hash_password(user.password)
    
    # Create user
    db_user = models.UserDetails(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        password_hash=password_hash,
        phone=user.phone,
        role=user.role,
        is_active=user.is_active,
        company_id=user.company_id
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.get("/", response_model=List[schemas.UserDetailsResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    is_active: bool = None,
    role: str = None,
    db: Session = Depends(get_db)
):
    """
    Get all users with optional filtering
    """
    query = db.query(models.UserDetails)
    
    if is_active is not None:
        query = query.filter(models.UserDetails.is_active == is_active)
    
    if role:
        query = query.filter(models.UserDetails.role == role)
    
    users = query.offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=schemas.UserDetailsWithCompany)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by ID with company details
    """
    user = db.query(models.UserDetails).filter(models.UserDetails.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    return user

@router.put("/{user_id}", response_model=schemas.UserDetailsResponse)
def update_user(user_id: int, user_update: schemas.UserDetailsUpdate, db: Session = Depends(get_db)):
    """
    Update a user
    """
    db_user = db.query(models.UserDetails).filter(models.UserDetails.id == user_id).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # Update fields
    update_data = user_update.model_dump(exclude_unset=True)
    
    # If password is being updated, hash it
    if "password" in update_data:
        update_data["password_hash"] = hash_password(update_data.pop("password"))
    
    # Check email uniqueness if being updated
    if "email" in update_data and update_data["email"] != db_user.email:
        existing_email = db.query(models.UserDetails).filter(
            models.UserDetails.email == update_data["email"],
            models.UserDetails.id != user_id
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user
    """
    db_user = db.query(models.UserDetails).filter(models.UserDetails.id == user_id).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    db.delete(db_user)
    db.commit()
    
    return None

@router.get("/username/{username}", response_model=schemas.UserDetailsWithCompany)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """
    Get a user by username
    """
    user = db.query(models.UserDetails).filter(models.UserDetails.username == username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username '{username}' not found"
        )
    
    return user

@router.patch("/{user_id}/deactivate", response_model=schemas.UserDetailsResponse)
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    """
    Deactivate a user account
    """
    db_user = db.query(models.UserDetails).filter(models.UserDetails.id == user_id).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    db_user.is_active = False
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.patch("/{user_id}/activate", response_model=schemas.UserDetailsResponse)
def activate_user(user_id: int, db: Session = Depends(get_db)):
    """
    Activate a user account
    """
    db_user = db.query(models.UserDetails).filter(models.UserDetails.id == user_id).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    db_user.is_active = True
    db.commit()
    db.refresh(db_user)
    
    return db_user
