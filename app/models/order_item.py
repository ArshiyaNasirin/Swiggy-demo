"""
Food Order API - Order Item Database Model
==========================================
SQLAlchemy ORM model representing individual line items inside a customer order.
"""

from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database.base import Base


class OrderItem(Base):
    """
    OrderItem database model.
    Represents an item within an order, linking an Order to a FoodItem
    with specific quantity and historical unit price locked at order time.
    """
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    food_item_id = Column(Integer, ForeignKey("food_items.id"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="order_items")

    food_item = relationship("FoodItem", back_populates="order_items")

    def __repr__(self) -> str:
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, food_item_id={self.food_item_id}, quantity={self.quantity})>"
