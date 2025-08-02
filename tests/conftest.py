"""
Pytest configuration and fixtures for DORMATORY tests.
"""

import pytest
import tempfile
import os
from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from dormatory.api.routes import objects, types, links, permissions, versioning, attributes
from dormatory.api.dependencies import get_db
from dormatory.models.dormatory_model import Base


@pytest.fixture
def test_app():
    """Create a test-specific FastAPI app."""
    app = FastAPI(
        title="DORMATORY API Test",
        description="Test API for DORMATORY",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add root and health endpoints
    @app.get("/")
    async def root():
        """Root endpoint with API information."""
        return {
            "message": "Welcome to DORMATORY API",
            "version": "0.1.0",
            "docs": "/docs",
            "description": "API for hierarchical data storage using flat tables"
        }

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "dormatory-api"}
    
    # Include routers
    app.include_router(objects.router, prefix="/api/v1/objects", tags=["objects"])
    app.include_router(types.router, prefix="/api/v1/types", tags=["types"])
    app.include_router(links.router, prefix="/api/v1/links", tags=["links"])
    app.include_router(permissions.router, prefix="/api/v1/permissions", tags=["permissions"])
    app.include_router(versioning.router, prefix="/api/v1/versioning", tags=["versioning"])
    app.include_router(attributes.router, prefix="/api/v1/attributes", tags=["attributes"])
    
    return app


@pytest.fixture
def client(test_app):
    """Create a test client for the FastAPI application."""
    return TestClient(test_app)


@pytest.fixture
def test_db():
    """Create a test database."""
    # Use file-based SQLite for testing to avoid threading issues
    db_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    db_path = db_file.name
    db_file.close()
    
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
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
        # Clean up the temporary file
        try:
            os.unlink(db_path)
        except:
            pass


@pytest.fixture(autouse=True)
def setup_test_db(test_app):
    """Setup test database for each test."""
    # Use file-based SQLite for testing to avoid threading issues
    db_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    db_path = db_file.name
    db_file.close()
    
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    def override_get_db() -> Generator[Session, None, None]:
        # Create a new session using the same engine
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    # Override the database dependency
    test_app.dependency_overrides[get_db] = override_get_db
    
    yield
    
    # Clean up
    test_app.dependency_overrides.clear()
    engine.dispose()
    # Clean up the temporary file
    try:
        os.unlink(db_path)
    except:
        pass


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