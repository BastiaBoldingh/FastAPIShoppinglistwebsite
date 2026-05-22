from fastapi import Depends, APIRouter, HTTPException
from uuid import UUID
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.repositories.category_repository import CategoryRepository

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/lists/{list_id}/categories")
async def add_category_to_list(list_id: UUID, category_name: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    created = CategoryRepository.add_category_to_list(db=db, list_id=list_id, name=category_name, user=user)
    if not created:
        raise HTTPException(status_code=404, detail="List not found or access denied")
    return created


@router.get("/{category_id}")
async def get_category(category_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cat = CategoryRepository.get_category_by_id(db=db, category_id=category_id, user=user)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found or access denied")
    return cat


