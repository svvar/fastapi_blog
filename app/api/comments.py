from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.ai.ai_tools import moderate_text
from app.core.security import get_current_user
from app.core.autoreply import schedule_reply
from app.db.crud import comment_crud as comment_crud
from app.db.crud import post_crud as post_crud
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.schemas.user import User
from app.schemas.analytics import CommentAnalyticsResponse
from app.db.session import get_db

router = APIRouter()


@router.get("/daily-breakdown", response_model=CommentAnalyticsResponse)
def get_daily_comments_breakdown(
        date_from: date = Query(...),
        date_to: date = Query(...),
        db: Session = Depends(get_db)
):
    if date_from > date_to:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="date_from must be before date_to")

    return comment_crud.get_comments_daily_breakdown(db, date_from, date_to)


@router.post("/post/{post_id}", response_model=CommentResponse)
def create_comment(
        post_id: int,
        comment_data: CommentCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    if not post_crud.get_post(db, post_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    comment = comment_crud.create_comment(db, comment_data.content, post_id, current_user.id, comment_data.reply_to)

    if 'BAN' in moderate_text(comment_data.content):
        comment_crud.ban_comment(db, comment.id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Comment contains inappropriate content")

    reply_on, delay, user_id = post_crud.get_autoreply_data(db, post_id)
    if reply_on and user_id != current_user.id:
        schedule_reply(db, comment, user_id, delay)

    return comment


@router.get("/post/{post_id}", response_model=list[CommentResponse])
def show_post_comments(
        post_id: int,
        page: int = Query(1, ge=1),
        db: Session = Depends(get_db)
):
    page_size = 100
    comments = comment_crud.get_comments_of_post(db, post_id, limit=page_size, offset=(page - 1) * page_size)
    if not comments and page > 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")

    return comments


@router.get("/{comment_id}", response_model=CommentResponse)
def read_comment(
        comment_id: int,
        db: Session = Depends(get_db)):
    comment = comment_crud.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


@router.patch("/{comment_id}", response_model=CommentResponse)
def update_comment(
        comment_id: int,
        comment_data: CommentUpdate,
        db: Session = Depends(get_db)
):
    comment = comment_crud.update_comment(db, comment_id, comment_data)

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    if 'BAN' in moderate_text(comment_data.content):
        comment_crud.ban_comment(db, comment_id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Comment contains inappropriate content")

    return comment


@router.delete("/{comment_id}", response_model=CommentResponse)
def delete_comment(
        comment_id: int,
        db: Session = Depends(get_db)
):
    comment = comment_crud.delete_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment




