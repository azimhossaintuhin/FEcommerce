from  pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    class Config:
        from_attributes = True


class UserReadSchema(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    is_verified: bool

    class Config:
        from_attributes = True
        


class LoginSchema(BaseModel):
    username: str
    password: str
