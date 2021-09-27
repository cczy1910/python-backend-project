import app.data.data_access as data_access
from typing import Optional
from pydantic.main import BaseModel
from app.models import Credentials, Item, RegisterForm
from fastapi import FastAPI, Path, Response, status
from fastapi.param_functions import Body, Query

import app.items as Items
import app.discounts as Discounts
import app.users as Users


app = FastAPI()


@app.on_event("startup")
async def startup():
    data_access.initialize()


@app.get("/item/{itemId}")
async def get_item(response: Response, itemId: int = Path(..., ge=1)):
    item = Items.getItem(itemId)
    if item is None:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        return item


@app.post("/item/{itemId}/discount")
async def get_item_discounted(response: Response, itemId: int = Path(..., ge=1), credentials: Credentials = Body(...)):
    item = Discounts.getDiscounted(credentials, itemId)
    if item is None:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        return item


@app.post("/item")
async def add_item(response: Response, item: Item = Body(...)):
    Items.addItem(item)
    response.status_code = status.HTTP_200_OK


@app.post("/user/register")
async def add_item(response: Response, registerForm: RegisterForm = Body(...)):
    Users.register(registerForm)
    response.status_code = status.HTTP_200_OK


@app.post("/user/{userId}/discount")
async def add_item(response: Response, userId: int = Path(..., ge=1), discount: float = Query(..., gt=0, le=1)):
    Users.setDiscount(userId, discount)
    response.status_code = status.HTTP_200_OK

@app.get("/user/{userId}")
async def get_item(response: Response, userId: int = Path(..., ge=1)):
    user = Users.getUser(userId)
    if user is None:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        return user
