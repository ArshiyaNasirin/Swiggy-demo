"""
Food Order API - Database Connection & Session Management
=========================================================
SQLAlchemy engine initialization, session factory creation,
and FastAPI dependency injection function for request lifecycle database sessions.
"""

from typing import Any, Dict, Generator
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config.settings import settings

connect_args: Dict[str, Any] = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine: Engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=settings.DEBUG,
)

SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a scoped database session per HTTP request.
    Automatically rolls back uncommitted errors and closes the session upon response completion.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
