"""
Food Order API - Routes Package
===============================
Exports all APIRouters for Users, Restaurants, Food Items, and Orders.
"""

from app.routes.foods import router as foods_router
from app.routes.orders import router as orders_router
from app.routes.restaurants import router as restaurants_router
from app.routes.users import router as users_router

__all__ = [
    "users_router",
    "restaurants_router",
    "foods_router",
    "orders_router",
]
