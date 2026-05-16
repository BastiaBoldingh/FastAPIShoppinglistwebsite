import uuid 
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base



class ShoppingListMember(Base):
    __tablename__ = "shopping_list_members"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    list_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("shopping_lists.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    permission: Mapped[str] = mapped_column(String(50), default="read")
    created_at: Mapped[str] = mapped_column(String(50))