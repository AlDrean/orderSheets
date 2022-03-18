import datetime
from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    hashId: str
    price: float


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    active: bool

    class Config:
        orm_mode = True


class OrderSheetBase(BaseModel):
    hash_order_id: str


class OrderSheetCreate(OrderSheetBase):
    items: List[int]


class OrderSheet(OrderSheetBase):
    id: int
    item: int
    consumed: bool
    consumed_location: str
    consumed_time: str

    class Config:
        orm_mode = True
