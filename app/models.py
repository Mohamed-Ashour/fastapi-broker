from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class StockLog(Base):
    __tablename__ = "stocks_logs"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(String)
    name = Column(String)
    price = Column(Integer)
    availability = Column(Integer)
    timestamp = Column(DateTime)


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(String)
    name = Column(String)
    price = Column(Integer)
    availability = Column(Integer)
    timestamp = Column(DateTime)
    users = relationship("Ownership", back_populates="stock")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fund = Column(Integer, default=0)
    stocks = relationship("Ownership", back_populates="user")


class Ownership(Base):
    __tablename__ = 'ownership'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'), primary_key=True)
    own = Column(Integer)
    user = relationship("User", back_populates="stocks")
    stock = relationship("Stock", back_populates="users")
