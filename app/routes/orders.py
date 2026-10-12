"""
Food Order API - Orders Route Controller
========================================
RESTful API endpoints for order placement, tracking, lifecycle status updates, and cancellation.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.order import Order
from app.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate,
)
from app.services import order_service

router: APIRouter = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new order",
)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
) -> Order:
    """
    Place a new food order with items.
    Validates user, restaurant, and food item availability,
    and calculates the total price automatically.
    """
    return order_service.create_order(db=db, order_data=order_data)


@router.get(
    "/",
    response_model=List[OrderResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all orders",
)
def get_orders(
    user_id: Optional[int] = None,
    restaurant_id: Optional[int] = None,
    order_status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[Order]:
    """
    Retrieve orders with optional filtering by user, restaurant, or status.
    """
    return order_service.get_all_orders(
        db=db,
        user_id=user_id,
        restaurant_id=restaurant_id,
        status_filter=order_status,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Get order by ID",
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
) -> Order:
    """
    Fetch complete details of a specific order, including ordered items.
    """
    return order_service.get_order_by_id(db=db, order_id=order_id)


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Update order status",
)
def update_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
) -> Order:
    """
    Advance or update the lifecycle status of an order.
    """
    return order_service.update_order_status(
        db=db,
        order_id=order_id,
        new_status=status_data.status.value,
    )


@router.patch(
    "/{order_id}/cancel",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Cancel an order",
)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
) -> Order:
    """
    Cancel an order if it has not yet been delivered.
    """
    return order_service.cancel_order(db=db, order_id=order_id)
