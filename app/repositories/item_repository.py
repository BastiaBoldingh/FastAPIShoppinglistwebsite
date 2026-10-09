from fastapi import Depends
from sqlalchemy import func 
from sqlalchemy.orm import Session
from uuid import UUID 

from app.models.shopping_item import ShoppingItem
from app.models.shopping_list import ShoppingList
from app.models.category import Category
from app.models.user import User
from app.services.categorizer import categorize, DEFAULT_CATEGORY


class ItemRepository:
    @staticmethod
    def get_items_by_list_id(db: Session, list_id, user: User):
        # ensure the list belongs to the user
        shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id, ShoppingList.owner_id == user.id).first()
        if not shopping_list:
            return []
        return db.query(ShoppingItem).filter(ShoppingItem.list_id == list_id).all()

    @staticmethod
    def add_item_to_list(db: Session, item_data, list_id: UUID, user: User):
        # the row lock serializes concurrent adds to the same list, so positions
        # and category creation can't race each other
        shopping_list = (
            db.query(ShoppingList)
            .filter(ShoppingList.id == list_id, ShoppingList.owner_id == user.id)
            .with_for_update()
            .first()
        )
        if not shopping_list:
            return None

        name = item_data.name.strip()
        if not name:
            return None

        if item_data.category_id:
            category = (
                db.query(Category)
                .filter(Category.id == item_data.category_id, Category.list_id == list_id)
                .first()
            )
            if not category:
                return None
        else:
            category = ItemRepository._get_or_create_category(db, list_id, categorize(name))

        max_pos = (
            db.query(func.max(ShoppingItem.position))
            .filter(ShoppingItem.list_id == list_id)
            .scalar()
        )

        new_item = ShoppingItem(
            list_id=list_id,
            name=name,
            quantity=item_data.quantity,
            unit=item_data.unit or None,
            category_id=category.id if category else None,
            position=0 if max_pos is None else max_pos + 1,
        )
        db.add(new_item)
        db.commit()  # one commit covers the new category and the item
        db.refresh(new_item)
        return new_item


    @staticmethod
    def _get_or_create_category(db: Session, list_id: UUID, suggested: str):
        if suggested == DEFAULT_CATEGORY:
            return None  # nothing matched, so leave the item uncategorized

        category = (
            db.query(Category)
            .filter(Category.list_id == list_id, func.lower(Category.name) == suggested.lower())
            .first()
        )
        if category:
            return category

        max_order = (
            db.query(func.max(Category.sort_order))
            .filter(Category.list_id == list_id)
            .scalar()
        )
        category = Category(
            list_id=list_id,
            name=suggested.capitalize(),  # "fruit" -> "Fruit"
            sort_order=0 if max_order is None else max_order + 1,
        )
        db.add(category)
        db.flush()  # assigns category.id without committing yet
        return category

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
    