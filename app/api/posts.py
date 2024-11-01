from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.ai.ai_tools import moderate_text
from app.core.security import get_current_user
from app.db.crud import post_crud as post_crud
from app.schemas.user import User
from app.schemas.post import PostCreate, PostResponse
from app.schemas.comment import CommentResponse
from app.db.session import get_db

router = APIRouter()


@router.get("/", response_model=list[PostResponse])
def show_posts(
        page: int = Query(1, ge=1),
        db: Session = Depends(get_db)
):
    page_size = 50
    posts = post_crud.get_all_posts(db, limit=page_size, offset=(page - 1) * page_size)
    if not posts and page > 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")

    return posts


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
        post: PostCreate,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if not post.content:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Content is required")

    created_post = post_crud.create_post(db, post, user.id)

    if 'BAN' in moderate_text(post.content):
        post_crud.ban_post(db, created_post.id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post contains inappropriate content")

    return created_post


@router.get("/my", response_model=list[PostResponse])
def show_my_posts(
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    result = post_crud.get_users_posts(db, user.id)
    return result


@router.get("/{post_id}", response_model=PostResponse)
def read_post(
        post_id: int,
        db: Session = Depends(get_db)
):
    post = post_crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.get("/{post_id}/comments", response_model=list[CommentResponse])
def get_post_comments(
        post_id: int,
        db: Session = Depends(get_db)
):
    if not post_crud.get_post(db, post_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    comments = post_crud.get_post_comments(db, post_id)
    return comments


@router.patch("/{post_id}", response_model=PostResponse)
def update_post(
        post_id: int,
        post_data: PostCreate,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if not post_data.content:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Content is required")

    if not post_crud.check_post_owner(db, post_id, user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this post")

    post = post_crud.update_post(db, post_id, post_data)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if 'BAN' in moderate_text(post_data.content):
        post_crud.ban_post(db, post.id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post contains inappropriate content")

    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
        post_id: int,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):

    if not post_crud.check_post_owner(db, post_id, user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this post")

    post_crud.delete_post(db, post_id)






