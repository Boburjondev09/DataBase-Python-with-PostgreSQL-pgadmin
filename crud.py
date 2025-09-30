from sqlalchemy.orm import Session
import models
import schemas


def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employees(**employee.dict(exclude_unset=True))
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee



def get_employees(db: Session):
    return db.query(models.Employees).all()



def get_employee(db: Session, employee_id: int):
    return db.query(models.Employees).filter(models.Employees.employee_id == employee_id).first()



def put_employee(db: Session, employee_id: int, updated_employee: schemas.EmployeePut):
    db_employee = db.query(models.Employees).filter(models.Employees.employee_id == employee_id).first()
    if not db_employee:
        return None
    for key, value in updated_employee.dict().items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee






def patch_employee(db: Session, employee_id: int, patch_data: schemas.EmployeePatch):
    db_employee = db.query(models.Employees).filter(models.Employees.employee_id == employee_id).first()
    if not db_employee:
        return None
    for key, value in patch_data.dict(exclude_unset=True).items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee






def delete_employee(db: Session, employee_id: int):
    db_employee = db.query(models.Employees).filter(models.Employees.employee_id == employee_id).first()
    if not db_employee:
        return False
    db.delete(db_employee)
    db.commit()
    return True



