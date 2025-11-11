from pydantic import BaseModel

class UserRegister(BaseModel):
    email: str
    name: str

class UserLogin(BaseModel):
    email: str