from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
import uuid

from app.core.database import Base


class User(Base): 
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    hashed_password: Mapped[str] = mapped_column(String(128))
    refresh_token: Mapped[str] = mapped_column(String(256), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(default=True)



