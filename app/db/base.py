from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.db.models import user_model, post_model, comment_model
