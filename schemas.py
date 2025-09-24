from pydantic import BaseModel

class UserItemCreate(BaseModel):
    id : int
    user_name: str
    user_surname: str
    item_name: str
    item_description: str

class UserItemResponse(UserItemCreate):

    class Config:
        orm_mode = True

class UserItemRead(BaseModel):
    id : int
    user_name : str
    user_surname : str
    item_name : str
    item_description : str

    class Config:
        orm_mode = True

# class UserCreate(BaseModel):
#     id : int
#     name : str
#     surname : str
#
# class UserRead(BaseModel):
#     id : int
#     name : str
#     surname : str

