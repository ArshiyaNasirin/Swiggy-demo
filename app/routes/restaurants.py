"""
Food Order API - Restaurants Route Controller
=============================================
RESTful API endpoints for restaurant onboarding, management, search, and nested menu creation.
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.food_item import FoodItem
from app.models.restaurant import Restaurant
from app.schemas.food_item import FoodItemCreate, FoodItemResponse
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantResponse,
    RestaurantUpdate,
)
from app.services import food_service, restaurant_service

router: APIRouter = APIRouter(prefix="/api/v1/restaurants", tags=["Restaurants"])


@router.post(
    "/",
    response_model=RestaurantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new restaurant",
)
def create_restaurant(
    restaurant_data: RestaurantCreate,
    db: Session = Depends(get_db),
) -> Restaurant:
    """
    Register a new restaurant on the platform.
    """
    return restaurant_service.create_restaurant(db=db, restaurant_data=restaurant_data)


@router.get(
    "/",
    response_model=List[RestaurantResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all restaurants",
)
def get_restaurants(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    db: Session = Depends(get_db),
) -> List[Restaurant]:
    """
    Retrieve all restaurants with optional pagination and active-status filter.
    """
    return restaurant_service.get_all_restaurants(
        db=db,
        skip=skip,
        limit=limit,
        active_only=active_only,
    )


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
    status_code=status.HTTP_200_OK,
    summary="Get restaurant by ID",
)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
) -> Restaurant:
    """
    Fetch a single restaurant by its primary key ID.
    """
    return restaurant_service.get_restaurant_by_id(db=db, restaurant_id=restaurant_id)


@router.put(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
    status_code=status.HTTP_200_OK,
    summary="Update restaurant details",
)
def update_restaurant(
    restaurant_id: int,
    restaurant_data: RestaurantUpdate,
    db: Session = Depends(get_db),
) -> Restaurant:
    """
    Update details of an existing restaurant.
    """
    return restaurant_service.update_restaurant(
        db=db,
        restaurant_id=restaurant_id,
        restaurant_data=restaurant_data,
    )


@router.delete(
    "/{restaurant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a restaurant",
)
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a restaurant and cascade-delete all its food items and associated orders.
    """
    restaurant_service.delete_restaurant(db=db, restaurant_id=restaurant_id)
    return None


@router.post(
    "/{restaurant_id}/foods/",
    response_model=FoodItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a food item to a restaurant",
)
def add_food_item_to_restaurant(
    restaurant_id: int,
    food_data: FoodItemCreate,
    db: Session = Depends(get_db),
) -> FoodItem:
    """
    Add a new food item directly under the specified restaurant ID.
    """
    return food_service.create_food_item(
        db=db,
        food_data=food_data,
        restaurant_id=restaurant_id,
    )
