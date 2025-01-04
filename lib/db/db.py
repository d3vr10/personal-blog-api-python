from functools import partial
import sqlite3
from textwrap import dedent
from typing import Callable
from lib.db.models import Category, Comment, Model, Post, PostTags, User, Tag

def create_pool():
    conn = sqlite3.connect(":memory:")
    def wrapper():
        return conn
    return wrapper


def insert(Model: Model, db: sqlite3.Connection, attrs: dict, autocommit=False):
    instance = Model(**attrs)
    sql, params = make_insert_sql(Model.display_name, **instance.model_dump())
    rows = db.execute(sql, params).fetchone()

    if autocommit is True:
        db.commit()

    return rows

def make_insert_sql(table: str, **kwargs):
    keys = kwargs.items()
    columns = map(lambda x: x[0], keys)
    values = tuple(map(lambda y: y[1], keys))
    sql = dedent(f"""
        INSERT INTO {table} 
        ({",".join(columns)}) VALUES ({",".join(len(values) * "?")})
        RETURNING *;
    """)
    return (sql, values)

def get_by_field(
    table: str, 
    db: sqlite3.Connection, 
    columns: list | None = None, 
    where: dict = {},
    single: bool = False,
    limit: int = 0,
):
    if single: limit = 1
    default_column = "*"
    ## Query Building stage
    sql = 'SELECT {columns} FROM {table} {where_expr} {limit};'
    items = where.items()
    where_expr = " AND ".join(
        map(
            lambda pair: "=".join((pair[0], "?")),
            items,
        )
    )
    if where_expr:
        where_expr = "WHERE " + where_expr

    if columns: 
        select_expr = ", ".join(columns)
    else: 
        select_expr = default_column

    sql = sql.format(
        where_expr=where_expr, 
        table=table, 
        columns=select_expr, 
        limit="" if limit == 0 else f"LIMIT {limit}",
    )
    params = tuple(value for _, value in items)

    ## Perform and return query
    cursor = db.execute(sql, params)

    if single: 
        return cursor.fetchone()

    return cursor.fetchall()
        
def update(Model: Model, db: sqlite3.Connection, attrs: dict, where: dict, autocommit=False):
    if len(attrs) == 0:
        raise ValueError("No attributes to update")
    keys = attrs.items()
    set_expr = ", ".join(map(lambda x: f"{x[0]} = ?", keys))
    where_expr = " AND ".join(map(lambda pair: f"{pair[0]} = ?", where.items()))
    sql = dedent(f"""
        UPDATE {Model.display_name} 
        SET {set_expr} 
        WHERE {where_expr}
        RETURNING *;
    """)
    params = tuple(map(lambda y: y[1], keys)) + tuple(map(lambda y: y[1], where.items()))
    rows = db.execute(sql, params).fetchall()

    if autocommit:
        db.commit()

    return rows

def delete(table: str, db: sqlite3.Connection, where: dict, autocommit=False):
    where_expr = " AND ".join(map(lambda pair: f"{pair[0]} = ?", where.items()))
    sql = f"DELETE FROM {table} WHERE {where_expr};"
    params = tuple(map(lambda y: y[1], where.items()))

    cursor = db.execute(sql, params)

    if autocommit:
        db.commit()
    
    return cursor.rowcount



insert_user: Callable = partial(insert, User)
insert_comment: Callable = partial(insert, Comment)
insert_post: Callable = partial(insert, Post)
insert_post_tags: Callable = partial(insert, PostTags)
insert_category: Callable = partial(insert, Category)
insert_tag: Callable = partial(insert, Tag)

update_user: Callable = partial(update, User)
update_comment: Callable = partial(update, Comment)
update_post: Callable = partial(update, Post)
update_posttags: Callable = partial(update, PostTags)
update_category: Callable = partial(update, Category)
update_tag: Callable = partial(update, Tag)

delete_user: Callable = partial(delete, "User")
delete_post: Callable = partial(delete, "Post")
delete_posttags: Callable = partial(delete, "PostTags")
delete_tag: Callable = partial(delete, "Tag")
delete_category: Callable = partial(delete, "Category")

get_db_connection: Callable = create_pool()

