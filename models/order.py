from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from config import Base
from datetime import datetime
import enum


class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationship 
    items = relationship("OrderProduct", back_populates="order", cascade="all, delete")
    receipt = relationship("Receipt", back_populates="order", uselist=False)