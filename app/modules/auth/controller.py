from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.modules.users.db_model import User
from app.utils.jwt import create_access_token
from app.utils.hash import verify_password

gsb_mobile_auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@gsb_mobile_auth_router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, str(user.password)):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id), "role": user.role})

    return {"access_token": access_token, "token_type": "bearer"}


