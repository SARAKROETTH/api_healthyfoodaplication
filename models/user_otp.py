import enum
import datetime
from sqlalchemy import Column,Integer,String ,Boolean , DateTime,Enum,ForeignKey

from sqlalchemy.orm import relationship
from config import Base


class OTP(Base):
    __tablename__ = "otp_store"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String,nullable=False)
    otp_code = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)