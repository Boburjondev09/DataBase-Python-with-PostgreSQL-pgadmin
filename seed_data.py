from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models


models.Base.metadata.create_all(bind=engine)


db: Session = SessionLocal()


sample_employees = [
    models.Employees(employee_name="Alice", employee_age=25, employee_degree=1, employee_experience=2, department_id=101),
    models.Employees(employee_name="Bob", employee_age=30, employee_degree=2, employee_experience=5, department_id=102),
    models.Employees(employee_name="Charlie", employee_age=28, employee_degree=1, employee_experience=3, department_id=101),
    models.Employees(employee_name="Diana", employee_age=35, employee_degree=3, employee_experience=10, department_id=103),
    models.Employees(employee_name="Eve", employee_age=40, employee_degree=2, employee_experience=15, department_id=104),
    models.Employees(employee_name="Mike", employee_age=32, employee_degree=3, employee_experience=15, department_id=107)
]


if not db.query(models.Employees).first():
    db.add_all(sample_employees)
    db.commit()
    print("Sample employees inserted successfully")
else:
    print("Employees table already has data, skipping seeding")

db.close()
