"""
Food Order API - Food Item Service
==================================
Business logic, database queries, and persistence operations for Restaurant Menu Items.
"""

from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Query, Session

from app.models.food_item import FoodItem
from app.models.restaurant import Restaurant
from app.schemas.food_item import FoodItemCreate, FoodItemUpdate


def get_all_food_items(
    db: Session,
    restaurant_id: Optional[int] = None,
    available_only: bool = False,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[FoodItem]:
    """
    Retrieve food items with optional filtering by restaurant, keyword search (name/description), and availability.
    """
    query: Query[FoodItem] = db.query(FoodItem)
    if restaurant_id is not None:
        query = query.filter(FoodItem.restaurant_id == restaurant_id)
    if available_only:
        query = query.filter(FoodItem.is_available == True)
    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.filter(
            FoodItem.name.ilike(search_pattern) | FoodItem.description.ilike(search_pattern)
        )
    return query.offset(skip).limit(limit).all()



def get_food_item_by_id(db: Session, food_id: int) -> FoodItem:
    """
    Retrieve a single food item by primary key ID or raise 404 Not Found.
    """
    food_item: Optional[FoodItem] = db.query(FoodItem).filter(FoodItem.id == food_id).first()
    if not food_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food item with ID {food_id} not found",
        )
    return food_item


def create_food_item(
    db: Session,
    food_data: FoodItemCreate,
    restaurant_id: Optional[int] = None,
) -> FoodItem:
    """
    Add a new food item.
    Verifies that the target restaurant exists before creating the menu item.
    """
    target_restaurant_id: Optional[int] = restaurant_id if restaurant_id is not None else food_data.restaurant_id
    if not target_restaurant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="restaurant_id is required to create a food item",
        )

    restaurant: Optional[Restaurant] = db.query(Restaurant).filter(Restaurant.id == target_restaurant_id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot add food item: Restaurant with ID {target_restaurant_id} not found",
        )

    food_item: FoodItem = FoodItem(
        restaurant_id=target_restaurant_id,
        name=food_data.name,
        description=food_data.description,
        price=food_data.price,
        is_available=food_data.is_available,
    )
    db.add(food_item)
    db.commit()
    db.refresh(food_item)
    return food_item


def update_food_item(
    db: Session,
    food_id: int,
    food_data: FoodItemUpdate,
) -> FoodItem:
    """
    Update details of an existing food item.
    Only updates fields that were explicitly provided in the request payload.
    """
    food_item: FoodItem = get_food_item_by_id(db, food_id)

    update_dict = food_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(food_item, field, value)

    db.commit()
    db.refresh(food_item)
    return food_item


def delete_food_item(db: Session, food_id: int) -> None:
    """
    Delete a food item by ID.
    Raises 404 Not Found if food item does not exist.
    """
    food_item: FoodItem = get_food_item_by_id(db, food_id)
    db.delete(food_item)
    db.commit()
