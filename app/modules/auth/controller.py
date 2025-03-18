from typing import Set

from typing_extensions import Annotated

from app.core.security import get_current_user
from app.modules import RoleEnum
from app.modules.auth.schema import FormData, TokenProvider, LogoutMessage
from fastapi import APIRouter, Depends, HTTPException, Form, status, Header
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.modules.users.db_model import UserModel
from app.utils.jwt import create_access_token, verify_access_token
from app.utils.hash import verify_password
from app.utils.token_blacklist import BLACKLISTED_TOKENS, add_token_to_blacklist

gsb_mobile_auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
e = RoleEnum


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


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


@gsb_mobile_auth_router.delete("/logout", response_model=LogoutMessage)
def logout(
        credentials: HTTPAuthorizationCredentials = Depends(security),  # ✅ Gère mieux Authorization
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value, e.user.value]))
):
    token = credentials.credentials
    print(f"Le toekn est {token}")  # ✅ Extrait le token proprement

    add_token_to_blacklist(token)

    return LogoutMessage(message="Token ajouté à la BL")
