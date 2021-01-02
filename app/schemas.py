from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class Stock(BaseModel):
    stock_id: str
    name: str
    price: int
    availability: int
    timestamp: datetime


class StockResponse(Stock):
    id: int
    lowest_price_today: int
    highest_price_today: int

    class Config:
        orm_mode = True


class Ownership(BaseModel):
    stock_id: int
    user_id: int
    own: int

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    fund: int
    stocks: List[Ownership]

    class Config:
        orm_mode = True


class Transaction(BaseModel):
    user_id: int
    amount: int


class Invest(BaseModel):
    user_id: int
    stock_id: int
    total: int
    upper_bound: int
    lower_bound: int
