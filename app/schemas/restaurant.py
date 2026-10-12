"""
Food Order API - Restaurant Pydantic Schemas
============================================
Request validation and response serialization schemas for Restaurant entities.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class RestaurantBase(BaseModel):
    """Base fields shared across Restaurant schemas."""
    name: str = Field(..., min_length=1, max_length=150, description="Restaurant name")
    address: str = Field(..., min_length=1, max_length=255, description="Physical address")
    phone: Optional[str] = Field(None, max_length=20, description="Contact phone number")
    is_active: bool = Field(True, description="Whether the restaurant is currently accepting orders")


class RestaurantCreate(RestaurantBase):
    """Schema for creating a new restaurant (request body)."""
    pass


class RestaurantUpdate(BaseModel):
    """Schema for updating an existing restaurant (all fields optional)."""
    name: Optional[str] = Field(None, min_length=1, max_length=150, description="Updated name")
    address: Optional[str] = Field(None, min_length=1, max_length=255, description="Updated address")
    phone: Optional[str] = Field(None, max_length=20, description="Updated phone number")
    is_active: Optional[bool] = Field(None, description="Updated active status")


class RestaurantResponse(RestaurantBase):
    """Schema for returning restaurant data (response body)."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
