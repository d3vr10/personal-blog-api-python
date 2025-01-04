from contextlib import asynccontextmanager
from fastapi import FastAPI
from lib.db.init import init
from routers.posts.router import router as posts_router
from routers.users.router import router as users_router
from routers.tags.router import router as tags_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    ## Init tasks
    init()
    yield
    ## Cleanup

app = FastAPI(lifespan=lifespan)
app.include_router(posts_router)
app.include_router(users_router)
app.include_router(tags_router)