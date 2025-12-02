from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User, UserRole
from app.auth import get_password_hash

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/init-admin", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_initial_admin(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Create the first admin user - only works if no users exist"""
    user_count = db.query(User).count()
    
    if user_count > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin user already exists. Use /auth/login to authenticate."
        )
    
    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        role=UserRole.ADMINISTRATOR
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
