from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.core.dependencies import get_db
from app.modules import UserModel
from app.modules.users.schema import UserCreate, GetUser, UpdateUser, UserReponse, DeleteUser, RoleEnum
from app.utils.hash import hash_password

gsb_mobile_user_router = APIRouter(prefix="/users", tags=["Users"])

e = RoleEnum


# Create user
@gsb_mobile_user_router.post("/create-user", response_model=UserReponse)
def create_user(
        user: UserCreate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value]))
):
    _current_user = current_user
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if len(user.password) < 3:
        raise HTTPException(status_code=400, detail="Your password must be at least 3 characters long")

    hashed_password = hash_password(user.password)
    new_user = UserModel(username=user.username, email=user.email, password=hashed_password, role=user.role)
    print(type(new_user))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print(f"Orm : {GetUser.from_orm(new_user)}")

    return UserReponse(messages=GetUser.from_orm(new_user))


@gsb_mobile_user_router.get("/all", response_model=list[GetUser])
def get_all_users(
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.user.value, e.editor.value, e.admin]))
):
    _ = current_user

    users = db.query(UserModel).all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    return [GetUser.from_orm(user) for user in users]


@gsb_mobile_user_router.get("/{user_id}", response_model=GetUser)
def get_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.user.value, e.editor.value, e.admin.value]))
):

    _current_user = current_user
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_password = user.password
    user -= user_password

    return user


@gsb_mobile_user_router.delete("/delete-user/{user_id}", response_model=DeleteUser)
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value]))
):
    _current_user = current_user
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="usernot found")
    db.delete(user)
    db.commit()

    return DeleteUser(message=f"Utilisateur supprimé : {user.username}", id=user.id, username=user.username)


@gsb_mobile_user_router.put("/update-user/{user_id}", response_model=GetUser)
def update_user(
        user_id: int,
        user_update: UpdateUser,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value]))
):
    _current_user = current_user
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.model_dump(exclude_unset=True, mode='python')

    if not isinstance(update_data, dict):
        update_data = dict(update_data)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return GetUser(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        password=hash_password(user.password) if isinstance(user.password, str) else user.password,
        profile_picture_url=user.profile_picture_url,
        created_at=user.created_at
    )
