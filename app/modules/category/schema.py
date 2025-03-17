from datetime import datetime
from typing import Union, Dict

from pydantic import BaseModel


class Category(BaseModel):
    name: str
    created_at: datetime
    modified_at: datetime


class CategoryResponse(BaseModel):
    message: str

