"""
Food Order API - Food Items Route Controller
============================================
RESTful API endpoints for menu items creation, listing, details, updates, and removal.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.food_item import FoodItem
from app.schemas.food_item import (
    FoodItemCreate,
    FoodItemResponse,
    FoodItemUpdate,
)
from app.services import food_service

router: APIRouter = APIRouter(prefix="/api/v1/foods", tags=["Food Items"])


@router.post(
    "/",
    response_model=FoodItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new food item",
)
def create_food_item(
    food_data: FoodItemCreate,
    db: Session = Depends(get_db),
) -> FoodItem:
    """
    Create a new food item for a restaurant.
    Requires 'restaurant_id' in the request payload.
    """
    return food_service.create_food_item(db=db, food_data=food_data)


@router.get(
    "/",
    response_model=List[FoodItemResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all food items",
)
def get_food_items(
    restaurant_id: Optional[int] = None,
    search: Optional[str] = None,
    available_only: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[FoodItem]:
    """
    Retrieve food items with optional filtering by restaurant_id, search keyword (name/description), and availability.
    """
    return food_service.get_all_food_items(
        db=db,
        restaurant_id=restaurant_id,
        available_only=available_only,
        search=search,
        skip=skip,
        limit=limit,
    )



@router.get(
    "/{food_id}",
    response_model=FoodItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Get food item by ID",
)
def get_food_item(
    food_id: int,
    db: Session = Depends(get_db),
) -> FoodItem:
    """
    Fetch a single food item by its primary key ID.
    """
    return food_service.get_food_item_by_id(db=db, food_id=food_id)


@router.put(
    "/{food_id}",
    response_model=FoodItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Update food item",
)
def update_food_item(
    food_id: int,
    food_data: FoodItemUpdate,
    db: Session = Depends(get_db),
) -> FoodItem:
    """
    Update details (name, price, availability, description) of a food item.
    """
    return food_service.update_food_item(
        db=db,
        food_id=food_id,
        food_data=food_data,
    )


@router.delete(
    "/{food_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete food item",
)
def delete_food_item(
    food_id: int,
    db: Session = Depends(get_db),
) -> None:
    """
    Remove a food item from the database.
    """
    food_service.delete_food_item(db=db, food_id=food_id)
    return None
