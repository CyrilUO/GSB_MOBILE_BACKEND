from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class RatingBase(BaseModel):
    product_id: int = Field(..., description="ID of the product being rated")
    user_id: int = Field(..., description="ID of the user giving the rating")
    rating: int = Field(..., ge=1, le=5, description="Rating value between 1 and 5")


class RatingCreate(RatingBase):
    pass


class RatingResponse(RatingBase):
    id: int
    created_at: datetime
    modified_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RatingResponseWithProduct(RatingResponse):
    product_name: str

    class Config:
        from_attributes = True
