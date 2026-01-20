import enum
import datetime
from sqlalchemy import Column,Integer,String ,Boolean , DateTime,Enum

from sqlalchemy.orm import relationship
from config import Base

class Ingradent(Base):

    __tablename__ = "ingardent"
    id = Column(Integer,primary_key=True,nullable=False)

    ingradent_name = Column(String,nullable=True)

