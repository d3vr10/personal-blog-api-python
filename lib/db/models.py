from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import ClassVar, TypedDict

class ModelMeta(type(BaseModel)):
    def __new__(cls, name, bases, attrs):
        if name != "Model":
            attrs["display_name"] = name.capitalize()
        return super().__new__(cls, name, bases, attrs)

class Model(BaseModel, metaclass=ModelMeta):
    display_name: ClassVar[str]


class User(Model):
    id: int | None = None
    username: constr(min_length=3, max_length=15)
    email: EmailStr
    password: str | None = None
    bio: str | None = None
    profile_picture: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Post(Model):
    id: int | None = None
    user_id: int
    title: constr(min_length=3, max_length=40)
    content: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    published_at: datetime | None = None


class Comment(Model):  
    id: int | None = None
    user_id: int
    post_id: int
    content: constr(min_length=1, max_length=500)
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Category(Model):
    id: int | None = None
    name: str
    created_at: datetime | None = None


class Tag(Model):
    id: int | None = None
    name: str
    created_at: datetime | None = None

class PostTags(Model):
    tag_id: int
    post_id: int 