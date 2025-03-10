from sqlalchemy import Column, Integer, String, Enum, DateTime, func, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from enum import Enum as PyEnum

class Base(DeclarativeBase):
    pass

class RoleEnum(str, PyEnum):
    admin = 'admin'
    editor = 'editor'
    user = 'user'

class User(Base):
    __tablename__ = 'users'

    __table_args__ = (
        CheckConstraint("email LIKE '%@%'", name="email_must_have_@"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(55), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), server_default="user", nullable=False)
    profile_picture_url: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.current_timestamp(), nullable=False)

