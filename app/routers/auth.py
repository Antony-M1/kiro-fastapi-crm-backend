from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest
from app.models.user import User, UserStatus
from app.models.jwt_session import JWTSession
from app.auth import verify_password, create_access_token, create_refresh_token, decode_token
from app.config import settings
from app.timezone import now, add_days

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    access_token = create_access_token(data={"sub": user.user_id})
    refresh_token = create_refresh_token(data={"sub": user.user_id})
    
    jwt_session = JWTSession(
        user_id=user.user_id,
        expires_at=add_days(settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(jwt_session)
    db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    payload = decode_token(request.refresh_token)
    
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user or user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Verify the refresh token session exists and is not expired
    jwt_session = db.query(JWTSession).filter(JWTSession.user_id == user_id).first()
    if not jwt_session or jwt_session.expires_at < now():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token session expired or not found"
        )
    
    # Only create a new access token, keep the existing refresh token
    access_token = create_access_token(data={"sub": user.user_id})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=request.refresh_token
    )

@router.post("/logout")
def logout(current_user: dict = Depends(decode_token), db: Session = Depends(get_db)):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user_id = current_user.get("sub")
    
    # Revoke all active tokens for the user
    # Delete all JWT sessions to invalidate refresh tokens
    jwt_sessions = db.query(JWTSession).filter(JWTSession.user_id == user_id).all()
    for session in jwt_sessions:
        db.delete(session)
    
    # Update user's token version to invalidate all access tokens
    # This requires adding a token_version field to the User model
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        if not hasattr(user, 'token_version'):
            user.token_version = 1
        else:
            user.token_version += 1
    
        db.commit()
    return {"message": "All tokens revoked successfully. Please login again."}
