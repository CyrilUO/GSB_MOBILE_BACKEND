from fastapi import APIRouter

from app.modules.auth.controller import gsb_mobile_auth_router
from app.modules.products.controller import gsb_mobile_product_router
from app.modules.users.controller import gsb_mobile_user_router

global_router = APIRouter()

global_router.include_router(gsb_mobile_auth_router)
global_router.include_router(gsb_mobile_user_router)
global_router.include_router(gsb_mobile_product_router)
