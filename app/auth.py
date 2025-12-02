from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.user import User, UserStatus
from app.models.jwt_session import JWTSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire, "type": "access", "sub": str(to_encode.get("sub"))})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh", "sub": str(to_encode.get("sub"))})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user_id_str = payload.get("sub")
    session_id = payload.get("session_id")
    
    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    # Check if session is valid and not revoked
    if session_id:
        jwt_session = db.query(JWTSession).filter(
            JWTSession.session_id == session_id,
            JWTSession.user_id == user_id
        ).first()
        
        if not jwt_session or jwt_session.revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session has been revoked. Please login again."
            )
        
        if jwt_session.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session has expired. Please login again."
            )
    
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None or user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    return user
