from fastapi import FastAPI
from lib.db.init import init
from routers.posts.router import router as posts_router
from routers.users.router import router as users_router

init()
app = FastAPI()
app.include_router(posts_router)
app.include_router(users_router)