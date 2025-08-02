"""
Database dependencies for FastAPI.

This module provides database session management and dependency injection
for the DORMATORY API.
"""

from typing import Generator
from sqlalchemy.orm import Session

from dormatory.models.dormatory_model import create_engine_and_session

# Create engine and session factory
engine, SessionLocal = create_engine_and_session()


def get_db() -> Generator[Session, None, None]:
    """
    Database dependency for FastAPI.
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 