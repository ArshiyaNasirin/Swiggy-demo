"""
Food Order API - User Pydantic Schemas
======================================
Request validation and response serialization schemas for User entities.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    """Base fields shared across User schemas."""
    name: str = Field(..., min_length=1, max_length=100, description="Full name of the user")
    email: str = Field(..., min_length=3, max_length=255, description="Email address")
    phone: Optional[str] = Field(None, max_length=20, description="Contact phone number")
    address: Optional[str] = Field(None, max_length=255, description="Default delivery address")


class UserCreate(UserBase):
    """Schema for creating a new user (request body)."""
    pass


class UserUpdate(BaseModel):
    """Schema for updating an existing user (all fields optional)."""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Updated full name")
    email: Optional[str] = Field(None, min_length=3, max_length=255, description="Updated email address")
    phone: Optional[str] = Field(None, max_length=20, description="Updated phone number")
    address: Optional[str] = Field(None, max_length=255, description="Updated delivery address")


class UserResponse(UserBase):
    """Schema for returning user data (response body)."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
