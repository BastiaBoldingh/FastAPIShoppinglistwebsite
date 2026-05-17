from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin
from app.core.security import generate_password_hash, verify_password, create_access_token, verify_access_token, hash_token, create_refresh_token



router = APIRouter(prefix="/auth", tags=["authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter((User.email == user.email) | (User.username == user.username)).first()

    if existing_user: 
        raise HTTPException(status_code=400, detail="Email or username already registered")
    
    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=generate_password_hash(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}

    

@router.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

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

    existing_user.refresh_token = hash_token(refresh_token)
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    

@router.post("/logout")
async def logout_user():
    return {"message": "User logged out successfully"}

@router.post("/refresh")
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    payload = verify_access_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    
    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()

    if not user: 
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.refresh_token != hash_token(refresh_token):
        raise HTTPException(status_code=401, detail="Refresh token does not match")
    
    new_access_token = create_access_token(data={"user_id": str(user.id)})

    return {"access_token": new_access_token, "token_type": "bearer"}

