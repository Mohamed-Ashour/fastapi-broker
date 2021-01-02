import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, database
from seed import seed

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
seed()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.put("/deposit", response_model=schemas.User)
def deposit(transaction: schemas.Transaction, db: Session = Depends(get_db)):
    user = crud.get_user(db, transaction.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.user_deposit(db=db, user=user, amount=transaction.amount)


@app.put("/withdraw", response_model=schemas.User)
def withdraw(transaction: schemas.Transaction, db: Session = Depends(get_db)):
    user = crud.get_user(db, transaction.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.fund < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    return crud.user_withdraw(db=db, user=user, amount=transaction.amount)


@app.put("/buy", response_model=schemas.User)
def buy_stock(invest: schemas.Invest, db: Session = Depends(get_db)):
    user = crud.get_user(db, invest.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    stock = crud.get_stock(db, invest.stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    # if stock price is out of boundaries user should try again with new boundaries
    if stock.price > invest.upper_bound or stock.price < invest.lower_bound:
        raise HTTPException(status_code=400, detail="Stock price is out of boundaries")
    if stock.availability < invest.total:
        raise HTTPException(status_code=400, detail="Requested stocks are not available")
    if user.fund < invest.total * stock.price:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    return crud.user_buy(db=db, user=user, stock=stock, total=invest.total)


@app.put("/sell", response_model=schemas.User)
def sell_stock(invest: schemas.Invest, db: Session = Depends(get_db)):
    user = crud.get_user(db, invest.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    stock = crud.get_stock(db, invest.stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    # if stock price is out of boundaries user should try again with new boundaries
    if stock.price > invest.upper_bound or stock.price < invest.lower_bound:
        raise HTTPException(status_code=400, detail="Stock price is out of boundaries")
    try:
        ownership = next(s for s in user.stocks if s.stock_id == stock.id)
        if ownership.own < invest.total:
            raise HTTPException(status_code=400, detail="User don't own enough stocks")
        return crud.user_sell(db=db, user=user, stock=stock, ownership=ownership, total=invest.total)
    except StopIteration:
        raise HTTPException(status_code=400, detail="User don't own this stock")


@app.get("/stock/{stock_id}", response_model=schemas.StockResponse)
def get_stock(stock_id: int, db: Session = Depends(get_db)):
    stock = crud.get_stock(db, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    stock_with_stats = crud.get_stock_stats(db, stock)
    return stock_with_stats


@app.get("/user/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
