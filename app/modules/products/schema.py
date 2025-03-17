from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Union
from datetime import datetime


class ProductBase(BaseModel):
    name: str = Field(..., max_length=255, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(description="Product price")
    category_id: int = Field(..., description="Category ID")
    images: Optional[Union[HttpUrl, bytes]] = Field(None, description="Image URL or Binary Image Data")


class ProductCreate(ProductBase):
    pass


class GetProduct(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(gt=0)
    category_id: Optional[int] = None
    images: Optional[Union[HttpUrl, bytes]] = Field(None, description="Image URL or Binary Image Data")


class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProductResponseMsg(BaseModel):
    message: str


class ProductImgResponse(BaseModel):
    filename: str
