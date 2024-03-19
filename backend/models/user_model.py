from pydantic import BaseModel

class Users(BaseModel):
    name: str
    last_name: str
    personal_id: int
    phone: str 
    address: str 
    email: str
    user_password: str 

class Role(BaseModel): 
    name: str
    description: str

class LoginModel(BaseModel):
    email: str
    user_password: str


