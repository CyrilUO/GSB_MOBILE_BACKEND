from app.core.dependencies import get_db
from app.core.exceptions import HarmFullEnum
from app.core.security import get_current_user
from app.modules import UserModel, ArticleModel, ProductModel
from app.modules.comment.db_model import CommentModel
from app.modules.comment.schema import Comment, CreateComment, CommentResponse, UpdatedComment
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.modules.users.db_model import RoleEnum

gsb_mobile_comment_router = APIRouter(prefix="/comment", tags=["Comments"])
e = RoleEnum
h = HarmFullEnum


# Api work
@gsb_mobile_comment_router.get('/all', response_model=list[Comment])
def get_all_comments(
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value, e.user.value]))
):
    _current_user = current_user
    comments = db.query(CommentModel).all()

    if not comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No comments found")

    return [Comment(**c.__dict__) for c in comments]


# Api work
@gsb_mobile_comment_router.get('/{comment_id}', response_model=Comment)
def get_comment_by_id(
        comment_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value]))
):
    _current_user = current_user
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    return Comment.model_validate(comment)

#Api works
@gsb_mobile_comment_router.post('/create-comment', response_model=CommentResponse)
def post_comment(
        c: CreateComment,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value]))
):
    _current_user = current_user

    current_user_id = _current_user.get('sub', None)
    print(f"L'id du user actuel est : {current_user_id}")

    req = db.query(CommentModel).filter(CommentModel.user_id == current_user_id)

    if c.article_id is not None:
        req = req.filter(CommentModel.article_id == c.article_id)
    else:
        req = req.filter(CommentModel.article_id.is_(None))  # Vérifie NULL correctement

    if c.product_id is not None:
        req = req.filter(CommentModel.product_id == c.product_id)
    else:
        req = req.filter(CommentModel.product_id.is_(None))  # Vérifie NULL correctement

    commented = req.first()

    if commented:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Commentaire déjà existant pour cet article et produit')

    user = db.query(UserModel).filter(UserModel.id == c.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    if not c.content.strip():
        raise HTTPException(status_code=404, detail="Content is empty")

    new_comment = CommentModel(
        user_id=c.user_id,
        content=c.content,
        rating=c.rating,
        article_id=c.article_id,
        product_id=c.product_id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return CommentResponse(message=f"Commentaire n°{new_comment.id} posté ")

#Api working
@gsb_mobile_comment_router.put('/update-comment/{comment_id}', response_model=CommentResponse)
def update_comment(
        comment_id: int,
        uc: UpdatedComment,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value, e.user.value]))
):
    _user = current_user

    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    # Vérifier si l'utilisateur est bien l'auteur du commentaire ou qu'il soit admin
    if comment.user_id != _user.get('sub') and _user.get('role') != e.admin.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this comment")

    # Mise à jour des champs fournis
    updated_data = uc.model_dump(exclude_unset=True)
    for key, val in updated_data.items():
        setattr(comment, key, val)

    db.commit()
    db.refresh(comment)

    return CommentResponse(message=f"Commentaire id : {comment_id} mis à jour avec succès")


#Api works
@gsb_mobile_comment_router.delete('/delete-comment/{comment_id}', response_model=CommentResponse)
def delete_comment(
        comment_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user([e.admin.value, e.editor.value, e.user.value]))
):
    _user = current_user

    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail='Comment not found')

    # Vérifier que seul l'auteur ou un admin peut supprimer
    if comment.user_id != _user.get('sub') and _user.get("role") not in [e.admin.value, e.editor.value]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    db.delete(comment)
    db.commit()

    return CommentResponse(message=f"Commentaire id {comment_id} supprimé avec succès")
