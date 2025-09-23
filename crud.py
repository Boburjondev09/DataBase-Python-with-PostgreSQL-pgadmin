from sqlalchemy.orm import session
import database
import schematics

def create_user(db: session, user: schematics.UserCreate):
    db_user = database.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: session):
    return db.query(database.User).all()