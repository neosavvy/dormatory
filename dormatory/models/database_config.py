"""
Database configuration for DORMATORY.

This module provides database configuration utilities for different database types
(SQLite and PostgreSQL) and handles database-specific requirements.
"""

import os
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_database_url() -> str:
    """
    Get database URL from environment variable or use default.
    
    Returns:
        Database URL string
    """
    return os.getenv("DATABASE_URL", "sqlite:///dormatory.db")


def create_engine_and_session(database_url: Optional[str] = None):
    """
    Create SQLAlchemy engine and session factory.
    
    Args:
        database_url: Database connection URL. If None, uses environment or default.
        
    Returns:
        Tuple of (engine, SessionLocal)
    """
    if database_url is None:
        database_url = get_database_url()
    
    # Configure engine based on database type
    if database_url.startswith("sqlite"):
        # SQLite configuration
        engine = create_engine(
            database_url,
            echo=True,
            connect_args={"check_same_thread": False}
        )
    elif database_url.startswith("postgresql"):
        # PostgreSQL configuration
        engine = create_engine(
            database_url,
            echo=True,
            pool_pre_ping=True,
            pool_recycle=300
        )
    else:
        # Default configuration
        engine = create_engine(database_url, echo=True)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal


def get_database_info() -> dict:
    """
    Get information about the current database configuration.
    
    Returns:
        Dictionary with database information
    """
    database_url = get_database_url()
    
    if database_url.startswith("sqlite"):
        db_type = "SQLite"
        db_name = database_url.replace("sqlite:///", "").replace("sqlite://", "")
    elif database_url.startswith("postgresql"):
        db_type = "PostgreSQL"
        # Extract database name from PostgreSQL URL
        db_name = database_url.split("/")[-1].split("?")[0]
    else:
        db_type = "Unknown"
        db_name = database_url
    
    return {
        "type": db_type,
        "name": db_name,
        "url": database_url
    }


def is_postgresql() -> bool:
    """
    Check if the current database is PostgreSQL.
    
    Returns:
        True if PostgreSQL, False otherwise
    """
    return get_database_url().startswith("postgresql")


def is_sqlite() -> bool:
    """
    Check if the current database is SQLite.
    
    Returns:
        True if SQLite, False otherwise
    """
    return get_database_url().startswith("sqlite") 