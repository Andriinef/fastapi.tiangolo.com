from fastapi import Body, Query
from fastapi.routing import APIRouter

from users.model import Image, Item, Offer, User

user_router = APIRouter(prefix="/items", tags=["user"])


@user_router.get("/{item_id}")
async def read_user_item(
    item_id: int,
    user: str,
    description: str,
    query: str | None = None,
    short: bool = False,
    skip: int = 0,
    limit: int | None = None,
):
    item = {
        "item_id": item_id,
        "user": user,
        "description": description,
        "query": query,
        "short": short,
        "skip": skip,
        "limit": limit,
    }
    return item


@user_router.post("/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@user_router.post("/offers/")
async def create_offer(offer: Offer):
    return offer


@user_router.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images


@user_router.put("/{item_id}")
# async def create_item(item_id: int, item: Item, query: str | None = None):
#     result = {"item_id": item_id, **item.dict()}
#     if query:
#         result.update({"query": query})
#     return result
# async def read_items(
#     *,
#     item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
#     query: str,
#     size: float = Query(gt=0, lt=10.5, title="0 - 10.5")
# ):
#     results = {"item_id": item_id}
#     if query:
#         results.update({"query": query})
#     return results
async def update_item(
    *,
    item_id: int,
    item: Item = Body(embed=True),
    user: User,
    importance: int = Body(default=None),
    query: str | None = None,
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if query:
        results.update({"query": query})
    return results


@user_router.get("/")
# async def read_items(query: list[str] | None = Query(default=None)):
#     query_items = {"query": query}
#     return query_items
# async def read_items(query: list = Query(default=[])):
#     query_items = {"query": query}
#     return query_items
async def read_items(
    query: str
    | None = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if query:
        results.update({"query": query})  # type: ignore
