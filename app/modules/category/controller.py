from sys import prefix

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules import Product, Category

gsb_mobile_category_router = APIRouter(prefix="/category", tags=["CATEGORY"])

@gsb_mobile_category_router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Check if products exist in this category
    products = db.query(Product).filter(Product.category_id == category_id).all()

    if products:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete category {category.name}. There are {len(products)} products linked to it."
        )

    db.delete(category)
    db.commit()
    return {"message": f"Category {category.name} deleted successfully"}
