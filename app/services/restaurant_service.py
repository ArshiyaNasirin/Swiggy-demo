"""
Food Order API - Restaurant Service
===================================
Business logic, database queries, and persistence operations for Partner Restaurants.
"""

from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Query, Session

from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


def get_all_restaurants(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    search: Optional[str] = None,
) -> List[Restaurant]:
    """
    Retrieve all restaurants with optional pagination, active-only filter, and keyword search.
    """
    query: Query[Restaurant] = db.query(Restaurant)
    if active_only:
        query = query.filter(Restaurant.is_active == True)
    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.filter(
            Restaurant.name.ilike(search_pattern) | Restaurant.address.ilike(search_pattern)
        )
    return query.offset(skip).limit(limit).all()



def get_restaurant_by_id(db: Session, restaurant_id: int) -> Restaurant:
    """
    Retrieve a single restaurant by primary key ID or raise 404 Not Found.
    """
    restaurant: Optional[Restaurant] = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Restaurant with ID {restaurant_id} not found",
        )
    return restaurant


def create_restaurant(db: Session, restaurant_data: RestaurantCreate) -> Restaurant:
    """
    Create and persist a new restaurant profile.
    """
    restaurant: Restaurant = Restaurant(
        name=restaurant_data.name,
        address=restaurant_data.address,
        phone=restaurant_data.phone,
        is_active=restaurant_data.is_active,
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


def update_restaurant(
    db: Session,
    restaurant_id: int,
    restaurant_data: RestaurantUpdate,
) -> Restaurant:
    """
    Update details of an existing restaurant.
    Only updates fields that were explicitly provided in the request payload.
    """
    restaurant: Restaurant = get_restaurant_by_id(db, restaurant_id)

    update_dict = restaurant_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(restaurant, field, value)

    db.commit()
    db.refresh(restaurant)
    return restaurant


def delete_restaurant(db: Session, restaurant_id: int) -> None:
    """
    Delete a restaurant by ID.
    Raises 404 Not Found if restaurant does not exist.
    Cascade-deletes menu items and orders attached to this restaurant.
    """
    restaurant: Restaurant = get_restaurant_by_id(db, restaurant_id)
    db.delete(restaurant)
    db.commit()
