"""
Food Order API - ORM Models Package
===================================
Exports all SQLAlchemy database models so they are registered with Base.metadata.
"""

from app.models.food_item import FoodItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.restaurant import Restaurant
from app.models.user import User

__all__ = [
    "User",
    "Restaurant",
    "FoodItem",
    "Order",
    "OrderItem",
]
