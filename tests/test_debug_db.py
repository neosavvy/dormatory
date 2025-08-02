"""
Debug test to isolate database dependency issue.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from dormatory.api.dependencies import get_db
from dormatory.api.routes import types
from dormatory.models.dormatory_model import Base


def test_debug_database_setup():
    """Debug test to understand the database setup issue."""
    # Create test app
    app = FastAPI()
    app.include_router(types.router, prefix="/api/v1/types", tags=["types"])
    
    # Create test database
    engine = create_engine("sqlite:///:memory:", echo=True)  # Enable echo for debugging
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Verify tables exist
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables in database: {tables}")
    
    # Store the engine and session factory in the app state
    app.state.engine = engine
    app.state.TestingSessionLocal = TestingSessionLocal
    
    def override_get_db() -> Generator[Session, None, None]:
        print("Creating test database session")
        # Use the engine from app state
        db = app.state.TestingSessionLocal()
        try:
            print("Yielding test database session")
            yield db
        finally:
            print("Closing test database session")
            db.close()
    
    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client
    client = TestClient(app)
    
    # Test creating a type
    type_data = {"type_name": "test_type"}
    print("Making API request...")
    response = client.post("/api/v1/types/", json=type_data)
    
    print(f"Response status: {response.status_code}")
    if response.status_code != 200:
        print(f"Response content: {response.text}")
    
    # Should succeed
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["type_name"] == "test_type"
    
    # Clean up
    app.dependency_overrides.clear()
    engine.dispose()


def test_verify_dependency_override():
    """Test that dependency override is working."""
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, Session
    from typing import Generator
    
    from dormatory.api.dependencies import get_db
    from dormatory.models.dormatory_model import Base
    
    # Create test app
    app = FastAPI()
    
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
    
    # Verify the override is in place
    assert get_db in app.dependency_overrides
    assert app.dependency_overrides[get_db] == override_get_db
    
    # Clean up
    app.dependency_overrides.clear()
    engine.dispose() 