import enum
import datetime
from sqlalchemy import Column,Integer,String ,Boolean , DateTime,Enum

from sqlalchemy.orm import relationship
from config import Base

class Category(Base):
    
    __tablename__ = "categories"

    id = Column(Integer,primary_key=True,unique=True)
    name = Column(String,nullable=False)
    image_url = Column(String,nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )