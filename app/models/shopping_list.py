from __future__ import annotations
import uuid 
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .category import Category
    from .shopping_item import ShoppingItem

from app.core.database import Base




class ShoppingList(Base):
    __tablename__ = "shopping_lists"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    storename: Mapped[str] = mapped_column(String(100), nullable=True)

    is_shared: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    categories: Mapped[list["Category"]] = relationship(
        "Category", back_populates="shopping_list", order_by="Category.sort_order"
    )
    items: Mapped[list["ShoppingItem"]] = relationship(
        "ShoppingItem", back_populates="shopping_list"
    )