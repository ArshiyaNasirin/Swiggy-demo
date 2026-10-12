"""
Food Order API - Order Item Pydantic Schemas
============================================
Request validation and response serialization schemas for Order Line Item entities.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.food_item import FoodItemResponse


class OrderItemBase(BaseModel):
    """Base fields for an item inside an order."""
    food_item_id: int = Field(..., gt=0, description="ID of the food item")
    quantity: int = Field(1, ge=1, description="Quantity ordered (must be at least 1)")


class OrderItemCreate(OrderItemBase):
    """Schema for requesting items when placing an order."""
    pass


class OrderItemResponse(OrderItemBase):
    """Schema for returning order item details with locked unit price."""
    id: int
    order_id: int
    unit_price: float = Field(..., description="Locked purchase price per unit at the time of order")
    food_item: Optional[FoodItemResponse] = Field(None, description="Optional food item details")

    model_config = ConfigDict(from_attributes=True)
