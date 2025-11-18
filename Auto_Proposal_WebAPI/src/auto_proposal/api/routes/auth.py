"""
Authentication routes for login and user verification
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import bcrypt

from ...db.database import get_db
from ...core import models, schemas

router = APIRouter(prefix="/auth", tags=["Authentication"])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception as e:
        print(f"Password verification error: {e}")
        return False


def hash_password(password: str) -> str:
    """Hash a password for storing."""
    # Truncate password to 72 bytes for bcrypt
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')


@router.post("/login", response_model=schemas.LoginResponse, status_code=status.HTTP_200_OK)
def login(
    login_data: schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login endpoint with comprehensive validation.
    
    Validates:
    - Company exists and name matches
    - User exists with the provided email
    - User belongs to the specified company
    - Password is correct
    - User account is active
    - User has valid access (not expired)
    
    Returns:
    - Success response with user details and access information
    - Error response with specific validation failure message
    """
    
    # Step 1: Validate company exists
    company = db.query(models.CompanyDetails).filter(
        models.CompanyDetails.company_name == login_data.company_name
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "message": f"Company '{login_data.company_name}' not found",
                "error_code": "INVALID_COMPANY"
            }
        )
    
    # Step 2: Validate user exists with the provided email
    user = db.query(models.UserDetails).filter(
        models.UserDetails.email == login_data.email
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "message": f"User with email '{login_data.email}' not found",
                "error_code": "INVALID_USER"
            }
        )
    
    # Step 3: Validate user belongs to the specified company
    if user.company_id != company.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "success": False,
                "message": f"User does not belong to company '{login_data.company_name}'",
                "error_code": "COMPANY_MISMATCH"
            }
        )
    
    # Step 4: Validate password
    if not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "message": "Password not set for this user. Please contact administrator.",
                "error_code": "NO_PASSWORD"
            }
        )
    
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "message": "Invalid password",
                "error_code": "INVALID_PASSWORD"
            }
        )
    
    # Step 5: Validate user account is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "success": False,
                "message": "User account is deactivated. Please contact administrator.",
                "error_code": "ACCOUNT_INACTIVE"
            }
        )
    
    # Step 6: Check access expiration date
    access_granted = True
    access_message = "Login successful"
    
    if user.auto_proposal_access_end_date:
        current_date = datetime.now().date()
        if isinstance(user.auto_proposal_access_end_date, datetime):
            access_end_date = user.auto_proposal_access_end_date.date()
        else:
            access_end_date = user.auto_proposal_access_end_date
        
        if current_date > access_end_date:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "message": f"Access expired on {access_end_date}. Please renew subscription.",
                    "error_code": "ACCESS_EXPIRED"
                }
            )
        
        # Check if expiring soon (within 7 days)
        days_remaining = (access_end_date - current_date).days
        if days_remaining <= 7:
            access_message = f"Login successful. Access expires in {days_remaining} days."
    
    # Load user with company details
    user_with_company = db.query(models.UserDetails).filter(
        models.UserDetails.id == user.id
    ).first()
    
    return schemas.LoginResponse(
        success=True,
        message=access_message,
        user=user_with_company,
        access_granted=access_granted,
        access_end_date=user.auto_proposal_access_end_date
    )


@router.post("/set-password/{user_id}", status_code=status.HTTP_200_OK)
def set_password(
    user_id: int,
    password: str,
    db: Session = Depends(get_db)
):
    """
    Set or update password for a user.
    This is a utility endpoint for testing/admin purposes.
    """
    user = db.query(models.UserDetails).filter(models.UserDetails.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.password_hash = hash_password(password)
    db.commit()
    
    return {
        "success": True,
        "message": f"Password set successfully for user {user.email}"
    }
