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

class PostEdit(BaseModel):
    title: constr(min_length=3, max_length=20) | None = None
    content: str | None = None
    

class PostCreate(BaseModel):
    user_id: int
    title: constr(min_length=3, max_length=20)
    content: str

class TagCreate(BaseModel):
    name: str

class TagEdit(BaseModel):
    name: str | None = None

class CategoryCreate(BaseModel):
    name: str
    description: str | None = None

class CategoryEdit(BaseModel):
    name: str | None = None
    description: str | None = None

class UserCreate(BaseModel):
    username: str
    email: str
    bio: str | None = None
    profile_picture: str | None = None

class UserEdit(BaseModel):
    username: str | None = None
    email: str | None = None
    bio: str | None = None
    profile_picture: str | None = None


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