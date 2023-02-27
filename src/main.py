from fastapi import FastAPI, File, Form, Header, HTTPException, UploadFile

import models_post.models
from dependencies.app import router_dependencies
from jsons.app import router_jsons
from models_post.database import engine
from models_post.router import router_models_psgs
from modeltype.app import model_router
from users.api import user_router
from users.model import ModelRole

models_post.models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(model_router)
app.include_router(router_jsons)
app.include_router(router_dependencies)
app.include_router(router_models_psgs)


@app.get("/", deprecated=True)
def home():
    return {"key": "Hello"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get("/models/{model_role}")
async def get_model(model_role: ModelRole):
    if model_role is ModelRole.manager:
        return {"model_role": model_role, "message": "your role is manager"}

    if model_role.value == "user":
        return {"model_role": model_role, "message": "your role is user"}

    return {"model_role": model_role, "message": "your role is admin"}


@app.get("/header/")
# async def read_items(user_agent: str | None = Header(default=None)):
#     return {"User-Agent": user_agent}
# async def read_items(
#     strange_header: str | None = Header(default=None, convert_underscores=False)
# ):
#     return {"strange_header": strange_header}
async def read_items(x_token: list[str] | None = Header(default=None)):
    return {"X-Token values": x_token}


@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}


# @app.post("/files/")
# async def create_file(file: bytes = File()):
#     return {"file_size": len(file)}


# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}
@app.post("/files/")
async def create_files(
    files: list[bytes] = File(description="Multiple files as bytes"),
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(
    files: list[UploadFile] = File(description="Multiple files as UploadFile"),
):
    return {"filenames": [file.filename for file in files]}


@app.post("/files_token/")
async def create_file(file: bytes = File(), uploadfile: UploadFile = File(), token: str = Form()):
    return {
        "file_size": len(file),
        "fileb_content_type": uploadfile.content_type,
        "token": token,
    }


items = {"foo": "The Foo Wrestlers"}


@app.get("/itemsexception/{item_id}")
async def read_item(item_id: str):
    """input: foo"""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
