from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.repositories.item_repository import ItemRepository
from app.schemas.shopping_item import ShoppingItemAdd


router = APIRouter(tags=["shopping_items"])


@router.post("/lists/{list_id}/items")
async def add_shopping_item(list_id: UUID, item: ShoppingItemAdd, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    created = ItemRepository.add_item_to_list(db=db, item_data=item, list_id=list_id, user=user)
    if not created:
        raise HTTPException(status_code=404, detail="List not found or invalid category")
    return created


@router.patch("/items/{item_id}")
async def update_shopping_item(item_id: UUID, updated_item: ShoppingItemAdd, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    updated = ItemRepository.update_item(db=db, item_id=item_id, updated_item_data=updated_item, user=user)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found or/or access denied")
    return updated


@router.delete("/items/{item_id}")
async def delete_shopping_item(item_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    res = ItemRepository.delete_item(db=db, item_id=item_id, user=user)
    if not res:
        raise HTTPException(status_code=404, detail="Item not found or/or access denied")
    return res

@router.post("/items/reorder")
async def reorder_shopping_items():
    raise HTTPException(status_code=501, detail="Not implemented")

@router.post("/items/sort")
async def sort_shopping_items():
    raise HTTPException(status_code=501, detail="Not implemented")

@router.patch("/lists/{list_id}/items/reorder")
async def reorder_shopping_items_in_list(list_id: UUID):
    raise HTTPException(status_code=501, detail="Not implemented")