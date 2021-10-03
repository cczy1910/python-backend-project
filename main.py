from graphene import Schema
from starlette.graphql import GraphQLApp
from fastapi import FastAPI, Path, Response, status
from fastapi.param_functions import Body, Query

from app.models import Category, Credentials, Item, RegisterForm
import app.data.data_access as DataAccess
import app.categories as Categories
import app.items as Items
import app.discounts as Discounts
import app.users as Users
import app.graphql_schema as AppGraphQLSchema


app = FastAPI()


@app.on_event("startup")
async def startup():
    DataAccess.initialize()

app.add_route("/category/query", GraphQLApp(schema=Schema(query=AppGraphQLSchema.Query)))


@app.get("/category/{categoryId}")
async def get_category(response: Response, categoryId: int = Path(..., ge=1)):
    category = Categories.getCategory(categoryId)
    if category is None:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        return category


@app.post("/category")
async def add_category(response: Response, category: Category = Body(...)):
    Categories.addCategory(category)
    response.status_code = status.HTTP_200_OK


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
