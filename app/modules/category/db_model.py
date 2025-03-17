from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, func, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

from app.db import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.current_timestamp(), nullable=False)
    modified_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        server_onupdate=func.current_timestamp(),  # Remarque les parenthèses ici
        nullable=True
    )
