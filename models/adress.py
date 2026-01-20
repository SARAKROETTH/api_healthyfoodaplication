import enum
import datetime
from sqlalchemy import Column,Integer,String ,Boolean , DateTime,Enum
from sqlalchemy.orm import relationship
from config import Base


class Adress(Base):
    id = Column(Integer,nullable=False,primary_key=True)

    user_id = Column(Integer,nullable=False)
    street = Column(Integer,nullable=False)
    city = Column(String,nullable=True)
    latitude = Column(String,nullable=True)
    Longtidue = Column(String,nullable=False)
