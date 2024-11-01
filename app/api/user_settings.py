from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session


from app.db.crud.user_crud import autoreply_on, autoreply_off
from app.schemas.user import User, AutoReply
from app.db.session import get_db
from app.core.security import get_current_user

router = APIRouter()


@router.post("/autoreply/on")
def turn_autoreply_on(
        delay: AutoReply,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    autoreply_on(db, user.id, delay.auto_reply_delay)
    return {"message": f"Autoreply enabled. Delay: {delay.auto_reply_delay} minute(s)"}


@router.post("/autoreply/off")
def turn_autoreply_off(
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    autoreply_off(db, user.id)
    return {"message": "Autoreply disabled"}
