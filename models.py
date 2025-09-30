from sqlalchemy import Column, Integer, String
from database import Base

class Employees(Base):
    __tablename__ = "employees"
    __table_args__ = {"extend_existing": True}

    employee_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_name = Column(String(100), nullable=False, index=True)
    employee_age = Column(Integer, nullable=False)
    employee_degree = Column(Integer, nullable=False)
    employee_experience = Column(Integer, nullable=True)
    department_id = Column(Integer, nullable=False)
