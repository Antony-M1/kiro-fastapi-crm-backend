from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.lead import LeadSource, LeadStatus

class LeadBase(BaseModel):
    lead_name: str
    company_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: LeadSource = LeadSource.OTHER

class LeadCreate(LeadBase):
    assigned_to: Optional[int] = None

class LeadUpdate(BaseModel):
    lead_name: Optional[str] = None
    company_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: Optional[LeadSource] = None
    status: Optional[LeadStatus] = None
    assigned_to: Optional[int] = None

class LeadResponse(LeadBase):
    lead_id: int
    status: LeadStatus
    assigned_to: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True
