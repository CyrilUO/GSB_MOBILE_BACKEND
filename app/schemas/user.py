from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.models.user import RoleEnum


class UserBase(BaseModel):
    username: str
    role: RoleEnum
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    password: str
    profile_picture_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
