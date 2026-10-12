"""
Food Order API - Order Service
==============================
Core transactional order processing, item price locking, and lifecycle status management.
"""

from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Query, Session

from app.models.food_item import FoodItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.restaurant import Restaurant
from app.models.user import User
from app.schemas.order import OrderCreate, OrderStatus


def create_order(db: Session, order_data: OrderCreate) -> Order:
    """
    Create a new order with multiple line items within a transactional context.

    Enforces business validation rules:
      1. User must exist.
      2. Restaurant must exist and be active.
      3. Food items must exist, belong to this restaurant, and be available.
      4. Calculates total order price from current food item prices.
      5. Locks purchase unit_price in OrderItems table.
    """
    user: Optional[User] = db.query(User).filter(User.id == order_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {order_data.user_id} not found",
        )

    restaurant: Optional[Restaurant] = db.query(Restaurant).filter(Restaurant.id == order_data.restaurant_id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Restaurant with ID {order_data.restaurant_id} not found",
        )
    if not restaurant.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Restaurant '{restaurant.name}' is currently inactive and cannot accept orders",
        )

    total_price: float = 0.0
    items_to_create: List[OrderItem] = []

    for item_input in order_data.items:
        food: Optional[FoodItem] = db.query(FoodItem).filter(FoodItem.id == item_input.food_item_id).first()
        if not food:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Food item with ID {item_input.food_item_id} not found",
            )
        if food.restaurant_id != restaurant.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Food item '{food.name}' (ID {food.id}) does not belong to "
                    f"Restaurant '{restaurant.name}' (ID {restaurant.id})"
                ),
            )
        if not food.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Food item '{food.name}' is currently unavailable for order",
            )

        item_cost: float = food.price * item_input.quantity
        total_price += item_cost

        items_to_create.append(
            OrderItem(
                food_item_id=food.id,
                quantity=item_input.quantity,
                unit_price=food.price,
            )
        )

    new_order: Order = Order(
        user_id=user.id,
        restaurant_id=restaurant.id,
        total_price=round(total_price, 2),
        status=OrderStatus.PENDING.value,
        delivery_address=order_data.delivery_address,
    )
    db.add(new_order)
    db.flush()

    for order_item in items_to_create:
        order_item.order_id = new_order.id
        db.add(order_item)

    db.commit()
    db.refresh(new_order)
    return new_order


def get_all_orders(
    db: Session,
    user_id: Optional[int] = None,
    restaurant_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[Order]:
    """
    Retrieve orders with optional filtering by user, restaurant, and status.
    """
    query: Query[Order] = db.query(Order)
    if user_id is not None:
        query = query.filter(Order.user_id == user_id)
    if restaurant_id is not None:
        query = query.filter(Order.restaurant_id == restaurant_id)
    if status_filter is not None:
        query = query.filter(Order.status == status_filter)

    return query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()


def get_order_by_id(db: Session, order_id: int) -> Order:
    """
    Retrieve an order by primary key ID or raise 404 Not Found.
    """
    order: Optional[Order] = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found",
        )
    return order


def update_order_status(db: Session, order_id: int, new_status: str) -> Order:
    """
    Update the lifecycle status of an existing order.
    Prevents invalid transitions if already delivered or cancelled.
    """
    order: Order = get_order_by_id(db, order_id)

    if order.status == OrderStatus.DELIVERED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update status: Order has already been delivered",
        )
    if order.status == OrderStatus.CANCELLED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update status: Order is already cancelled",
        )

    order.status = new_status
    order.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(order)
    return order


def cancel_order(db: Session, order_id: int) -> Order:
    """
    Cancel an existing order.
    Enforces business rules:
      - Cannot cancel an order that is already delivered.
      - Cannot cancel an order that is already cancelled.
    """
    order: Order = get_order_by_id(db, order_id)

    if order.status == OrderStatus.DELIVERED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel order: Order has already been delivered",
        )
    if order.status == OrderStatus.CANCELLED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order is already cancelled",
        )

    order.status = OrderStatus.CANCELLED.value
    order.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(order)
    return order
