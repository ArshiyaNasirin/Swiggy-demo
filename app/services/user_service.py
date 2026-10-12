"""
Food Order API - User Service
=============================
Business logic, database queries, and persistence operations for Customer Accounts.
"""

from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Retrieve all registered users with pagination.
    """
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Retrieve a single user by primary key ID or raise 404 Not Found.
    """
    user: Optional[User] = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Retrieve a user by unique email address.
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_data: UserCreate) -> User:
    """
    Create and persist a new customer account.
    Validates that the email address is unique before saving.
    """
    existing_user: Optional[User] = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email '{user_data.email}' already exists",
        )

    user: User = User(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        address=user_data.address,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
    """
    Update details of an existing user.
    Only updates fields that were explicitly provided in the request.
    """
    user: User = get_user_by_id(db, user_id)

    if user_data.email and user_data.email != user.email:
        existing_user: Optional[User] = get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email '{user_data.email}' already exists",
            )

    update_dict = user_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> None:
    """
    Delete a user by ID.
    Raises 404 Not Found if user does not exist.
    """
    user: User = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()
