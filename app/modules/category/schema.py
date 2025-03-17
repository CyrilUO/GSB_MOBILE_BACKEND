from datetime import datetime
from typing import Union, Dict, Optional

from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str
    created_at: datetime
    modified_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CreateCategory(BaseModel):
    name: str


class UpdateCategory(CreateCategory):
    pass


class CategoryResponse(BaseModel):
    message: str
