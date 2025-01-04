import sqlite3
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from lib.db.db import get_by_field, get_db_connection, delete_user, update_user, insert_user
from lib.db.models import UserCreate, UserEdit

router = APIRouter(prefix="/users")


@router.get("/{user_id}")
async def GET(user_id: int):
    with get_db_connection() as db:
        user = get_by_field("User", db, where={"id": user_id}, single=True)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

@router.get("")
async def GET_ALL():
    with get_db_connection() as db:
        users = get_by_field("User", db)
        return users

@router.delete("/{user_id}")
async def DELETE(user_id: int):
    with get_db_connection() as db:
        delete_user(db, where={"id": user_id})
        db.commit()

        return {"message": "User deleted"}

@router.put("/{user_id}")
async def PUT(user_id: int, user: UserEdit):
    with get_db_connection() as db:
        try:
            result = update_user(
                db, 
                user.model_dump(exclude_defaults=True), 
                where={"id": user_id},
            )
            if not result:
                raise HTTPException(status_code=404, detail="User not found")

            db.commit()
            return result

        except sqlite3.IntegrityError as e:
            msg = ""
            if "email" in str(e):
                msg = "Email already exists"
            elif "username" in str(e):
                msg = "Username already exists"
            raise HTTPException(status_code=400, detail=msg)



@router.post("")
async def POST(user: UserCreate):
    with get_db_connection() as db:
        try:
            result = insert_user(db, user.model_dump())
        except sqlite3.IntegrityError as e:
            msg = ""
            if "email" in str(e):
                msg = "Email already exists"
            elif "username" in str(e):
                msg = "Username already exists"
            raise HTTPException(status_code=400, detail=msg)

        return result