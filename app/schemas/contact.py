from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ContactBase(BaseModel):
    contact_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class ContactCreate(ContactBase):
    linked_customer_id: Optional[int] = None

class ContactUpdate(BaseModel):
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    linked_customer_id: Optional[int] = None

class ContactResponse(ContactBase):
    contact_id: int
    linked_customer_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True
