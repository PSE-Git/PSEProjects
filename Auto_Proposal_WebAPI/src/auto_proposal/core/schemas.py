from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel, EmailStr, Field, validator

if TYPE_CHECKING:
    from typing import ForwardRef

# ==================== ProposalItem Schemas ====================
class ProposalItemBase(BaseModel):
    item_name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    qty: int = Field(default=1, ge=1)
    unit_price: float = Field(..., ge=0)

class ProposalItemCreate(ProposalItemBase):
    proposal_id: int

class ProposalItemUpdate(BaseModel):
    item_name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    qty: Optional[int] = Field(None, ge=1)
    unit_price: Optional[float] = Field(None, ge=0)

class ProposalItemResponse(ProposalItemBase):
    id: int
    proposal_id: int
    total: Optional[float] = None

    class Config:
        from_attributes = True

# ==================== Client Schemas (Old - for backward compatibility) ====================
class ClientBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    business_type: str = Field(..., max_length=100)
    fee: float = Field(..., ge=0)
    pricing_plan: str = Field(..., max_length=50)
    notes: Optional[str] = Field(None, max_length=1000)
    email: EmailStr
    phone: str = Field(..., max_length=50)
    address: Optional[str] = Field(None, max_length=500)

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# UserDetails Schemas
class UserDetailsBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    designation: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    role: str = Field(default="User", max_length=50)
    is_active: bool = True
    company_id: int
    auto_proposal_access_end_date: Optional[datetime] = None

class UserDetailsCreate(UserDetailsBase):
    password: str = Field(..., min_length=6)

class UserDetailsUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    designation: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    role: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None
    company_id: Optional[int] = None
    password: Optional[str] = Field(None, min_length=6)
    auto_proposal_access_end_date: Optional[datetime] = None

class UserDetailsResponse(UserDetailsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# CompanyDetails Schemas
class CompanyDetailsBase(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=150)
    industry_type: Optional[str] = Field(None, max_length=100)
    contact_person: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    alternate_phone: Optional[str] = Field(None, max_length=20)
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: str = Field(default="India", max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=150)
    gst_number: Optional[str] = Field(None, max_length=30)
    pan_number: Optional[str] = Field(None, max_length=20)
    logo_url: Optional[str] = Field(None, max_length=255)
    subscription_type: Optional[str] = Field(None, max_length=50)
    subscription_start_date: Optional[datetime] = None
    subscription_end_date: Optional[datetime] = None
class CompanyDetailsCreate(CompanyDetailsBase):
    pass

class CompanyDetailsUpdate(BaseModel):
    company_name: Optional[str] = Field(None, min_length=1, max_length=150)
    industry_type: Optional[str] = Field(None, max_length=100)
    contact_person: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    alternate_phone: Optional[str] = Field(None, max_length=20)
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=150)
    gst_number: Optional[str] = Field(None, max_length=30)
    pan_number: Optional[str] = Field(None, max_length=20)
    logo_url: Optional[str] = Field(None, max_length=255)
    subscription_type: Optional[str] = Field(None, max_length=50)
    subscription_start_date: Optional[datetime] = None
    subscription_end_date: Optional[datetime] = None

class CompanyDetailsResponse(CompanyDetailsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CompanyDetailsWithUsers(CompanyDetailsResponse):
    users: List[UserDetailsResponse] = []

    class Config:
        from_attributes = True

# UserDetailsWithCompany must be defined after CompanyDetailsResponse
class UserDetailsWithCompany(UserDetailsResponse):
    company: Optional[CompanyDetailsResponse] = None

    class Config:
        from_attributes = True
# Login Schemas
class LoginRequest(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=150, description='Company name')
    email: EmailStr = Field(..., description='User email address')
    password: str = Field(..., min_length=1, description='User password')

class LoginResponse(BaseModel):
    success: bool
    message: str
    user: Optional[UserDetailsWithCompany] = None
    access_granted: bool = False
    access_end_date: Optional[datetime] = None

# PseApBoqItems Schemas
class BoqItemBase(BaseModel):
    company_id: Optional[int] = None
    project_type: Optional[str] = Field(None, max_length=100)
    title: Optional[str] = Field(None, max_length=150)
    description: Optional[str] = None
    unit: Optional[str] = Field(None, max_length=50)
    basic_rate: Optional[float] = Field(None, ge=0)
    premium_rate: Optional[float] = Field(None, ge=0)

class BoqItemCreate(BoqItemBase):
    pass

class BoqItemUpdate(BaseModel):
    company_id: Optional[int] = None
    project_type: Optional[str] = Field(None, max_length=100)
    title: Optional[str] = Field(None, max_length=150)
    description: Optional[str] = None
    unit: Optional[str] = Field(None, max_length=50)
    basic_rate: Optional[float] = Field(None, ge=0)
    premium_rate: Optional[float] = Field(None, ge=0)

class BoqItemResponse(BoqItemBase):
    sno: int

    class Config:
        from_attributes = True


# ClientDetails Schemas
class ClientDetailsBase(BaseModel):
    company_id: Optional[int] = None
    client_name: str = Field(..., max_length=100)
    email_address: Optional[EmailStr] = None
    mobile_number: Optional[str] = Field(None, max_length=15)
    contact_address: Optional[str] = None
    is_active: Optional[bool] = True

class ClientDetailsCreate(ClientDetailsBase):
    company_id: int  # Required for creation

class ClientDetailsUpdate(BaseModel):
    client_name: Optional[str] = Field(None, max_length=100)
    email_address: Optional[EmailStr] = None
    mobile_number: Optional[str] = Field(None, max_length=15)
    contact_address: Optional[str] = None
    is_active: Optional[bool] = None

class ClientDetailsResponse(ClientDetailsBase):
    id: int
    create_date: datetime
    modified_date: datetime

    class Config:
        from_attributes = True


# ==================== Proposal Schemas ====================
class ProposalBase(BaseModel):
    company_id: int
    client_id: int
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    amount: float = Field(default=0.00, ge=0)
    status: Optional[str] = Field(default='Draft', max_length=50)
    project_type: Optional[str] = Field(None, max_length=100)
    area: Optional[str] = Field(None, max_length=50)
    material_preferences: Optional[str] = None
    special_requirement: Optional[str] = None

class ProposalCreate(ProposalBase):
    pass

class ProposalUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    amount: Optional[float] = Field(None, ge=0)
    status: Optional[str] = Field(None, max_length=50)
    project_type: Optional[str] = Field(None, max_length=100)
    area: Optional[str] = Field(None, max_length=50)
    material_preferences: Optional[str] = None
    special_requirement: Optional[str] = None
    pdf_url: Optional[str] = Field(None, max_length=255)

class ProposalResponse(ProposalBase):
    id: int
    pdf_url: Optional[str] = None
    created_date: datetime
    modify_date: datetime

    class Config:
        from_attributes = True
