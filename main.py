from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from schemas import BulkEmployeeRequest, EmployeeCreate, EmployeePut, EmployeePatch, EmployeeBase, EmployeeResponse
from typing import List
import pandas as pd

import database
import crud
import schemas
import ml_model



app = FastAPI(title="Employee API")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post("/employees/", response_model=schemas.EmployeeCreate)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = crud.create_employee(db, employee)
    return schemas.EmployeeCreate.from_orm(db_employee)


@app.get("/employees/", response_model=List[schemas.EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    employees = crud.get_employees(db)
    return [schemas.EmployeeResponse.from_orm(emp) for emp in employees]


@app.get("/employees/{employee_id}", response_model=schemas.EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return schemas.EmployeeResponse.from_orm(employee)


@app.put("/employees/{employee_id}", response_model=schemas.EmployeePut)
def put_employee(employee_id: int, employee: schemas.EmployeePut, db: Session = Depends(get_db)):
    db_employee = crud.put_employee(db, employee_id, employee)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return schemas.EmployeePut.from_orm(db_employee)


@app.patch("/employees/{employee_id}", response_model=schemas.EmployeePatch)
def patch_employee(employee_id: int, employee: schemas.EmployeePatch, db: Session = Depends(get_db)):
    db_employee = crud.patch_employee(db, employee_id, employee)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return schemas.EmployeePatch.from_orm(db_employee)


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_employee(db, employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": f"Employee {employee_id} deleted successfully"}




@app.post("/train_model/")
def train_on_employees(db: Session = Depends(get_db)):
    employees = crud.get_employees(db)
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found to train")

    df = pd.DataFrame([{
        "employee_id": emp.employee_id,
        "employee_name": emp.employee_name,
        "employee_age": emp.employee_age,
        "employee_degree": emp.employee_degree,
        "employee_experience": emp.employee_experience,
        "department_id": emp.department_id
    } for emp in employees])

    model, loss = ml_model.train_model(df)
    return {"message": "Model trained successfully", "loss": float(loss)}







@app.post("/predict/bulk")
def predict_bulk_employees(employee: List[EmployeeCreate]):
    model, scaler = ml_model.load_trained_model()
    if not model or not scaler:
        raise HTTPException(status_code=400, detail="Model not trained yet. Train first at /train_model/")

    df = pd.DataFrame([emp.dict() for emp in employee])
    X, _ = ml_model.prepare_data(df)
    predictions = ml_model.predict(model, scaler, X)

    return {
        "predictions": [
            {
                "employee_name": emp.employee_name,
                "employee_age": emp.employee_age,
                "employee_degree": emp.employee_degree,
                "employee_experience": emp.employee_experience,
                "department_id": emp.department_id,
                "predicted_value": float(pred)
            }
            for emp, pred in zip(employee, predictions.flatten())
        ]
    }





# @app.post("/predict/{employee_id}")
# def predict_employee(employee_id: int, db: Session = Depends(get_db)):
#     emp = crud.get_employee(db, employee_id)
#     if not emp:
#         raise HTTPException(status_code=404, detail="Employee not found")
#
#     model, scaler = ml_model.load_trained_model()
#     if not model:
#         raise HTTPException(status_code=500, detail="Model not trained yet")
#
#     df = pd.DataFrame([{
#         "employee_id": emp.employee_id,
#         "employee_name": emp.employee_name,
#         "employee_age": emp.employee_age,
#         "employee_degree": emp.employee_degree,
#         "employee_experience": emp.employee_experience,
#         "department_id": emp.department_id
#     }])
#
#     X, _ = ml_model.prepare_data(df)
#     prediction = ml_model.predict(model, scaler, X)
#
#     return {
#         "employee_id": employee_id,
#         "employee_name": emp.employee_name,
#         "predicted_value": float(prediction[0][0]),
#         "employee_experience" : emp.employee_experience,
#         "department_id" : emp.department_id
#     }



