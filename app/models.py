from typing import Optional
from pydantic import BaseModel
from pydantic.fields import Field


class User(BaseModel):
    id: int
    username: str
    password_hash: str
    discount: Optional[float]


class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: Optional[int]


class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=3, max_length=16)


class RegisterForm(BaseModel):
    id: int
    credentials: Credentials

class Category(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]