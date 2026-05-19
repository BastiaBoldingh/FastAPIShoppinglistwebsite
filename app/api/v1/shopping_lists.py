from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.models.shopping_list import ShoppingList
from app.models.user import User
from app.core.dependencies import get_current_user, get_db
from app.repositories.list_repository import ListRepository

from app.schemas.shopping_list import ShoppingListCreate



router = APIRouter(prefix="/lists", tags=["shopping_lists"])


@router.get("/")
async def get_shopping_lists(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ListRepository.get_shopping_lists_by_user_id(db, user)


@router.post("/")
async def create_shopping_list(list_data: ShoppingListCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ListRepository.create_shopping_list(db, list_data, user)

@router.get("/{list_id}")
async def get_shopping_list(list_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ListRepository.get_shopping_list_by_id(db, list_id, user)

@router.patch("/{list_id}")
async def update_shopping_list(list_id: int):
    pass
        #update the shopping list with the given id for the user

@router.delete("/{list_id}")
async def delete_shopping_list(list_id: int):
    pass
        #delete the shopping list with the given id for the user