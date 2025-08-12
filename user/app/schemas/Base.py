from pydantic import BaseModel
from typing import Union, Optional, Any, Dict, List

class SuccessResponse(BaseModel):
    
    status: str = "success"
    message: str
    data: Union[Dict[str, Any], List[Any]]

    
    def model_validate(self, data: Dict[str, Any]) -> 'SuccessResponse':
        if not data.get("data"):
            data.pop("data", None)
        return SuccessResponse(**data)
    
    d

class ErrorResponse(BaseModel):
    status: str = "false"
    message: str
    errors: Optional[Union[Dict[str, Any], str]] = None
