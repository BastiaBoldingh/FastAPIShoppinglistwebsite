from __future__ import annotations
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .shopping_list import ShoppingList
    from .shopping_item import ShoppingItem




class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    list_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("shopping_lists.id"))
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    shopping_list: Mapped["ShoppingList"] = relationship(back_populates="categories")
    items: Mapped[list["ShoppingItem"]] = relationship(
        "ShoppingItem", back_populates="category", order_by="ShoppingItem.position"
    )