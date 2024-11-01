from datetime import datetime
from pydantic import BaseModel

from app.schemas.user import UserResponse


class PostCreate(BaseModel):
    content: str


class PostResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    last_modified: datetime | None
    owner: UserResponse

    class Config:
        from_attributes = True