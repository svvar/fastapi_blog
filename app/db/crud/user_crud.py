from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert
from app.schemas.user import UserCreate
from app.db.models.user_model import User
from app.core.security import get_password_hash, verify_password


def create_user(session: Session, user_data: UserCreate):
    hashed_password = get_password_hash(user_data.password)
    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=hashed_password)
    session.add(user)
    session.commit()
    return


def check_user_exists(session: Session, email: str):
    user = session.execute(select(User).where(User.email == email))                 # type: ignore
    user = user.scalars().first()
    return user


def authenticate_user(session: Session, email: str, password: str):
    user = session.execute(select(User).where(User.email == email))                 # type: ignore
    user = user.scalars().first()
    if user and verify_password(password, user.password):
        return user
    return None


def autoreply_on(session: Session, user_id: int, delay: int):
    session.execute(update(User)
                    .where(User.id == user_id)         # type: ignore
                    .values(auto_reply=True, auto_reply_delay=delay))
    session.commit()


def autoreply_off(session: Session, user_id: int):
    session.execute(update(User)
                    .where(User.id == user_id)         # type: ignore
                    .values(auto_reply=False))
    session.commit()

