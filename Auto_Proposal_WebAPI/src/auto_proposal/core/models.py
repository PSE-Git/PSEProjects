from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON, Enum, Text, Computed
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(255), nullable=False)
    business_type: Mapped[str] = Column(String(100))
    fee: Mapped[float] = Column(Float)
    pricing_plan: Mapped[str] = Column(String(50))
    notes: Mapped[Optional[str]] = Column(String(1000))
    email: Mapped[str] = Column(String(255))
    phone: Mapped[str] = Column(String(50))
    address: Mapped[Optional[str]] = Column(String(500))
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Proposal(Base):
    __tablename__ = "Proposal"

    id: Mapped[int] = Column('Id', Integer, primary_key=True, index=True, autoincrement=True)
    company_id: Mapped[Optional[int]] = Column('CompanyID', Integer, ForeignKey('CompanyDetails.CompanyID'))
    client_id: Mapped[int] = Column('ClientId', Integer, ForeignKey('ClientDetails.ClientID'), nullable=False)
    title: Mapped[str] = Column('Title', String(200), nullable=False)
    description: Mapped[Optional[str]] = Column('Description', Text)
    amount: Mapped[float] = Column('Amount', Float, nullable=False, default=0.00)
    status: Mapped[Optional[str]] = Column('Status', String(50), default='Draft')
    pdf_url: Mapped[Optional[str]] = Column('PdfUrl', String(255))
    created_date: Mapped[datetime] = Column('CreatedDate', DateTime, server_default="CURRENT_TIMESTAMP")
    modify_date: Mapped[datetime] = Column('ModifyDate', DateTime, server_default="CURRENT_TIMESTAMP", onupdate=datetime.utcnow)
    project_type: Mapped[Optional[str]] = Column('ProjectType', String(100))
    area: Mapped[Optional[str]] = Column('Area', String(50))
    material_preferences: Mapped[Optional[str]] = Column('MaterialPreferences', Text)
    special_requirement: Mapped[Optional[str]] = Column('SpecialRequirement', Text)

    company: Mapped[Optional['CompanyDetails']] = relationship('CompanyDetails')
    client: Mapped['ClientDetails'] = relationship('ClientDetails')

class ProposalItem(Base):
    __tablename__ = "ProposalItem"

    id: Mapped[int] = Column('Id', Integer, primary_key=True, index=True, autoincrement=True)
    proposal_id: Mapped[int] = Column('ProposalId', Integer, ForeignKey('Proposal.Id'), nullable=False)
    item_name: Mapped[str] = Column('ItemName', String(200), nullable=False)
    description: Mapped[Optional[str]] = Column('Description', Text)
    qty: Mapped[int] = Column('Qty', Integer, nullable=False, default=1)
    unit_price: Mapped[float] = Column('UnitPrice', Float, nullable=False, default=0.00)
    total: Mapped[Optional[float]] = Column('Total', Float, Computed('Qty * UnitPrice', persisted=True))

    proposal: Mapped['Proposal'] = relationship('Proposal')


class UserDetails(Base):
    __tablename__ = "UserDetails"

    id: Mapped[int] = Column("UserID", Integer, primary_key=True, index=True, autoincrement=True)
    company_id: Mapped[int] = Column("CompanyID", Integer, ForeignKey("CompanyDetails.CompanyID"), nullable=False)
    full_name: Mapped[str] = Column("FullName", String(100), nullable=False)
    designation: Mapped[Optional[str]] = Column("Designation", String(100))
    email: Mapped[str] = Column("Email", String(150), unique=True, nullable=False)
    phone: Mapped[Optional[str]] = Column("PhoneNumber", String(20))
    password_hash: Mapped[Optional[str]] = Column("PasswordHash", String(255))
    role: Mapped[str] = Column("Role", String(50), default="User")
    is_active: Mapped[bool] = Column("IsActive", Integer, default=1)
    auto_proposal_access_end_date: Mapped[Optional[datetime]] = Column("AutoProposalAccessEndDate", DateTime)
    created_at: Mapped[datetime] = Column("CreatedAt", DateTime, server_default="CURRENT_TIMESTAMP")
    updated_at: Mapped[datetime] = Column("UpdatedAt", DateTime, server_default="CURRENT_TIMESTAMP", onupdate=datetime.utcnow)

    company: Mapped["CompanyDetails"] = relationship("CompanyDetails", back_populates="users")

class CompanyDetails(Base):
    __tablename__ = "CompanyDetails"

    id: Mapped[int] = Column("CompanyID", Integer, primary_key=True, index=True, autoincrement=True)
    company_name: Mapped[str] = Column("CompanyName", String(150), nullable=False)
    industry_type: Mapped[Optional[str]] = Column("IndustryType", String(100))
    contact_person: Mapped[Optional[str]] = Column("ContactPerson", String(100))
    email: Mapped[Optional[str]] = Column("Email", String(150))
    phone: Mapped[Optional[str]] = Column("PhoneNumber", String(20))
    alternate_phone: Mapped[Optional[str]] = Column("AlternatePhone", String(20))
    address_line1: Mapped[Optional[str]] = Column("AddressLine1", String(255))
    address_line2: Mapped[Optional[str]] = Column("AddressLine2", String(255))
    city: Mapped[Optional[str]] = Column("City", String(100))
    state: Mapped[Optional[str]] = Column("State", String(100))
    country: Mapped[str] = Column("Country", String(100), server_default="India")
    postal_code: Mapped[Optional[str]] = Column("PostalCode", String(20))
    website: Mapped[Optional[str]] = Column("Website", String(150))
    gst_number: Mapped[Optional[str]] = Column("GSTNumber", String(30))
    pan_number: Mapped[Optional[str]] = Column("PANNumber", String(20))
    logo_url: Mapped[Optional[str]] = Column("LogoURL", String(255))
    subscription_type: Mapped[Optional[str]] = Column("SubscriptionType", String(50))
    subscription_start_date: Mapped[Optional[datetime]] = Column("SubscriptionStartDate", DateTime)
    subscription_end_date: Mapped[Optional[datetime]] = Column("SubscriptionEndDate", DateTime)
    created_at: Mapped[datetime] = Column("CreatedAt", DateTime, server_default="CURRENT_TIMESTAMP")
    updated_at: Mapped[datetime] = Column("UpdatedAt", DateTime, server_default="CURRENT_TIMESTAMP", onupdate=datetime.utcnow)

    users: Mapped[List["UserDetails"]] = relationship("UserDetails", back_populates="company")

class PseApBoqItems(Base):
    __tablename__ = 'PseApBoqItems'

    sno: Mapped[int] = Column('SNo', Integer, primary_key=True, index=True, autoincrement=True)
    company_id: Mapped[Optional[int]] = Column('CompanyID', Integer, ForeignKey('CompanyDetails.CompanyID'))
    project_type: Mapped[Optional[str]] = Column('ProjectType', String(100))
    title: Mapped[Optional[str]] = Column('Title', String(150))
    description: Mapped[Optional[str]] = Column('Description', String(1000))
    unit: Mapped[Optional[str]] = Column('Unit', String(50))
    basic_rate: Mapped[Optional[float]] = Column('BasicRate', Float)
    premium_rate: Mapped[Optional[float]] = Column('PremiumRate', Float)

    company: Mapped[Optional['CompanyDetails']] = relationship('CompanyDetails')


class ClientDetails(Base):
    __tablename__ = 'ClientDetails'

    id: Mapped[int] = Column('ClientID', Integer, primary_key=True, index=True, autoincrement=True)
    company_id: Mapped[Optional[int]] = Column('CompanyID', Integer, ForeignKey('CompanyDetails.CompanyID'))
    client_name: Mapped[str] = Column('ClientName', String(100), nullable=False)
    email_address: Mapped[Optional[str]] = Column('EmailAddress', String(150))
    mobile_number: Mapped[Optional[str]] = Column('MobileNumber', String(15))
    contact_address: Mapped[Optional[str]] = Column('ContactAddress', Text)
    create_date: Mapped[datetime] = Column('CreateDate', DateTime, server_default="CURRENT_TIMESTAMP")
    modified_date: Mapped[datetime] = Column('ModifiedDate', DateTime, server_default="CURRENT_TIMESTAMP", onupdate=datetime.utcnow)
    is_active: Mapped[Optional[bool]] = Column('IsActive', Integer, default=1)

    company: Mapped[Optional['CompanyDetails']] = relationship('CompanyDetails')
