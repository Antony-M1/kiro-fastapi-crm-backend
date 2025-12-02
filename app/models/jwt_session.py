from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class JWTSession(Base):
    __tablename__ = "jwt_sessions"
    
    session_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    issued_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    device_info = Column(String, nullable=True)
    revoked = Column(Boolean, default=False)
