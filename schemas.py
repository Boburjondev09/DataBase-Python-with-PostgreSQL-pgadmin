from pydantic import BaseModel
from typing import Optional, List



class EmployeeBase(BaseModel):
    employee_name: Optional[str] = None
    employee_age: Optional[int] = None
    employee_degree: Optional[int] = None
    employee_experience: Optional[int] = None
    department_id: Optional[int] = None



class EmployeeCreate(EmployeeBase):

    employee_name: str
    employee_age: int
    employee_degree: int
    department_id: int



class EmployeePut(EmployeeBase):
    """
    Full update (PUT) - all fields optional for safety,
    but in practice you usually expect all fields.
    """
    pass


class EmployeePatch(EmployeeBase):
    """
    Partial update (PATCH) - same as PUT, but semantically different.
    """
    pass



class EmployeeResponse(EmployeeBase):
    employee_id: int

    class Config:
        orm_mode = True


class BulkEmployeeRequest(BaseModel):
    employees: List[EmployeeCreate]