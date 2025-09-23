from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from fastapi import FastAPI

from sqlalchemy.orm import sessionmaker

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

@app.get("/")
def home():
    return {"message": "FASTApi"}

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
