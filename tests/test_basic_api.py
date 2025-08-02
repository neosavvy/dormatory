"""
Basic API tests without conftest.py dependencies.
"""

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dormatory.api.routes import objects, types, links, permissions, versioning, attributes


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


def test_root_endpoint(client):
    """Test that the root endpoint works."""
    response = client.get("/")
    assert response.status_code == 200


def test_health_endpoint(client):
    """Test that the health endpoint works."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_objects_endpoint_exists(client):
    """Test that the objects endpoint exists."""
    response = client.get("/api/v1/objects/")
    # Should return 200 even if no database (stub implementation)
    assert response.status_code == 200


def test_types_endpoint_exists(client):
    """Test that the types endpoint exists."""
    response = client.get("/api/v1/types/")
    # Should return 200 even if no database (stub implementation)
    assert response.status_code == 200 