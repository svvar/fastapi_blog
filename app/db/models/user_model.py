from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    auto_reply = Column(Boolean, default=False)
    auto_reply_delay = Column(Integer, default=5)

    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")

