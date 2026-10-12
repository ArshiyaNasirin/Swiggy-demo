"""
Food Order API - Order Database Model
=====================================
SQLAlchemy ORM model representing food delivery orders placed by customers.
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Order(Base):
    """
    Order database model.
    Represents an order placed by a customer to a specific restaurant.
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    total_price = Column(Float, default=0.0)
    status = Column(String, default="Pending")
    delivery_address = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="orders")

    restaurant = relationship("Restaurant", back_populates="orders")

    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Order(id={self.id}, user_id={self.user_id}, status='{self.status}', total={self.total_price})>"
