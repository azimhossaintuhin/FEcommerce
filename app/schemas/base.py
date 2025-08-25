from typing import Optional,Any ,TypeVar ,Generic
from pydantic import BaseModel
ModelType = TypeVar("ModelType")


class SuccessResponse(BaseModel, Generic[ModelType]):
    status: bool = True
    message: str
    data:Optional[ModelType] = None

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    error: Optional[Any] = None