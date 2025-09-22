from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import sessionmaker

import pandas as pd
from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import List
from database import DATABASE_URL

import database
import schematics
import crud
import ml_model


DATABASE_URL = "postgresql://postgres:your_password@localhost:5432/fastapitest"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class ItemCreate(BaseModel):
    name: str

Base.metadata.create_all(bind=engine)

@app.get("/items")
def get_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return items

@app.get("/items/{item_id}")
def get_item(item_id: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    db.close()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items")
def create_item(item: ItemCreate):
    db = SessionLocal()
    new_item = Item(name=item.name)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    db.close()
    return new_item


app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schematics.UserRead)
def create_user_endpoint(user: schematics.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users/", response_model=List[schematics.UserRead])
def get_users_endpoint(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.get("/train")
def train_model_endpoint():
    df = pd.read_sql("SELECT * FROM users", engine)
    model, mse = ml_model.train_model(df)
    return {"message": "Model trained successfully", "mse": mse}

@app.get("/predict/{user_id}")
def predict_name_length(user_id: int):
    df = pd.read_sql("SELECT * FROM users", engine)
    model,_ = ml_model.train_model(df)
    prediction = ml_model.predict(model, pd.DataFrame([[user_id]], columns=['id']))
    return {"predicted_length": int(prediction[0])}

