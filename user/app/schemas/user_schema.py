from  pydantic import BaseModel, Field,EmailStr
from typing import Optional
import uuid
class UserIn(BaseModel):
    email: EmailStr
    password: str
    is_superuser: Optional[bool] = False
    is_staff: Optional[bool] = False
    is_verified: Optional[bool] = False

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    email: EmailStr
    is_superuser: bool
    is_staff: bool
    is_verified: bool   

    class Config:
        from_attributes = True