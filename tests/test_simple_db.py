"""
Simple test to verify database setup.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from dormatory.models.dormatory_model import Base, Type, Object


def test_database_dependency_override():
    """Test that database dependency override works correctly."""
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, Session
    from typing import Generator
    
    from dormatory.api.dependencies import get_db
    from dormatory.api.routes import types
    from dormatory.models.dormatory_model import Base
    
    # Create test app
    app = FastAPI()
    app.include_router(types.router, prefix="/api/v1/types", tags=["types"])
    
    # Create test database
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client
    client = TestClient(app)
    
    # Test creating a type
    type_data = {"type_name": "test_type"}
    response = client.post("/api/v1/types/", json=type_data)
    
    # Should succeed
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["type_name"] == "test_type"
    
    # Clean up
    app.dependency_overrides.clear()
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