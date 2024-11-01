from dotenv import load_dotenv
from fastapi import FastAPI

from app.api import auth, posts, comments, user_settings

load_dotenv()

app = FastAPI()
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
app.include_router(user_settings.router, prefix="/settings", tags=["settings"])


@app.get("/")
def root():
    return {"message": "Hello API check"}


