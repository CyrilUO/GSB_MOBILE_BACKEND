from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.modules import ArticleModel, ProductModel, UserModel, RoleEnum
from app.modules.article.schemas import GetArticle, CreateArticle, ResponseArticle, UpdateArticle

gsb_mobile_article_router = APIRouter(prefix="/article", tags=["Articles"])

e = RoleEnum


# API works
@gsb_mobile_article_router.get('/all', response_model=List[GetArticle])
def get_articles(
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value, e.user.value]))
):
    _current_user = current_user
    articles = db.query(ArticleModel).all()

    if not articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No articles found")

    return [GetArticle.model_validate(article) for article in articles]


# API works
@gsb_mobile_article_router.get('/{article_id}', response_model=GetArticle)
def get_article_by_id(
        article_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value, e.user.value]))
):
    _current_user = current_user
    article = db.query(ArticleModel).filter(ArticleModel.id == article_id).first()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    return GetArticle.model_validate(article)


# Api works
@gsb_mobile_article_router.get('/product/{product_id}', response_model=List[GetArticle])
def get_articles_by_product(
        product_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value]))
):
    _current_user = current_user
    articles = db.query(ArticleModel).filter(ArticleModel.product_id == product_id).all()

    if not articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No articles found for this product")

    return [GetArticle.model_validate(article) for article in articles]


# Api works
@gsb_mobile_article_router.get('/user/{user_id}', response_model=List[GetArticle])
def get_articles_by_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value]))
):
    _current_user = current_user
    articles = db.query(ArticleModel).filter(ArticleModel.user_id == user_id).all()

    if not articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No articles found for this user")

    return [GetArticle.model_validate(article) for article in articles]


# Api works!
@gsb_mobile_article_router.post('/create-article', response_model=ResponseArticle)
def create_article(
        c: CreateArticle,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value]))
):
    _current_user = current_user
    # Vérifier si l'utilisateur existe
    user = db.query(UserModel).filter(UserModel.id == c.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    # Vérifier si un article existe déjà pour ce produit
    existing_article = db.query(ArticleModel).filter(ArticleModel.product_id == c.product_id).first()
    if existing_article:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Article for this product already exists')

    # Cas de prise du token (petit bonus)
    man_in_the_middle = int(_current_user.get("sub"))
    if man_in_the_middle != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Nice try')

    new_article = ArticleModel(
        title=c.title,
        content=c.content,
        product_id=c.product_id,
        user_id=c.user_id
    )

    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return ResponseArticle(message=f"Article {new_article.id}: '{new_article.title}' ajouté avec succès")


# Api works!
@gsb_mobile_article_router.delete('/delete-article/{article_id}', response_model=ResponseArticle)
def delete_article(
        article_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value]))
):
    _current_user = current_user

    print(f"🛠 current_user reçu: {_current_user}")

    article = db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Article not found')

    db.delete(article)
    db.commit()

    return ResponseArticle(message=f"Article '{article.title}' supprimé avec succès")


# Api works !
@gsb_mobile_article_router.put('/update-article/{article_id}', response_model=ResponseArticle)
def update_article(
        article_id: int,
        article_data: UpdateArticle,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value]))
):
    _current_user = current_user
    article = db.query(ArticleModel).filter(ArticleModel.id == article_id).first()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    update_data = article_data.model_dump(exclude_unset=True)  #

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No valid fields provided for update")

    for key, value in update_data.items():
        setattr(article, key, value)

    db.commit()
    db.refresh(article)

    return ResponseArticle(message=f"Article '{article.title}' (ID: {article.id}) updated successfully")
