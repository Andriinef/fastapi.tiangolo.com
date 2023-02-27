from dataclasses import dataclass

from fastapi import Depends
from fastapi.routing import APIRouter

router_dependencies = APIRouter(tags=["dependencies"])
app = router_dependencies


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@dataclass
class CommonQueryParams:
    q: str | None = None
    skip: int = 0
    limit: int = 100


@app.get("/items_common/")
async def read_items_common(commons: CommonQueryParams = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response
