from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from app.models.opportunity import OpportunityStatus

class OpportunityBase(BaseModel):
    expected_value: float = 0.0
    probability: float = 0.0
    next_follow_up_date: Optional[date] = None

class OpportunityCreate(OpportunityBase):
    customer_id: Optional[int] = None
    lead_id: Optional[int] = None
    assigned_to: Optional[int] = None

class OpportunityUpdate(BaseModel):
    customer_id: Optional[int] = None
    lead_id: Optional[int] = None
    expected_value: Optional[float] = None
    probability: Optional[float] = None
    status: Optional[OpportunityStatus] = None
    assigned_to: Optional[int] = None
    next_follow_up_date: Optional[date] = None

class OpportunityResponse(OpportunityBase):
    opportunity_id: int
    customer_id: Optional[int]
    lead_id: Optional[int]
    status: OpportunityStatus
    assigned_to: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True
