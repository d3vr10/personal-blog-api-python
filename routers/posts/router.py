import sqlite3
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, constr
from lib.db.db import delete, update_post, delete_post, insert_post
from lib.db.db import get_by_field, get_db_connection, update
from lib.db.models import PostCreate, PostEdit

router = APIRouter(
    prefix="/posts",
)


@router.get("")
async def GET_ALL():
    with get_db_connection() as db:
        posts = get_by_field("Post", db)
        return posts

@router.get("/{post_id}")
async def GET(post_id: int):
    with get_db_connection() as db:
        post = get_by_field("Post", db, where={"id": post_id}, single=True)
        return post

@router.put("/{post_id}")
async def PUT(post_id: int, post: PostEdit):
    with get_db_connection() as db:
        try:
            update_post(
                db, 
                post.model_dump(exclude_defaults=True), 
                where={"id": post_id},
            )
            post = get_by_field("Post", db, where={"id": post_id}, single=True)
        except sqlite3.IntegrityError as e:
            msg = ""
            if "user_id" in str(e):
                msg = "User already exists"
            elif "title" in str(e):
                msg = "Title already exists"
            raise HTTPException(status_code=400, detail=msg)
        return post
    
@router.delete("/{post_id}")
async def DELETE(post_id: int):
    with get_db_connection() as db:
        delete_post(db, where={"id": post_id})

@router.post("")
async def POST(post: PostCreate):
    with get_db_connection() as db:
        try:
            result = insert_post(
                db, 
                post.model_dump(),
            )
        except sqlite3.IntegrityError as e:
            msg = str(e)
            if "user_id" in str(e):
                msg = "Username already exists"
            elif "title" in str(e):
                msg = "Title already exists"
            raise HTTPException(status_code=400, detail=msg)
            
        return result
    