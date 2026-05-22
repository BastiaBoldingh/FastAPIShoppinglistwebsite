from fastapi import Depends
from sqlalchemy.orm import Session

from app.models.shopping_item import ShoppingItem
from app.models.shopping_list import ShoppingList
from app.models.category import Category
from app.models.user import User


class ItemRepository:
    @staticmethod
    def get_items_by_list_id(db: Session, list_id, user: User):
        # ensure the list belongs to the user
        shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id, ShoppingList.owner_id == user.id).first()
        if not shopping_list:
            return []
        return db.query(ShoppingItem).filter(ShoppingItem.list_id == list_id).all()

    @staticmethod
    def add_item_to_list(db: Session, item_data, list_id, user: User):
        # validate list ownership
        shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id, ShoppingList.owner_id == user.id).first()
        if not shopping_list:
            return None

        # validate category if provided
        if item_data.category_id:
            category = db.query(Category).filter(Category.id == item_data.category_id, Category.list_id == list_id).first()
            if not category:
                return None

        new_item = ShoppingItem(
            list_id=list_id,
            name=item_data.name,
            quantity=item_data.quantity,
            unit=item_data.unit if item_data.unit else None,
            category_id=item_data.category_id
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

    @staticmethod
    def update_item(db: Session, item_id, updated_item_data, user: User):
        item = db.query(ShoppingItem).filter(ShoppingItem.id == item_id).first()
        if not item:
            return None

        # ensure the user owns the parent list
        shopping_list = db.query(ShoppingList).filter(ShoppingList.id == item.list_id, ShoppingList.owner_id == user.id).first()
        if not shopping_list:
            return None

        item.name = updated_item_data.name
        item.quantity = updated_item_data.quantity
        item.unit = updated_item_data.unit if updated_item_data.unit else None
        item.category_id = updated_item_data.category_id
        # optional: update completion status if provided
        if hasattr(updated_item_data, "is_completed"):
            item.is_completed = updated_item_data.is_completed

        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_item(db: Session, item_id, user: User):
        item = db.query(ShoppingItem).filter(ShoppingItem.id == item_id).first()
        if not item:
            return None

        shopping_list = db.query(ShoppingList).filter(ShoppingList.id == item.list_id, ShoppingList.owner_id == user.id).first()
        if not shopping_list:
            return None

        db.delete(item)
        db.commit()
        return {"message": "Item deleted"}
    