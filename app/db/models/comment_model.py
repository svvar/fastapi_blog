import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_modified = Column(DateTime, default=None)
    is_blocked = Column(Boolean, default=False)
    reply_to = Column(Integer)
    owner_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))

    owner = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
