from functools import partial
import sqlite3
from textwrap import dedent
from lib.db.models import Category, Comment, Model, Post, PostTags, User, Tag

def insert(Model: Model, db: sqlite3.Connection, attrs: dict, autocommit=False):
    instance = Model(**attrs)
    sql, params = make_insert_sql(Model.display_name, **instance.model_dump())
    db.execute(sql, params)

    if autocommit is True:
        db.commit()


def make_insert_sql(table, **kwargs):
    keys = kwargs.items()
    columns = map(lambda x: x[0], keys)
    values = tuple(map(lambda y: y[1], keys))
    sql = f"INSERT INTO {table} ({",".join(columns)}) VALUES ({",".join(len(values) * "?")});"
    return (sql, values)



insert_user = partial(insert, User)
insert_comment = partial(insert, Comment)
insert_post = partial(insert, Post)
insert_post_tags = partial(insert, PostTags)
insert_category = partial(insert, Category)
insert_tag = partial(insert, Tag)