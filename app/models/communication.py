from sqlalchemy import Column, Integer, String, Enum, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base
import enum

class CommunicationType(str, enum.Enum):
    EMAIL = "Email"
    NOTE = "Note"
    CALL = "Call"
    MEETING = "Meeting"

class Communication(Base):
    __tablename__ = "communications"
    
    communication_id = Column(Integer, primary_key=True, index=True)
    reference_doctype = Column(String, nullable=False)
    reference_id = Column(Integer, nullable=False)
    type = Column(Enum(CommunicationType), nullable=False)
    subject = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
