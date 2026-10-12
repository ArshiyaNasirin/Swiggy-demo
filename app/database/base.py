"""
Food Order API - Database Base Class
====================================
Declarative base class definition for SQLAlchemy ORM models.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    SQLAlchemy DeclarativeBase.
    All database ORM models inherit from this base class for schema metadata.
    """
    pass
