from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from config import Base

import datetime


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String,nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    img_url = Column(String,nullable=False)
    is_verified = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    role = relationship("Role", back_populates="users")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
