from typing_extensions import Annotated

from app.modules.auth.schema import FormData, TokenProvider, LogoutMessage
from fastapi import APIRouter, Depends, HTTPException, Form, status, Header
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.modules.users.db_model import UserModel
from app.core.jwt import create_access_token
from app.core.hash import verify_password
from app.utils.token_blacklist import add_token_to_blacklist

gsb_mobile_auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@gsb_mobile_auth_router.post("/login", response_model=TokenProvider)
# Use x-www-form-urlencoded (key : value) if we stick to the Annotated Form() built in from FApi
def login(data: Annotated[FormData, Form(strict=True)], db: Session = Depends(get_db)):
    email = data.email
    password = data.password

    user = db.query(UserModel).filter(UserModel.email == email).first()

    if not user or not verify_password(password, str(user.password)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found quoi')

    print(f"Mon user id est : {user.id}")
    print(f"Mon user id est type  : {type(user.id)}")

    access_token = create_access_token({"sub": str(user.id), "role": user.role})

    return TokenProvider(
        access_token=access_token,
        token_type="Bearer",
    )


@gsb_mobile_auth_router.delete("/logout", response_model=LogoutMessage)
def logout(authorization: str = Header(...)):
    token = authorization.replace("Bearer", "").strip()

    add_token_to_blacklist(token)

    return LogoutMessage(message="Token ajouté à la BL")
