from sqlalchemy.orm import Session, joinedload
from fastapi import Depends
from uuid import UUID

from app.models.shopping_list import ShoppingList
from app.models.user import User
from app.core.dependencies import get_current_user

from app.schemas.shopping_list import ShoppingListCreate


class ListRepository: 
    @staticmethod
    def get_shopping_lists_by_user_id(db: Session, user: User = Depends(get_current_user)):
        return (
            db.query(ShoppingList)
            .options(joinedload(ShoppingList.categories), joinedload(ShoppingList.items))
            .filter(ShoppingList.owner_id == user.id)
            .all()
        )
    
    @staticmethod
    def create_shopping_list(db: Session, list_data: ShoppingListCreate, user: User):
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
    def get_shopping_list_by_id(db: Session, list_id: UUID, user: User):
        return (
            db.query(ShoppingList)
            .options(joinedload(ShoppingList.categories), joinedload(ShoppingList.items))
            .filter(ShoppingList.id == list_id, ShoppingList.owner_id == user.id)
            .first()
        )
    
    @staticmethod
    def delete_shopping_list(db: Session, list_id: UUID, user: User): 
        shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id, ShoppingList.owner_id == user.id).first()
        if shopping_list:
            db.delete(shopping_list)
            db.commit()
            return {"message": "Shopping list deleted successfully"}
        else:
            return {"message": "Shopping list not found"}
        
    @staticmethod
    def update_shopping_list(db: Session, list_id: UUID, list_data, user: User):
        shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id, ShoppingList.owner_id == user.id).first()
        if not shopping_list:
            return {"message": "Shopping list not found"}
        if list_data.name is not None:
            shopping_list.title = list_data.name
        if list_data.description is not None:
            shopping_list.description = list_data.description
        if list_data.storename is not None:
            shopping_list.storename = list_data.storename
        db.commit()
        db.refresh(shopping_list)
        return shopping_list

