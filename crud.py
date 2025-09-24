from sqlalchemy.orm import Session
import models
import schemas


def create_useritem(db: Session, user: schemas.UserItemCreate):
    db_item = models.UserItem(**user.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_all_useritems(db: Session):
    return db.query(models.UserItem).all()

def get_useritem(db: Session, user_id: int):
    return db.query(models.UserItem).filter(models.UserItem.id == user_id).first()

def update_useritem(db: Session, user_id: int, updated_user: schemas.UserItemCreate):
    db_user = get_useritem(db, user_id)
    if not db_user:
        return None
    for key, value in updated_user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_useritem(db: Session, user_id: int):
    db_user = get_useritem(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True
