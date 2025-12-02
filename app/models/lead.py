from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base
import enum

class LeadSource(str, enum.Enum):
    WEBSITE = "Website"
    REFERRAL = "Referral"
    CAMPAIGN = "Campaign"
    EMAIL = "Email"
    OTHER = "Other"

class LeadStatus(str, enum.Enum):
    NEW = "New"
    CONTACTED = "Contacted"
    QUALIFIED = "Qualified"
    LOST = "Lost"
    CONVERTED = "Converted"

class Lead(Base):
    __tablename__ = "leads"
    
    lead_id = Column(Integer, primary_key=True, index=True)
    lead_name = Column(String, nullable=False)
    company_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    source = Column(Enum(LeadSource), default=LeadSource.OTHER)
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW)
    assigned_to = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
