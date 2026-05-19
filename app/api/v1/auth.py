from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import RefreshTokenRequest, UserCreate, UserLogin
from app.core.security import generate_password_hash, verify_password, create_access_token, verify_access_token, hash_token, create_refresh_token
from app.repositories.user_repository import UserRepository
from app.core.dependencies import get_current_user, get_db



router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = UserRepository.get_user_by_email(db, user.email)
    if not existing_user:
        existing_user = UserRepository.get_user_by_username(db, user.username)

    if existing_user: 
        raise HTTPException(status_code=400, detail="Email or username already registered")
    
    new_user = UserRepository.create_user(db, email=user.email, username=user.username, hashed_password=generate_password_hash(user.password))
    
    return {"message": "User registered successfully", "user_id": new_user.id}

    

@router.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = UserRepository.get_user_by_email(db, user.email)

    if not existing_user or not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(
        data=
        {"user_id": str(existing_user.id)}
        )
    refresh_token = create_refresh_token(
        data={"user_id": str(existing_user.id)},
        expires_delta=60 * 60 * 24 * 7
    )

    UserRepository.update_refresh_token(db, existing_user, hash_token(refresh_token))

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    

@router.post("/logout")
async def logout_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user: 
        raise HTTPException(status_code=404, detail="User not found")
    UserRepository.update_refresh_token(db, current_user, None)
    return {"message": "User logged out successfully"}

@router.post("/refresh")
async def refresh_token(body: RefreshTokenRequest, db: Session = Depends(get_db)):
    refresh_token = body.refresh_token
    payload = verify_access_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    
    user_id = payload.get("user_id")
    user = UserRepository.get_user_by_id(db, user_id)

    if not user: 
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.refresh_token != hash_token(refresh_token):
        raise HTTPException(status_code=401, detail="Refresh token does not match")
    
    new_access_token = create_access_token(data={"user_id": str(user.id)})

    return {"access_token": new_access_token, "token_type": "bearer"}

