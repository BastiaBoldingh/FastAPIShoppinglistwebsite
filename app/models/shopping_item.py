from __future__ import annotations
import uuid 
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .shopping_list import ShoppingList
    from .category import Category

from app.core.database import Base



class ShoppingItem(Base):
    __tablename__ = "shopping_items"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    list_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("shopping_lists.id"))

    name: Mapped[str] = mapped_column(String(100))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit: Mapped[str] = mapped_column(String(50), nullable=True)

    category_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    is_completed: Mapped[bool] = mapped_column(default=False)
    position: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    shopping_list: Mapped["ShoppingList"] = relationship(back_populates="items")
    category: Mapped["Category"] = relationship(back_populates="items")
