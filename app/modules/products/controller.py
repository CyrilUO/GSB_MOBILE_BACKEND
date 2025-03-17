import io

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.modules.products.db_model import ProductModel
from app.modules.products.schema import ProductCreate, ProductResponse, ProductUpdate, ProductImgResponse, \
    ProductResponseMsg
from app.modules.users.db_model import RoleEnum

e = RoleEnum
gsb_mobile_product_router = APIRouter(prefix="/products", tags=["Products"])


@gsb_mobile_product_router.get('/all', response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db),
                     current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value, e.user.value]))):
    _ = current_user
    products = db.query(ProductModel).all()

    if products is None:
        raise ValueError("No products")
    return products


@gsb_mobile_product_router.get('/{product_id}', response_model=ProductResponse)
def get_product_by_id(
        product_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value, e.user.value]))
):
    _ = current_user

    product_in_db = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if not product_in_db:
        raise HTTPException(status_code=404, detail="Product not found")

    return product_in_db


@gsb_mobile_product_router.post('/create-product', response_model=ProductResponse)
def create_product(
        p: ProductCreate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value]))
):
    _ = current_user

    existing_product = db.query(ProductModel).filter(ProductModel.name == p.name).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product already exists")

    new_product = ProductModel(
        name=p.name,
        description=p.description,
        price=p.price,
        category_id=p.category_id,
        image=p.image,
    )

    # Save to database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@gsb_mobile_product_router.put('/update-product/{product_id}', response_model=ProductResponse)
def update_product(
        product_id: int,
        p: ProductUpdate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([RoleEnum.admin.value, RoleEnum.editor.value]))
):
    _ = current_user

    product_in_db = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if not product_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

    # Mise à jour des champs fournis
    update_data = p.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product_in_db, key, value)

    db.commit()
    db.refresh(product_in_db)

    return product_in_db


@gsb_mobile_product_router.delete('/delete-product/{product_id}', response_model=ProductResponseMsg)
def delete_product(
        product_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin]))
):
    _ = current_user

    product_in_db = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if not product_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

    db.delete(product_in_db)
    db.commit()

    return ProductResponseMsg(
        message=f"Product {product_in_db.name} (ID {product_in_db.id}) has been deleted successfully")


# Dealing with uploading the image

@gsb_mobile_product_router.post('/upload-img', response_model=ProductImgResponse)
async def upload_img(
        product_id: int,
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    existing_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

    file_content = await file.read()

    existing_product.images = file_content
    db.commit()
    db.refresh(existing_product)

    return ProductImgResponse(filename=file.filename)


@gsb_mobile_product_router.get("/get-image/{product_id}")
def get_image(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product or not product.images:
        raise HTTPException(status_code=404, detail="Image not found")

    return StreamingResponse(io.BytesIO(product.images), media_type="image/jpeg",
                             headers={"Content-Disposition": "inline; filename=image.jpg"})

