from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import List

DATABASE_URL = "postgresql://postgres:your_password@localhost:5432/fastapitest"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()


class UserItem(Base):
    __tablename__ = "user_items"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True, nullable=False)
    user_surname = Column(String, index=True, nullable=False)
    item_name = Column(String, index=True, nullable=False)
    item_description = Column(Text)


class UserItemCreate(BaseModel):
    user_name: str
    user_surname: str
    item_name: str
    item_description: str

class UserItemResponse(UserItemCreate):
    id: int
    class Config:
        orm_mode = True

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "FASTAPI is running"}

@app.get("/user_items", response_model=List[UserItemResponse])
def get_user_items(db: Session = Depends(get_db)):
    return db.query(UserItem).all()

@app.get("/user_items/{item_id}", response_model=UserItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(UserItem).filter(UserItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/user_items", response_model=UserItemResponse, status_code=201)
def create_item(item: UserItemCreate, db: Session = Depends(get_db)):
    new_item = UserItem(
        user_name=item.user_name,
        user_surname=item.user_surname,
        item_name=item.item_name,
        item_description=item.item_description
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item








# from fastapi import FastAPI, HTTPException, Depends
# from sqlalchemy.orm import Session
# from typing import List
# import crud
# from database import Base, engine, SessionLocal
# from schemas import UserItemCreate, UserItemResponse
#
#
# Base.metadata.create_all(bind=engine)
#
# app = FastAPI()
#
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# @app.get("/user_items", response_model=List[UserItemResponse])
# def get_user_items(db: Session = Depends(get_db)):
#     return crud.get_all_useritems(db)
#
# @app.get("/user_items/{item_id}", response_model=UserItemResponse)
# def get_item(item_id: int, db: Session = Depends(get_db)):
#     item = crud.get_useritem(db, item_id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return item
#
#
#
# @app.post("/user_items", response_model=UserItemResponse, status_code=201)
# def create_item(item: UserItemCreate, db: Session = Depends(get_db)):
#     return crud.create_useritem(db, item)
#
# @app.post("/generate_user_items/")
# def generate_user_items():
#     # your logic here
#     return {"message": "Not implemented yet"}
#
#
# @app.put("/user_items/{item_id}", response_model=UserItemResponse)
# def update_item(item_id: int, updated_item: UserItemCreate, db: Session = Depends(get_db)):
#     db_item = crud.update_useritem(db, item_id, updated_item)
#     if not db_item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return db_item
#
# @app.delete("/user_items/{item_id}", status_code=204)
# def delete_item(item_id: int, db: Session = Depends(get_db)):
#     success = crud.delete_useritem(db, item_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"detail": "Item deleted successfully"}
