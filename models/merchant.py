import enum
import datetime
from sqlalchemy import Column,Integer,String ,Boolean , DateTime,Enum
from sqlalchemy.orm import relationship
from config import Base


class Merchant(Base):

    __tablename__ = " merchants"
    id = Column(Integer,nullable=True,primary_key=True)

    owner_id = Column(Integer,nullable=True)
    name = Column(String,nullable=True)
    opening_hours = Column(DateTime)

    duration = Column(DateTime)
