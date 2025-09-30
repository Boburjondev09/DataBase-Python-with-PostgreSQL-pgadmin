from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import scoped_session
from database import SessionLocal, engine
import models, schemas, crud
import ml_model
import pandas as pd
from typing import List

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
db_session = scoped_session(SessionLocal)


@app.on_event("shutdown")
def shutdown_event():
    db_session.remove()




@app.post("/employees/", response_model=schemas.EmployeeResponse)
def create_employee(data: schemas.EmployeeCreate):
    employee = crud.create_employee(db_session, data)
    return employee


@app.get("/employees/", response_model=List[schemas.EmployeeResponse])
def get_employees():
    employees = crud.get_employees(db_session)
    return employees


@app.get("/employees/{employee_id}", response_model=schemas.EmployeeResponse)
def get_employee(employee_id: int):
    employee = crud.get_employee(db_session, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.put("/employees/{employee_id}", response_model=schemas.EmployeeResponse)
def put_employee(employee_id: int, data: schemas.EmployeePut):
    employee = crud.put_employee(db_session, employee_id, data)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.patch("/employees/{employee_id}", response_model=schemas.EmployeeResponse)
def patch_employee(employee_id: int, data: schemas.EmployeePatch):
    employee = crud.patch_employee(db_session, employee_id, data)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    success = crud.delete_employee(db_session, employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"detail": f"Employee {employee_id} deleted successfully"}




@app.post("/train-model/")
def train_model_from_db():
    try:
        model, loss = ml_model.train_from_db()
        return {"detail": "Model trained successfully", "loss": float(loss)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/")
def predict_employee(data: List[schemas.EmployeeCreate]):
    try:
        model, scaler = ml_model.load_trained_model()
        if not model or not scaler:
            raise HTTPException(status_code=400, detail="Model not trained yet. Train first at /train-model/")

        df = pd.DataFrame([emp.dict() for emp in data])
        X, _ = ml_model.prepare_data(df)

        preds = ml_model.predict(model, scaler, X)
        return {"predictions": preds.flatten().tolist()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
