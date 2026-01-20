from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from config import Base
from datetime import datetime


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    order_products = relationship("OrderProduct", back_populates="product")