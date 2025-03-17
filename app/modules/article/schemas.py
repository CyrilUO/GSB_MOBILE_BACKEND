from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class Article(BaseModel):
    title: str
    content: str
    product_id: int
    user_id: int

    class Config:
        from_attributes = True

# from_attributes = True permet d'utiliser directement des objets SQLAlchemy avec Pydantic.
# C'est indispensable si tes endpoints retournent des objets issus de la base de données.
# C'est la version moderne de orm_mode = True (Pydantic v1).


class CreateArticle(Article):
    pass


class UpdateArticle(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

    class Config:
        from_attributes = True


class GetArticle(Article):
    id: int
    created_at: datetime
    modified_at: Optional[datetime] = None


class ResponseArticle(BaseModel):
    message: str
