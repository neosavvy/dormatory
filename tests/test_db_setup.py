"""
Test database setup.
"""

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from dormatory.models.dormatory_model import Base, Type, Object


def test_database_setup():
    """Test that database setup works correctly."""
    # Create a new in-memory database
    engine = create_engine("sqlite:///:memory:", echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    session = SessionLocal()
    
    try:
        # Test creating a type
        type_obj = Type(type_name="test_type")
        session.add(type_obj)
        session.commit()
        session.refresh(type_obj)
        
        # Test creating an object
        obj = Object(
            name="test_object",
            version=1,
            type_id=type_obj.id,
            created_on="2024-01-01T00:00:00",
            created_by="test_user"
        )
        session.add(obj)
        session.commit()
        session.refresh(obj)
        
        # Verify the objects were created
        assert type_obj.id is not None
        assert obj.id is not None
        assert obj.name == "test_object"
        assert obj.type_id == type_obj.id
        
    finally:
        session.close()
        engine.dispose()


def test_database_tables_exist():
    """Test that all tables exist in the database."""
    # Create a new in-memory database
    engine = create_engine("sqlite:///:memory:", echo=False)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Check that tables exist
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    expected_tables = ['type', 'object', 'link', 'permissions', 'versioning', 'attributes']
    
    for table in expected_tables:
        assert table in tables, f"Table {table} not found in database"
    
    engine.dispose() 