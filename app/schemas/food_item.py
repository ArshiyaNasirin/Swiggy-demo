"""
Food Order API - Food Item Pydantic Schemas
===========================================
Request validation and response serialization schemas for Food Item entities.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class FoodItemBase(BaseModel):
    """Base fields shared across FoodItem schemas."""
    name: str = Field(..., min_length=1, max_length=150, description="Name of the food item")
    description: Optional[str] = Field(None, max_length=500, description="Description or ingredients")
    price: float = Field(..., gt=0, description="Price in currency units (must be greater than 0)")
    is_available: bool = Field(True, description="Whether the item is available for ordering")


class FoodItemCreate(FoodItemBase):
    """Schema for adding a new food item to a restaurant."""
    restaurant_id: Optional[int] = Field(None, gt=0, description="ID of the restaurant offering this item")


class FoodItemUpdate(BaseModel):
    """Schema for updating an existing food item (all fields optional)."""
    name: Optional[str] = Field(None, min_length=1, max_length=150, description="Updated name")
    description: Optional[str] = Field(None, max_length=500, description="Updated description")
    price: Optional[float] = Field(None, gt=0, description="Updated price")
    is_available: Optional[bool] = Field(None, description="Updated availability")


class FoodItemResponse(FoodItemBase):
    """Schema for returning food item data (response body)."""
    id: int
    restaurant_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
