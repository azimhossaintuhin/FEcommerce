from  fastapi.security.oauth2 import OAuth2PasswordBearer
from  datetime import timedelta ,datetime ,timezone
from  app.schemas.jwt_token import TokenDataSchema
from  fastapi import HTTPException, status
from fastapi import Depends
import jwt
import uuid
from typing import Annotated    


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4&*^$4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=15)
REFRESH_TOKEN_EXPIRE_DAYS = timedelta(days=7)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/auth_login")



def create_access_token(data: TokenDataSchema, expires_delta: timedelta  = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.model_dump()
    expire =  datetime.now(timezone.utc) + expires_delta
    to_encode.update({"jti": str(uuid.uuid4())})
    to_encode.update({"type": "access"})
    to_encode.update({"exp": expire.timestamp()})
    encode_jwt =  jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt



def  create_refresh_token(data: TokenDataSchema , expires_delta: timedelta  = REFRESH_TOKEN_EXPIRE_DAYS):
    to_encode = data.model_dump()
    expire =  datetime.now(timezone.utc) + expires_delta
    to_encode.update({"jti": str(uuid.uuid4())})
    to_encode.update({"type": "refresh"})
    to_encode.update({"exp": expire.timestamp()})
    encode_jwt =  jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt    

def create_token_pair(data: TokenDataSchema)-> dict:
    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)
    return {"access_token": access_token, "refresh_token": refresh_token}




async def verify_token(token: Annotated[str, Depends(oauth2_scheme)]): 
    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userid: str = payload.get("userid")
        if userid is None:
           return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
           )
        return {"userid": userid, "username": payload.get("username")}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise  HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
