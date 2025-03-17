from typing import Optional

from pydantic import field_validator
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from enum import Enum as PyEnum


class RoleEnum(str, PyEnum):
    admin = 'admin'
    editor = 'editor'
    user = 'user'

    @classmethod
    def is_valid_role(cls, role: str) -> bool:
        for member in cls:
            if role == member:
                return True
            else:
                return False
        raise ValueError(f"Le rôle '{role}' n'est pas autorisé. Rôles autorisés : {cls.__members__.values()}")


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: RoleEnum = Field(default=RoleEnum.user)

    @field_validator("role", mode="before")
    def validate_role(cls, value):
        if value not in RoleEnum.__members__.values():
            raise ValueError(f"Invalid role: {value}. Choose from {list(RoleEnum.__members__.values())}")
        return value


class UserCreate(UserBase):
    password: str = Field(min_length=5)


class GetUser(UserBase):
    id: Optional[int] = None
    password: str
    profile_picture_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class DeleteUser(BaseModel):
    message: str
    id: int
    username: str


class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[RoleEnum] = None
    profile_picture_url: Optional[str] = None


class UserReponse(BaseModel):
    messages: GetUser
