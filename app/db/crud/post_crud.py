
from sqlalchemy import update, delete, select, insert, func, join
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import Session
from app.db.models.post_model import Post
from app.db.models.user_model import User
from app.schemas.post import PostCreate


def create_post(db: Session, post: PostCreate, owner_id: int):
    result = db.execute(insert(Post)
                        .values(**post.dict(), owner_id=owner_id)
                        .returning(Post))

    new_post = result.scalars().first()
    db.commit()
    return new_post


def get_users_posts(db: Session, user_id: int):
    result = db.execute(select(Post)
                        .where(Post.owner_id == user_id)         # type: ignore
                        .where(Post.is_blocked.is_(False)))
    return result.scalars().all()


def get_post(db: Session, post_id: int):
    result = db.execute(select(Post)
                        .where(Post.id == post_id)              # type: ignore
                        .where(Post.is_blocked.is_(False)))
    return result.scalars().first()


def get_all_posts(db: Session, limit: int = 100, offset: int = 0):
    result = db.execute(select(Post)
                        .where(Post.is_blocked.is_(False))
                        .limit(limit)
                        .offset(offset))
    return result.scalars().all()


def check_post_owner(db: Session, post_id: int, owner_id: int):
    result = db.execute(select(Post)
                        .where(Post.id == post_id)              # type: ignore
                        .where(Post.owner_id == owner_id))
    return result.scalars().first()


def update_post(db: Session, post_id: int, post_data: PostCreate):
    result = db.execute(update(Post)
                        .where(Post.id == post_id)  # type: ignore
                        .where(Post.is_blocked.is_(False))
                        .values(**post_data.model_dump(), last_modified=func.now())
                        .returning(Post))

    updated_post = result.scalars().first()
    db.commit()
    return updated_post


def delete_post(db: Session, post_id: int) -> bool:
    result = db.execute(delete(Post)
                        .where(Post.id == post_id))  # type: ignore
    db.commit()
    return result.rowcount > 0


def ban_post(db: Session, post_id: int):
    db.execute(update(Post)
               .where(Post.id == post_id)               # type: ignore
               .values(is_blocked=True))
    db.commit()


"""
Comments related
"""


def get_post_comments(db: Session, post_id: int):
    result = db.execute(select(Post)
                        .options(selectinload(Post.comments))
                        .where(Post.id == post_id)               # type: ignore
                        .where(Post.is_blocked.is_(False)))
    post = result.scalars().first()
    return post.comments if post else None


"""
Auto reply related
"""


def get_autoreply_data(db: Session, post_id: int):
    result = db.execute(select(User)
                        .join(Post)
                        .where(Post.id == post_id)        # type: ignore
                        )
    user = result.scalars().first()
    return user.auto_reply, user.auto_reply_delay, user.id



