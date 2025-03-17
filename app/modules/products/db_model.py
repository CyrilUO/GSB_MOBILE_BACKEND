from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey, func, DateTime, LargeBinary
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

from app.db import Base


class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)
    images: Mapped[LargeBinary] = mapped_column(LargeBinary, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.current_timestamp())
    modified_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        server_onupdate=func.current_timestamp(),
        nullable=True
    )
