import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_modified = Column(DateTime, default=None)
    is_blocked = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
