from sqlalchemy.orm import Session 
from fastapi import Depends

from app.models.shopping_list import ShoppingList
from app.models.user import User
from app.core.dependencies import get_current_user

from app.schemas.shopping_list import ShoppingListCreate


class ListRepository: 
    @staticmethod
    def get_shopping_lists_by_user_id(db: Session, user: User = Depends(get_current_user)):
        return db.query(ShoppingList).filter(ShoppingList.owner_id == user.id).all()
    
    @staticmethod
    def create_shopping_list(db: Session, list_data: ShoppingListCreate, user: User = Depends(get_current_user)):
        new_list = ShoppingList(
            owner_id=user.id,
            title=list_data.name,
            description=list_data.description,
            storename=list_data.storename
        )
        db.add(new_list)
        db.commit()
        db.refresh(new_list)
        return new_list

    @staticmethod
    def get_shopping_list_by_id(db: Session, list_id: int, user: User = Depends(get_current_user)):
        return db.query(ShoppingList).filter(ShoppingList.id == list_id, ShoppingList.owner_id == user.id).first()
    
    @staticmethod
    def delete_shopping_list(db: Session, list_id: int, user: User): 
        shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id, ShoppingList.owner_id == user.id).first()
        if shopping_list:
            db.delete(shopping_list)
            db.commit()
            return {"message": "Shopping list deleted successfully"}
        else:
            return {"message": "Shopping list not found"}

