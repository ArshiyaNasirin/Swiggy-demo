"""
Food Order API - Order Pydantic Schemas
=======================================
Request validation and response serialization schemas for Order entities and lifecycle status Enums.
"""

from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.order_item import OrderItemCreate, OrderItemResponse


class OrderStatus(str, Enum):
    """Allowed states for an order lifecycle."""
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    PREPARING = "Preparing"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class OrderCreate(BaseModel):
    """Schema for placing a new order (request body)."""
    user_id: int = Field(..., gt=0, description="ID of the user placing the order")
    restaurant_id: int = Field(..., gt=0, description="ID of the restaurant being ordered from")
    delivery_address: str = Field(..., min_length=1, max_length=255, description="Destination delivery address")
    items: List[OrderItemCreate] = Field(..., min_length=1, description="List of food items and quantities")


class OrderStatusUpdate(BaseModel):
    """Schema for updating the status of an existing order."""
    status: OrderStatus = Field(..., description="New order status")


class OrderResponse(BaseModel):
    """Schema for returning order details including items (response body)."""
    id: int
    user_id: int
    restaurant_id: int
    total_price: float = Field(..., description="Total price of the order")
    status: str = Field(..., description="Current status of the order")
    delivery_address: str = Field(..., description="Delivery address")
    created_at: datetime
    updated_at: datetime
    order_items: List[OrderItemResponse] = Field(default_factory=list, description="Ordered items")

    model_config = ConfigDict(from_attributes=True)
