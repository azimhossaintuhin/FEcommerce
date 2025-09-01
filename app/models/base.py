from  sqlalchemy import Column, Integer, String,Date,func,UUID,Enum
from  app.config.database import BASE
import uuid
import enum


class BaseModel(BASE):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(Date, default=func.now())
    updated_at = Column(Date, default=func.now(), onupdate=func.now())
    
    
class Token_type(enum.Enum):
    EMAIL_VERIFICATION = "email_verification"
    PASSWORD_RESET = "password_reset"
    
    

class Order_payment_Type(enum.Enum):
    ONLINE = "online"
    COD = "cod"
    WALLET = "wallet"
    
class Order_status_Type(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"