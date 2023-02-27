# from typing import Any
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel, EmailStr
from starlette.responses import Response

from modeltype.model import UserOut, fake_save_user

model_router = APIRouter(tags=["modeltype"])
app = model_router


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    # response_model_include=["name", "description"],
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get(
    "/items/{item_id}/public",
    response_model=Item,
    # response_model_exclude=["tax"]
)
async def read_item_public_data(item_id: str):
    return items[item_id]


@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]


# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: str | None = None


# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None


# @app.post("/user/", response_model=UserOut)
# async def create_user(user: UserIn) -> Any:
#     return user


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str


# @app.post("/user/")
# async def create_user(user: UserIn) -> BaseUser:
#     return user


@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})


@app.get("/teleport")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)  # type: ignore
    return user_saved
