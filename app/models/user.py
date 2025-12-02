from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    ADMINISTRATOR = "Administrator"
    SALES_USER = "Sales User"
    SALES_MANAGER = "Sales Manager"

class UserStatus(str, enum.Enum):
    ACTIVE = "Active"
    DISABLED = "Disabled"

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.SALES_USER)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
