from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Contact(Base):
    __tablename__ = "contacts"
    
    contact_id = Column(Integer, primary_key=True, index=True)
    contact_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    linked_customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
