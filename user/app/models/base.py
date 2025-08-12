from  app.config.database import BASE
from  sqlalchemy import Column, Integer, String, Boolean ,UUID,ForeignKey, DateTime,func
from sqlalchemy.orm import relationship
import uuid
import datetime
import hashlib
import bcrypt


class BaseModel(BASE):
    __abstract__ = True
    __allow_unmapped__ = True

class User(BaseModel):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String(), unique=True, index=True)
    password = Column(String)
    is_superuser = Column(Boolean(), default=False)
    is_staff = Column(Boolean(), default=False)
    is_verified = Column(Boolean(), default=False)
    token = relationship("Token", back_populates="user")
    created_at = Column(DateTime, default=func.now())
    
    
    def save_password(self,password):
        self.password =  bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return self.password
    
    def checkPassword(self,password):
        if bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8')):
            return True
        return False

class Token(BaseModel):
    __tablename__ = "tokens"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    token = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=False)
    user = relationship("User", back_populates="token", foreign_keys=[user_id])
    
    def set_expire_time(self):
        self.expires_at = datetime.utcnow() + datetime.timedelta(minutes=15)
    
    def verify_token(self,token):
        if  self.token == token and datetime.utcnow() < self.expires_at:
            return True 
        else:
            return False
        
        