import uuid
from datetime import datetime

from annotated_types import SupportsGe
from typing import Optional

from pydantic import BaseModel, Field


class BaseComment(BaseModel):
    user_id: uuid.UUID
    content: str = Field(description="The comment of the user")
    rating: Optional[SupportsGe] = Field(ge=1, le=5 )
    article_id: Optional[int] = None
    product_id: Optional[int] = None


class CreateComment(BaseComment):
    pass

class Comment(BaseComment):
    id: int
    created_at : datetime
