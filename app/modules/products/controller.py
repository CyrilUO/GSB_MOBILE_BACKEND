from itertools import product
from platform import processor

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.exceptions import ErrorEnum
from app.core.security import get_current_user
from app.modules.products.db_model import Product
from app.modules.products.schema import ProductBase, ProductCreate, ProductResponse
from app.modules.users.db_model import RoleEnum


e = RoleEnum
gsb_mobile_product_router = APIRouter(prefix="/products", tags=["Products"])


@gsb_mobile_product_router.get('/all', response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value, e.user.value]))):

    _ = current_user
    products = db.query(Product).all()

    if products is None:
        raise ValueError("No products")
    return products


@gsb_mobile_product_router.get('/{p_id}', response_model=ProductResponse)
def get_product_by_id(
        p_id : int,
        db : Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value, e.user.value]))
):
    _ = current_user

    product_in_db = db.query(Product).filter(Product.id == p_id).first()

    if not product_in_db:
        raise HTTPException(status_code=400, detail="Product already exists")

    return product_in_db

@gsb_mobile_product_router.post('/create', response_model=ProductResponse)
def create_product(
        p: ProductCreate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value]))
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


@gsb_mobile_product_router.delete('/delete/{product_id}', response_model=ProductResponse)
def delete_product(
        product_id : int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user(["admin", "user"]))
):
    __ = current_user

    product_in_db = db.query(Product).filter(Product.id == product_id).first()

    if not product_in_db:
        raise ValueError('produit non existant')

    db.delete(product_in_db)
    db.commit()

    return {"messages" : f"Product {product_in_db.name} à l'id {product_in_db.id} a été supprimé avec succès"}



