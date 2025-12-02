from sqlalchemy import Column, Integer, String, Enum, Float, ForeignKey, Date, DateTime
from sqlalchemy.sql import func
from app.database import Base
import enum

class OpportunityStatus(str, enum.Enum):
    OPEN = "Open"
    QUOTED = "Quoted"
    WON = "Won"
    LOST = "Lost"

class Opportunity(Base):
    __tablename__ = "opportunities"
    
    opportunity_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=True)
    lead_id = Column(Integer, ForeignKey("leads.lead_id"), nullable=True)
    expected_value = Column(Float, default=0.0)
    probability = Column(Float, default=0.0)
    status = Column(Enum(OpportunityStatus), default=OpportunityStatus.OPEN)
    assigned_to = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    next_follow_up_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
