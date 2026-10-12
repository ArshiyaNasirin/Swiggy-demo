"""
Food Order API - Food Item Database Model
=========================================
SQLAlchemy ORM model representing menu food items offered by restaurants.
"""

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class FoodItem(Base):
    """
    FoodItem database model.
    Represents dishes and menu items offered by a restaurant.
    """
    __tablename__ = "food_items"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    restaurant = relationship("Restaurant", back_populates="food_items")

    order_items = relationship("OrderItem", back_populates="food_item")

    def __repr__(self) -> str:
        return f"<FoodItem(id={self.id}, name='{self.name}', price={self.price}, restaurant_id={self.restaurant_id})>"
