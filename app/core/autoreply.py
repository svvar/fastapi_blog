from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.db.crud import post_crud as post_crud, comment_crud as comment_crud
from app.ai.ai_tools import reply_comment
from app.schemas.comment import CommentResponse


scheduler = BackgroundScheduler()


def schedule_reply(db: Session, comment: CommentResponse, reply_from: int, delay: int):
    post_id = comment.post_id
    post_text = post_crud.get_post(db, post_id).content

    reply_text = reply_comment(post_text, comment.content)

    scheduler.add_job(comment_crud.create_comment, 'date', run_date=datetime.now() + timedelta(minutes=delay),
                      args=[db, reply_text, post_id, reply_from, comment.id])


scheduler.start()
