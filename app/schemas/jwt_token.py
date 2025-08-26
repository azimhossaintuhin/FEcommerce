from  pydantic  import  BaseModel
import uuid

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True


class TokenDataSchema(BaseModel):
    userid:str|None = None
    username: str|None = None    

        


