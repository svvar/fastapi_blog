from datetime import date

from sqlalchemy import update, delete, select, insert, func, and_, Integer
from sqlalchemy.orm import Session
from app.db.models.comment_model import Comment
from app.schemas.analytics import CommentAnalyticsResponse, CommentAnalytics
from app.schemas.comment import CommentUpdate


def create_comment(db: Session, comment_content: str, post_id: int, owner_id: int, reply_to: int = None):
    result = db.execute(insert(Comment)
                        .values(content=comment_content, post_id=post_id, owner_id=owner_id, reply_to=reply_to)
                        .returning(Comment))

    new_comment = result.scalars().first()
    db.commit()
    return new_comment


def get_comment(db: Session, comment_id: int):
    result = db.execute(select(Comment)
                        .where(Comment.id == comment_id)                # type: ignore
                        .where(Comment.is_blocked.is_(False)))
    return result.scalars().first()


def get_comments_of_post(db: Session, post_id: int, limit: int = 100, offset: int = 0):
    result = db.execute(select(Comment)
                        .where(Comment.post_id == post_id)              # type: ignore
                        .where(Comment.is_blocked.is_(False))
                        .limit(limit)
                        .offset(offset))
    return result.scalars().all()


def update_comment(db: Session, comment_id: int, comment_data: CommentUpdate):
    result = db.execute(update(Comment)
                        .where(Comment.id == comment_id)  # type: ignore
                        .where(Comment.is_blocked.is_(False))
                        .values(**comment_data.dict(), last_modified=func.now())
                        .returning(Comment))

    updated_comment = result.scalars().first()
    db.commit()
    return updated_comment


def delete_comment(db: Session, comment_id: int):
    db.execute(delete(Comment)
               .where(Comment.id == comment_id))  # type: ignore
    db.commit()


def ban_comment(db: Session, comment_id: int):
    db.execute(update(Comment)
               .where(Comment.id == comment_id)  # type: ignore
               .values(is_blocked=True))
    db.commit()


def get_comments_daily_breakdown(
        db: Session,
        date_from: date,
        date_to: date,
) -> CommentAnalyticsResponse:
    result = db.execute(select(
        func.date(Comment.created_at).label('date'),
        func.count(Comment.id).label('total_comments'),
        func.sum(Comment.is_blocked.cast(Integer)).label('blocked_comments')
    )
                        .where(and_(func.date(Comment.created_at) >= date_from,
                                    func.date(Comment.created_at) <= date_to))
                        .group_by(func.date(Comment.created_at))
                        .order_by(func.date(Comment.created_at)))
    result = result.fetchall()
    # daily_comments = [
    #     DailyCommentAnalytics(date=row.date, total_comments=row.total_comments, blocked_comments=row.blocked_comments)
    #     for row in result]
    daily_comments = {row.date: CommentAnalytics(total_comments=row.total_comments, blocked_comments=row.blocked_comments)
                      for row in result}

    total_comments, blocked_comments = 0, 0
    for _, analytics in daily_comments.items():
        total_comments += analytics.total_comments
        blocked_comments += analytics.blocked_comments

    return CommentAnalyticsResponse(
        summary=CommentAnalytics(
            total_comments=total_comments,
            blocked_comments=blocked_comments
        ),
        daily_breakdown=daily_comments
    )

