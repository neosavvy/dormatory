"""
Tests for main API endpoints.

These tests validate the root and health check endpoints.
"""

import pytest
from fastapi.testclient import TestClient


class TestMainAPI:
    """Test suite for main API endpoints."""

    @pytest.mark.api
    def test_root_endpoint(self, client: TestClient):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert "description" in data
        assert data["message"] == "Welcome to DORMATORY API"

    @pytest.mark.api
    def test_health_check_endpoint(self, client: TestClient):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "service" in data
        assert data["status"] == "healthy"
        assert data["service"] == "dormatory-api"

    @pytest.mark.api
    def test_docs_endpoint(self, client: TestClient):
        """Test that the docs endpoint is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200

    @pytest.mark.api
    def test_redoc_endpoint(self, client: TestClient):
        """Test that the redoc endpoint is accessible."""
        response = client.get("/redoc")
        assert response.status_code == 200 