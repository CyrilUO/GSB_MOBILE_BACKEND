from itertools import product
from platform import processor

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.modules.products.db_model import Product
from app.modules.products.schema import ProductBase, ProductCreate, ProductResponse

gsb_mobile_product_router = APIRouter(prefix="/products", tags=["Products"])


@gsb_mobile_product_router.get('/all', response_model=list[ProductBase])
def get_all_products(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user(["admin", "user"]))):

    _ = current_user
    products = db.query(Product).all()

    if products is None:
        raise ValueError("No products")
    return products



@gsb_mobile_product_router.post('/create', response_model=ProductResponse)
def create_product(
        p: ProductCreate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user(["admin", "user"]))
):
    _ = current_user

    existing_product = db.query(Product).filter(Product.name == p.name).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product already exists")

    new_product = Product(
        name=p.name,
        description=p.description,
        price=p.price,
        category_id=p.category_id,
        image_url=p.image_url,
        manufacturer=p.manufacturer
    )

    # Save to database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product



