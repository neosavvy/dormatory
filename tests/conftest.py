"""
Pytest configuration and fixtures for DORMATORY tests.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dormatory.api.main import app
from dormatory.models.dormatory_model import Base


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def test_db():
    """Create a test database."""
    # Use in-memory SQLite for testing
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture
def sample_type_data():
    """Sample type data for testing."""
    return {
        "type_name": "test_type"
    }


@pytest.fixture
def sample_object_data():
    """Sample object data for testing."""
    return {
        "name": "test_object",
        "version": 1,
        "type_id": "550e8400-e29b-41d4-a716-446655440000",  # UUID string
        "created_on": "2024-01-01T00:00:00",
        "created_by": "test_user"
    }


@pytest.fixture
def sample_link_data():
    """Sample link data for testing."""
    return {
        "parent_id": 1,
        "parent_type": "folder",
        "child_type": "file",
        "r_name": "contains",
        "child_id": 2
    }


@pytest.fixture
def sample_permission_data():
    """Sample permission data for testing."""
    return {
        "object_id": 1,
        "user": "test_user",
        "permission_level": "read_write"
    }


@pytest.fixture
def sample_versioning_data():
    """Sample versioning data for testing."""
    return {
        "object_id": 1,
        "version": "1.0.0",
        "created_at": "2024-01-01T00:00:00"
    }


@pytest.fixture
def sample_attribute_data():
    """Sample attribute data for testing."""
    return {
        "name": "test_attribute",
        "value": "test_value",
        "object_id": 1,
        "created_on": "2024-01-01T00:00:00",
        "updated_on": "2024-01-01T00:00:00"
    } 