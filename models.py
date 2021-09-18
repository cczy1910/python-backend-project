from typing import Optional
from pydantic import BaseModel
from pydantic.fields import Field

class ItemIn(BaseModel):
    username: str
    password: str
    price: float = Field(ge=0)
    item_name: str = Field(min_length=3, max_length=64)

class ItemOut(BaseModel):
    username: str
    price: float
    item_name: str