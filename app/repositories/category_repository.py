from sqlalchemy.orm import Session
from uuid import UUID

from app.models.category import Category
from app.models.shopping_list import ShoppingList
from app.models.user import User


class CategoryRepository:
    @staticmethod
    def add_category_to_list(db: Session, list_id: UUID, name: str, user: User):
        shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id, ShoppingList.owner_id == user.id).first()
        if not shopping_list:
            return None

        # determine sort_order (append to end)
        max_order = db.query(Category).filter(Category.list_id == list_id).order_by(Category.sort_order.desc()).first()
        next_order = (max_order.sort_order + 1) if max_order else 0

        new_cat = Category(list_id=list_id, name=name, sort_order=next_order)
        db.add(new_cat)
        db.commit()
        db.refresh(new_cat)
        return new_cat

    @staticmethod
    def get_category_by_id(db: Session, category_id: UUID, user: User):
        # ensure the category belongs to a list owned by the user
        return (
            db.query(Category)
            .join(ShoppingList, ShoppingList.id == Category.list_id)
            .filter(Category.id == category_id, ShoppingList.owner_id == user.id)
            .first()
        )
