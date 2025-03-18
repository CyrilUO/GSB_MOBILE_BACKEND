from app.core.security import get_current_user
from app.modules.category.schema import CategoryResponse, Category, CreateCategory, UpdateCategory
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules import CategoryModel, ProductModel, RoleEnum

gsb_mobile_category_router = APIRouter(prefix="/category", tags=["Category"])

e = RoleEnum


# Api works
@gsb_mobile_category_router.get('/all', response_model=list[Category])
def get_category(
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.user.value, e.editor.value]))
):
    _ = current_user
    categories = db.query(CategoryModel).all()

    if not categories:
        HTTPException(status_code=404, detail='Nothing found')

    return [Category.model_validate(c, from_attributes=True) for c in categories]


# Api works
@gsb_mobile_category_router.get('/{category_id}', response_model=Category)
def get_category_by_id(
        category_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value]))
):
    _ = current_user
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return Category.model_validate(category, from_attributes=True)


# Api works
@gsb_mobile_category_router.get('/{category_id}/products', response_model=list[Category])
def get_products_by_category(
        category_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value, e.admin.value]))
):
    _ = current_user
    products = db.query(ProductModel).filter(ProductModel.category_id == category_id).all()

    if not products:
        raise HTTPException(status_code=404, detail="No products found in this category")

    return [Category.model_validate(p, from_attributes=True) for p in products]


# Api works
@gsb_mobile_category_router.post('/create-category', response_model=CategoryResponse)
def add_category(
        c: CreateCategory,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value]))
):
    _ = current_user
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


# Api works
@gsb_mobile_category_router.put('/update-category/{category_id}', response_model=CategoryResponse)
def update_category(
        category_id: int,
        c: UpdateCategory,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value]))
):
    _ = current_user
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.name = c.name
    db.commit()
    db.refresh(category)

    return CategoryResponse(message=f"Category {category.name} updated successfully")


# Api works
@gsb_mobile_category_router.delete("/delete-category/{category_id}", response_model=CategoryResponse)
def delete_category(
        category_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value]))
):
    _ = current_user
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
