from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.customer import CustomerType

class CustomerBase(BaseModel):
    customer_name: str
    customer_type: CustomerType = CustomerType.INDIVIDUAL
    territory: Optional[str] = None
    industry: Optional[str] = None
    credit_limit: float = 0.0

class CustomerCreate(CustomerBase):
    primary_contact_id: Optional[int] = None

class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_type: Optional[CustomerType] = None
    territory: Optional[str] = None
    industry: Optional[str] = None
    credit_limit: Optional[float] = None
    primary_contact_id: Optional[int] = None

class CustomerResponse(CustomerBase):
    customer_id: int
    primary_contact_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True
