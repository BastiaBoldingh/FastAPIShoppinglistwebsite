from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, Integer, String
import uuid


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)