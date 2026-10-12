"""
Food Order API - Users Route Controller
=======================================
RESTful API endpoints for user registration, listing, retrieval, update, and deletion.
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services import user_service

router: APIRouter = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
) -> User:
    """
    Register a new customer account.
    Validates that the email is not already taken.
    """
    return user_service.create_user(db=db, user_data=user_data)


@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all users",
)
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[User]:
    """
    Retrieve all registered users with optional pagination.
    """
    return user_service.get_all_users(db=db, skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> User:
    """
    Fetch a single user by their primary key ID.
    """
    return user_service.get_user_by_id(db=db, user_id=user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update user details",
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
) -> User:
    """
    Update details of an existing user.
    """
    return user_service.update_user(db=db, user_id=user_id, user_data=user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a user and cascade-delete their orders.
    """
    user_service.delete_user(db=db, user_id=user_id)
    return None
