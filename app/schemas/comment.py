
from pydantic import BaseModel
from datetime import datetime


class CommentCreate(BaseModel):
    content: str
    reply_to: int | None = None


class CommentUpdate(BaseModel):
    content: str


class CommentResponse(CommentCreate):
    id: int
    content: str
    post_id: int
    created_at: datetime
    updated_at: datetime | None = None
    reply_to: int | None = None

    class Config:
        from_attributes = True
