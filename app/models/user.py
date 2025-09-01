from  sqlalchemy import Column, Integer, String,UUID,Boolean , ForeignKey,Enum
from sqlalchemy.orm import relationship
from app.models.base import BaseModel ,Token_type
import uuid
import bcrypt
from datetime import datetime, timedelta,timezone

class User(BaseModel):
    __tablename__ = "users"    
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  
    is_verified = Column(Boolean, default=False)  
    
    profile = relationship("UserProfile", back_populates="user", uselist=False) 
    def __str__(self):
        return self.username
    
    
    def set_password(self, password: str):
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.password = hashed_password.decode('utf-8')
            return self.password
            
        
    def check_password(self, password: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
        except ValueError:
            return False
 
 
class Token(BaseModel):
    __tablename__ = "tokens"
    token_type = Column(Enum(Token_type), nullable=False,default=Token_type.EMAIL_VERIFICATION)  
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id',ondelete='CASCADE'), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    is_useed = Column(Boolean, default=False) 
    is_expired = Column(Boolean, default=False)   
    user = relationship("User", backref="tokens")
    def __str__(self):
        return f"Token(id={self.id}, user_id={self.user_id}, token={self.token})"  
    
    def  genereate_token(self):
        self.token = str(uuid.uuid4())
        return self.token
    
    def is_token_expired(self, expiration_minutes: int = 5)->bool:
        if self.is_expired:
            return True
        expiration_time = self.created_at + timedelta(minutes=expiration_minutes)
        if datetime.now(timezone.utc) > expiration_time:
            self.is_expired = True
            return True
        return False

class UserProfile(BaseModel):
    __tablename__ = "user_profiles"
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id' ,ondelete='CASCADE'), nullable=False, unique=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    bio = Column(String(255), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    user = relationship("User", backref="user_profile", uselist=False)
    def __str__(self):
        return f"UserProfile(id={self.id}, user_id={self.user_id}, first_name={self.first_name}, last_name={self.last_name})" 
    
    
    