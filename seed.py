from app import models, database


def seed():
    db = database.SessionLocal()
    db.query(models.Ownership).delete()
    db.query(models.User).delete()
    user1 = models.User(id=1, fund=20000)
    user2 = models.User(id=2)
    user3 = models.User(id=3)
    db.add(user1)
    db.add(user2)
    db.add(user3)
    db.commit()
    db.close()
