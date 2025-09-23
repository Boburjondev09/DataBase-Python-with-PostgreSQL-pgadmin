from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import pandas as pd
import database
import schematics
import crud
import ml_model
from sqlalchemy import create_engine

app = FastAPI()
engine = create_engine("postgresql://postgres:your_password@localhost:5432/fastapitest")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schematics.UserRead)
def create_user_endpoint(user: schematics.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.get("/train")
def train_model_endpoint():
    df = pd.read_sql("SELECT * FROM users", engine)
    model = ml_model.train_model(df)
    return {"message": "Model trained successfully"}

@app.get("/predict/{user_id}")
def predict_name_length(user_id: int):
    df = pd.read_sql("SELECT * FROM users", engine)
    model = ml_model.train_model(df)
    prediction = ml_model.predict(model, pd.DataFrame([[user_id]], columns=['id']))
    return {"predicted_length": int(prediction[0])}
