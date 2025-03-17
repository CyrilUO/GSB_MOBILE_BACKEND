from app.modules.category.schema import CategoryResponse, Category
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules import CategoryModel, ProductModel

gsb_mobile_category_router = APIRouter(prefix="/category", tags=["Category"])


@gsb_mobile_category_router.post('/create-category', response_model=CategoryResponse)
def add_category(c: Category, db: Session = Depends(get_db)):
    category_in_db = db.query(CategoryModel).filter(CategoryModel.name == c.name).first()
    if category_in_db:
        raise HTTPException(status_code=400, detail='Category already exist')
    new_category = CategoryModel(name=c.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return CategoryResponse(
        message=f"Category {new_category.name} à l'id : {new_category.id}created successfully",
    )


@gsb_mobile_category_router.put('/update-category/{category_id}', response_model=CategoryResponse)
def update_category(category_id: int, c: Category, db: Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.name = c.name
    db.commit()
    db.refresh(category)

    return CategoryResponse(message=f"Category {category.name} updated successfully")


@gsb_mobile_category_router.delete("/delete-category/{category_id}", response_model=CategoryResponse)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    product_count = db.query(ProductModel).filter(ProductModel.category_id == category_id).count()
    if product_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete category {category.name}. {product_count} products are linked to it."
        )

    db.delete(category)
    db.commit()
    return CategoryResponse(message=f"{category.name} a été supprimé")


@gsb_mobile_category_router.get('/all', response_model=list[Category])
def get_category(db: Session = Depends(get_db)):
    categories = db.query(CategoryModel).all()

    if not categories:
        HTTPException(status_code=404, detail='Nothing found')

    return [Category.from_orm(c) for c in categories]


@gsb_mobile_category_router.get('/{category_id}', response_model=Category)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return Category.from_orm(category)


@gsb_mobile_category_router.get('/{category_id}/products', response_model=list[Category])
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    products = db.query(ProductModel).filter(ProductModel.category_id == category_id).all()

    if not products:
        raise HTTPException(status_code=404, detail="No products found in this category")

    return [Category.from_orm(p) for p in products]
