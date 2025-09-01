from typing import Optional,Any ,TypeVar ,Generic
from pydantic import BaseModel
from decouple import config
ModelType = TypeVar("ModelType")
BASE_URL = config("BASE_URL",default="http://localhost:8000")

class SuccessResponse(BaseModel, Generic[ModelType]):
    status: bool = True
    message: str
    data:Optional[ModelType] = None

class ErrorResponse(BaseModel):
    status: str 
    message: str
    error: Optional[Any] = None