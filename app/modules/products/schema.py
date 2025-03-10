from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., max_length=255, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(description="Product price")
    category_id: int = Field(..., description="Category ID")
    image_url: Optional[HttpUrl | str] = Field(None, description="Image URL")
    manufacturer: Optional[str] = Field(None, max_length=255, description="Manufacturer")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(gt=0)
    category_id: Optional[int] = None
    image_url: Optional[HttpUrl] = None
    manufacturer: Optional[str] = Field(None, max_length=255)

class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
