from enum import Enum

from pydantic import BaseModel, Field, HttpUrl


class ModelRole(str, Enum):
    admin = "admin"
    manager = "manager"
    user = "user"


class Image(BaseModel):
    url: HttpUrl = Field(example="http://example.com/baz.jpg")
    name: str = Field(example="The Foo live")


class Item(BaseModel):
    name: str = Field(example="Foo")
    description: str | None = Field(default=None, example="A very nice Item")
    price: float = Field(example=35.4)
    tax: float | None = Field(default=None, example=3.2)
    tags: set[str] = Field(default=set(), example=["rock", "metal", "bar"])
    image: list[Image] | None = None


class User(BaseModel):
    username: str = Field(example="Den")
    full_name: str | None = Field(default=None, example="Ridi")


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]
