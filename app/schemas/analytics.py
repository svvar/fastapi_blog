from pydantic import BaseModel
from datetime import date


class CommentAnalytics(BaseModel):
    total_comments: int
    blocked_comments: int


class CommentAnalyticsResponse(BaseModel):
    summary: CommentAnalytics
    daily_breakdown: dict[date, CommentAnalytics]

