from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.modules import RoleEnum, ProductModel
from app.modules.ratings.db_model import RatingModel
from app.modules.ratings.schema import RatingResponse, RatingCreate, RatingResponseWithProduct

e = RoleEnum

gsb_mobile_rating_router = APIRouter(prefix="/ratings", tags=["Ratings"])


@gsb_mobile_rating_router.post("/rate-product", response_model=RatingResponse)
def create_rating(
        rating: RatingCreate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value, e.user.value]))
):
    _ = current_user
    existing_rating = db.query(RatingModel).filter(
        RatingModel.product_id == rating.product_id,
        RatingModel.user_id == rating.user_id
    ).first()

    if existing_rating:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Rating already exists for this product by this user.")

    new_rating = RatingModel(**rating.dict())
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating


@gsb_mobile_rating_router.get("/get-all", response_model=List[RatingResponse])
def get_all_ratings(
        db: Session = Depends(get_db),
        _=Depends(get_current_user([e.admin.value, e.editor.value, e.user.value]))
):
    ratings = db.query(RatingModel).all()
    return ratings


@gsb_mobile_rating_router.get("/by_user/{user_id}", response_model=List[RatingResponse])
def get_ratings_by_user(
        user_id: int,
        db: Session = Depends(get_db),
        _=Depends(get_current_user([e.admin.value, e.editor.value, e.user.value]))
):
    ratings = db.query(RatingModel).filter(RatingModel.user_id == user_id).all()
    return ratings


@gsb_mobile_rating_router.get("/by_product/{product_id}", response_model=List[RatingResponseWithProduct])
def get_ratings_by_product(product_id: int, db: Session = Depends(get_db)):
    ratings = (
        db.query(RatingModel, ProductModel.name.label('product_name'))
        .join(ProductModel, RatingModel.product_id == ProductModel.id)
        .filter(RatingModel.product_id == product_id)
        .all()
    )
    return [RatingResponseWithProduct.model_validate({
        "id": rating.RatingModel.id,
        "product_id": rating.RatingModel.product_id,
        "user_id": rating.RatingModel.user_id,
        "rating": rating.RatingModel.rating,
        "created_at": rating.RatingModel.created_at,
        "modified_at": rating.RatingModel.modified_at,
        "product_name": rating.product_name
    }, from_attributes=True) for rating in ratings]
