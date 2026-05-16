from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
import datetime
import uuid

from core.database import Base


class User(Base): 
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[str] = mapped_column(String(50), default=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: Mapped[str] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(default=True)


