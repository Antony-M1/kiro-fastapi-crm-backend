from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Campaign(Base):
    __tablename__ = "campaigns"
    
    campaign_id = Column(Integer, primary_key=True, index=True)
    campaign_name = Column(String, nullable=False)
    medium = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
