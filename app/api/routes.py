from app.modules.category.controller import gsb_mobile_category_router
from app.modules.comment.controller import gsb_mobile_comment_router
from app.modules.auth.controller import gsb_mobile_auth_router
from app.modules.products.controller import gsb_mobile_product_router
from app.modules.ratings.controller import gsb_mobile_rating_router
from app.modules.users.controller import gsb_mobile_user_router
from app.modules.article.controller import gsb_mobile_article_router


from fastapi import APIRouter

global_router = APIRouter(prefix='/api')

global_router.include_router(gsb_mobile_auth_router)
global_router.include_router(gsb_mobile_user_router)
global_router.include_router(gsb_mobile_product_router)
global_router.include_router(gsb_mobile_comment_router)
global_router.include_router(gsb_mobile_category_router)
global_router.include_router(gsb_mobile_article_router)
global_router.include_router(gsb_mobile_rating_router)
