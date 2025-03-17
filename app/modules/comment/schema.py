import uuid
from datetime import datetime

from annotated_types import SupportsGe
from typing import Optional

from pydantic import BaseModel, Field


class BaseComment(BaseModel):
    user_id: int
    content: str = Field(description="The comment of the user")
    rating: Optional[int] = Field(None, ge=1, le=5)
    article_id: int = None
    product_id: int = None

    class Config:
        from_attributes = True


class CreateComment(BaseComment):
    pass


class Comment(BaseComment):
    id: int
    created_at: datetime
    modified_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UpdatedComment(BaseModel):
    content: Optional[str] = Field(None, description="Updated comment text")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Updated rating from 1 to 5")


class CommentResponse(BaseModel):
    message: str
