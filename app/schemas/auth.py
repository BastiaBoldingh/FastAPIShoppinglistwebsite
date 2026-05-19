from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel): 
    email: EmailStr
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str
    
    