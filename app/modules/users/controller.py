from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.core.dependencies import get_db
from app.modules.users.db_model import User
from app.modules.users.schema import UserCreate, GetUser, UpdateUser
from app.utils.hash import hash_password

gsb_mobile_user_router = APIRouter(prefix="/users", tags=["Users"])

#Create user
@gsb_mobile_user_router.post("/create", response_model=GetUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@gsb_mobile_user_router.get("/all", response_model=list[GetUser])
def get_all_users(
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user("admin"))
):

    _ = current_user

    users = db.query(User).all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users



#  `/users/{user_id}` separately
@gsb_mobile_user_router.get("/{user_id}", response_model=GetUser)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user



@gsb_mobile_user_router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="usernot found")
    db.delete(user)
    db.commit()

    return {"message": f"user : {user.username} with id : {user.id} deleted properly"}

@gsb_mobile_user_router.put("/{user_id}", response_model=GetUser)
def update_user(user_id: int, user_update: UpdateUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
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



