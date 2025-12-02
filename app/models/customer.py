from sqlalchemy import Column, Integer, String, Enum, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base
import enum

class CustomerType(str, enum.Enum):
    INDIVIDUAL = "Individual"
    COMPANY = "Company"

class Customer(Base):
    __tablename__ = "customers"
    
    customer_id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    customer_type = Column(Enum(CustomerType), default=CustomerType.INDIVIDUAL)
    territory = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    credit_limit = Column(Float, default=0.0)
    primary_contact_id = Column(Integer, ForeignKey("contacts.contact_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
