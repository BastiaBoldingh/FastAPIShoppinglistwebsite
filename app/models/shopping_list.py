import uuid 
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base



class ShoppingList(Base):
    __tablename__ = "shopping_lists"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    storename: Mapped[str] = mapped_column(String(100))

    is_shared: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[str] = mapped_column(String(50))
    updated_at: Mapped[str] = mapped_column(String(50))

