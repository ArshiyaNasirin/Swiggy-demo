"""
Food Order API - Restaurant Database Model
==========================================
SQLAlchemy ORM model representing partner restaurants and eateries.
"""

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Restaurant(Base):
    """
    Restaurant database model.
    Represents restaurants that provide food menus and receive orders.
    """
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    food_items = relationship("FoodItem", back_populates="restaurant", cascade="all, delete-orphan")

    orders = relationship("Order", back_populates="restaurant", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Restaurant(id={self.id}, name='{self.name}', is_active={self.is_active})>"
