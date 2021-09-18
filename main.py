from models import ItemIn, ItemOut
from fastapi import FastAPI, Path, Response, status
from fastapi.param_functions import Body, Query

app = FastAPI()

credentials = {
    "Alice":"12345",
    "Bob":"qwerty",
    "admin":"admin"
}

@app.get("/item/{item_number}")
async def get_item(item_number: int = Path(..., ge=1, le=10)):
    return {"item_price": item_number * (item_number + 1) // 2}

@app.post("/item", response_model=ItemOut)
async def calculate_discount(item: ItemIn, response: Response):
    if item.username in credentials and credentials[item.username] == item.password:
        return ItemOut(
            username = item.username,
            price = item.price * 0.8,
            item_name = item.item_name + " (Скидка)"
        )
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED