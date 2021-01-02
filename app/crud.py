from datetime import date, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from app import models, schemas


def add_stock(db: Session, new_stock: schemas.Stock) -> models.Stock:
    stock = db.query(models.Stock).filter(models.Stock.stock_id == new_stock.stock_id).first()
    if stock:
        stock.price = new_stock.price
        stock.availability = new_stock.availability
        stock.timestamp = new_stock.timestamp
    else:
        stock = models.Stock(**new_stock.dict())
        db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock


def add_stock_log(db: Session, new_stock: schemas.Stock) -> models.StockLog:
    stock_log_obj = models.StockLog(**new_stock.dict())
    db.add(stock_log_obj)
    db.commit()
    db.refresh(stock_log_obj)
    return stock_log_obj


def user_deposit(db: Session, user: models.User, amount: int) -> models.User:
    user.fund += amount
    db.commit()
    db.refresh(user)
    return user


def user_withdraw(db: Session, user: models.User, amount: int) -> models.User:
    user.fund -= amount
    db.commit()
    db.refresh(user)
    return user


def user_buy(db: Session, user: models.User, stock: models.Stock, total: int) -> models.User:
    try:
        ownership = next(s for s in user.stocks if s.stock_id == stock.id)
        ownership.own += total
    except StopIteration:
        ownership = models.Ownership(user_id=user.id, stock_id=stock.id, own=total)
        db.add(ownership)
    stock.availability -= total
    user.fund -= total * stock.price
    db.commit()
    db.refresh(user)
    return user


def user_sell(db: Session, user: models.User, stock: models.Stock, ownership: models.Ownership, total: int) \
        -> models.User:
    ownership.own -= total
    stock.availability += total
    user.fund += total * stock.price
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_stock(db: Session, stock_id: int) -> models.Stock:
    return db.query(models.Stock).filter(models.Stock.id == stock_id).first()


def get_stock_stats(db: Session, stock: models.Stock) -> schemas.StockResponse:
    stock.highest_price_today = db.query(func.max(models.StockLog.price)).filter(
        models.StockLog.stock_id == stock.stock_id,
        models.StockLog.timestamp.between(date.today(), date.today() + timedelta(days=1))
    ).one()[0]
    stock.lowest_price_today = db.query(func.min(models.StockLog.price)).filter(
        models.StockLog.stock_id == stock.stock_id,
        models.StockLog.timestamp.between(date.today(), date.today() + timedelta(days=1))
    ).one()[0]
    return stock
