from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import UserRole, UserStatus

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.SALES_USER

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    user_id: int
    status: UserStatus
    created_at: datetime
    
    class Config:
        from_attributes = True
