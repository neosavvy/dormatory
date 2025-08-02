"""
API tests for types endpoints.

These tests validate the types API endpoints.
"""

import pytest
from fastapi.testclient import TestClient


class TestTypesAPI:
    """Test types API endpoints."""

    @pytest.mark.api
    def test_create_type(self, client: TestClient, sample_type_data: dict):
        """Test creating a new type."""
        response = client.post("/api/v1/types/", json=sample_type_data)
        # Now implemented with stub response
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "type_name" in data

    @pytest.mark.api
    def test_get_type_by_id(self, client: TestClient):
        """Test retrieving a type by ID."""
        # First create a type
        type_data = {"type_name": "test_type_for_get"}
        create_response = client.post("/api/v1/types/", json=type_data)
        assert create_response.status_code == 200
        created_type = create_response.json()
        type_id = created_type["id"]
        
        # Now get the type by ID
        response = client.get(f"/api/v1/types/{type_id}")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "type_name" in data
        assert data["id"] == type_id

    @pytest.mark.api
    def test_get_all_types(self, client: TestClient):
        """Test retrieving all types."""
        response = client.get("/api/v1/types/")
        # Now implemented with stub response
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if data:  # If list is not empty
            assert "id" in data[0]
            assert "type_name" in data[0]

    @pytest.mark.api
    def test_get_all_types_with_filters(self, client: TestClient):
        """Test retrieving types with filters."""
        response = client.get("/api/v1/types/?type_name=test")
        # Now implemented with stub response
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.api
    def test_update_type(self, client: TestClient):
        """Test updating an existing type."""
        # First create a type
        type_data = {"type_name": "test_type_for_update"}
        create_response = client.post("/api/v1/types/", json=type_data)
        assert create_response.status_code == 200
        created_type = create_response.json()
        type_id = created_type["id"]
        
        # Now update the type
        update_data = {"type_name": "updated_type"}
        response = client.put(f"/api/v1/types/{type_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "type_name" in data
        assert data["type_name"] == "updated_type"

    @pytest.mark.api
    def test_delete_type(self, client: TestClient):
        """Test deleting a type."""
        # First create a type
        type_data = {"type_name": "test_type_for_delete"}
        create_response = client.post("/api/v1/types/", json=type_data)
        assert create_response.status_code == 200
        created_type = create_response.json()
        type_id = created_type["id"]
        
        # Now delete the type
        response = client.delete(f"/api/v1/types/{type_id}")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    @pytest.mark.api
    def test_create_types_bulk(self, client: TestClient, sample_type_data: dict):
        """Test creating multiple types in bulk."""
        bulk_data = [sample_type_data, sample_type_data]
        response = client.post("/api/v1/types/bulk", json=bulk_data)
        # Now implemented with stub response
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

    @pytest.mark.api
    def test_get_objects_by_type(self, client: TestClient):
        """Test retrieving objects by type."""
        # First create a type
        type_data = {"type_name": "test_type_for_objects"}
        create_response = client.post("/api/v1/types/", json=type_data)
        assert create_response.status_code == 200
        created_type = create_response.json()
        type_id = created_type["id"]
        
        # Test getting objects by type (should return empty list since no objects exist)
        response = client.get(f"/api/v1/types/{type_id}/objects")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Should be empty since no objects of this type exist yet
        assert len(data) == 0
        
        # Test getting objects by non-existent type
        response = client.get("/api/v1/types/00000000-0000-0000-0000-000000000000/objects")
        assert response.status_code == 404

    @pytest.mark.api
    def test_create_type_invalid_data(self, client: TestClient):
        """Test creating type with invalid data."""
        invalid_data = {}  # Missing required fields
        response = client.post("/api/v1/types/", json=invalid_data)
        # Should fail due to validation
        assert response.status_code == 422

    @pytest.mark.api
    def test_get_nonexistent_type(self, client: TestClient):
        """Test retrieving a non-existent type."""
        response = client.get("/api/v1/types/00000000-0000-0000-0000-000000000000")
        # Should return 404 for not found
        assert response.status_code == 404

    @pytest.mark.api
    def test_update_nonexistent_type(self, client: TestClient):
        """Test updating a non-existent type."""
        update_data = {"type_name": "updated_type"}
        response = client.put("/api/v1/types/00000000-0000-0000-0000-000000000000", json=update_data)
        # Should return 404 for not found
        assert response.status_code == 404

    @pytest.mark.api
    def test_delete_nonexistent_type(self, client: TestClient):
        """Test deleting a non-existent type."""
        response = client.delete("/api/v1/types/00000000-0000-0000-0000-000000000000")
        # Should return 404 for not found
        assert response.status_code == 404 