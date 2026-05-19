from fastapi import Depends, APIRouter

from app.models.user import User
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
async def get_current_user(user: User = Depends(get_current_user)):
    return user
        #return the current user
    


@router.patch("/me")
async def update_current_user(user: User = Depends(get_current_user)):
    pass
        #update the current user    
