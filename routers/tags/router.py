import sqlite3
from fastapi import APIRouter, HTTPException
from lib.db.db import get_by_field, get_db_connection, insert_tag, update_tag, delete_tag
from lib.db.models import TagCreate

router = APIRouter(prefix="/tags")

@router.get("")
async def GET_ALL():
    with get_db_connection() as db:
        rows = get_by_field("Tag", db)
        return rows
    

@router.get("/{tag_name}")
async def GET(tag_name: str):
    with get_db_connection() as db:
        rows = get_by_field("Tag", db, where={"name": tag_name})
        if not rows:
            raise HTTPException(404, detail='Tag "{tag_name}" wasn\'t found!')
        return rows

@router.post("")
async def POST(tag: TagCreate):
    with get_db_connection() as db:
        try:
            row = insert_tag(db, tag.model_dump())
            return row
        except sqlite3.IntegrityError as err:
            msg = str(err)
            if "name" in str(err):
                msg = f'Tag with this name ("{tag.name}") already exists'
            raise HTTPException(status_code=400, detail=msg)

@router.put("/{tag_name}")
async def PUT(tag_name: str, tag: TagCreate):
    with get_db_connection() as db:
        rows = update_tag(db, tag.model_dump(exclude_defaults=True), where={"name": tag_name})
        return rows

@router.delete("/{tag_name}")
async def DELETE(tag_name: str):
    with get_db_connection() as db:
        result = delete_tag(db, where={"name": tag_name})
        if not result > 0:
            return {"msg": f'Tag "{tag_name}" wasn\'t found'}

        return {"msg": f'Deleted tag "{tag_name}"'}
        

        
