"""
API tests for objects endpoints.

These tests validate the objects API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from uuid import UUID

from dormatory.models.dormatory_model import Type, Object


class TestObjectsAPI:
    """Test objects API endpoints."""

    @pytest.mark.api
    def test_create_object(self, client: TestClient, sample_object_data: dict):
        """Test creating a new object."""
        # Create a type first using the API
        type_data = {"type_name": "test_type"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        # Update the sample data with the actual type ID
        sample_object_data["type_id"] = type_result["id"]
        
        response = client.post("/api/v1/objects/", json=sample_object_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "name" in data
        assert "type_id" in data
        assert data["name"] == sample_object_data["name"]

    @pytest.mark.api
    def test_get_object_by_id(self, client: TestClient):
        """Test retrieving an object by ID."""
        # Create test data using the API
        type_data = {"type_name": "test_type"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_object",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        
        create_response = client.post("/api/v1/objects/", json=object_data)
        assert create_response.status_code == 200
        created_object = create_response.json()
        object_id = created_object["id"]
        
        response = client.get(f"/api/v1/objects/{object_id}")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "name" in data
        assert "type_id" in data
        assert data["name"] == "test_object"

    @pytest.mark.api
    def test_get_all_objects(self, client: TestClient):
        """Test retrieving all objects."""
        # Create test data using the API
        type_data = {"type_name": "test_type"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_object",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        
        # Create two objects
        client.post("/api/v1/objects/", json=object_data)
        object_data["name"] = "test_object_2"
        client.post("/api/v1/objects/", json=object_data)
        
        response = client.get("/api/v1/objects/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2
        if data:  # If list is not empty
            assert "id" in data[0]
            assert "name" in data[0]
            assert "type_id" in data[0]

    @pytest.mark.api
    def test_get_all_objects_with_filters(self, client: TestClient):
        """Test retrieving objects with filters."""
        # Create test data using the API
        type_data = {"type_name": "test_type"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_filter_object",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        
        client.post("/api/v1/objects/", json=object_data)
        
        response = client.get(f"/api/v1/objects/?name=test_filter&type_id={type_result['id']}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.api
    def test_update_object(self, client: TestClient):
        """Test updating an existing object."""
        # Create test data using the API
        type_data = {"type_name": "test_type"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "original_name",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        
        create_response = client.post("/api/v1/objects/", json=object_data)
        assert create_response.status_code == 200
        created_object = create_response.json()
        object_id = created_object["id"]
        
        update_data = {"name": "updated_object"}
        response = client.put(f"/api/v1/objects/{object_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "name" in data
        assert data["name"] == "updated_object"

    @pytest.mark.api
    def test_delete_object(self, client: TestClient):
        """Test deleting an object."""
        # Create test data using the API
        type_data = {"type_name": "test_type"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "to_delete",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        
        create_response = client.post("/api/v1/objects/", json=object_data)
        assert create_response.status_code == 200
        created_object = create_response.json()
        object_id = created_object["id"]
        
        response = client.delete(f"/api/v1/objects/{object_id}")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    @pytest.mark.api
    def test_create_objects_bulk(self, client: TestClient, sample_object_data: dict):
        """Test creating multiple objects in bulk."""
        # Create a type first using the API
        type_data = {"type_name": "test_type"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        # Update the sample data with the actual type ID
        sample_object_data["type_id"] = type_result["id"]
        
        bulk_data = [sample_object_data, sample_object_data]
        response = client.post("/api/v1/objects/bulk", json=bulk_data)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

    @pytest.mark.api
    def test_get_object_children(self, client: TestClient):
        """Test retrieving children of an object."""
        response = client.get("/api/v1/objects/1/children")
        # Not implemented yet
        assert response.status_code == 500

    @pytest.mark.api
    def test_get_object_parents(self, client: TestClient):
        """Test retrieving parents of an object."""
        response = client.get("/api/v1/objects/1/parents")
        # Not implemented yet
        assert response.status_code == 500

    @pytest.mark.api
    def test_get_object_hierarchy(self, client: TestClient):
        """Test retrieving complete hierarchy for an object."""
        response = client.get("/api/v1/objects/1/hierarchy")
        # Not implemented yet
        assert response.status_code == 500

    @pytest.mark.api
    def test_get_object_hierarchy_with_depth(self, client: TestClient):
        """Test retrieving hierarchy for an object up to specific depth."""
        response = client.get("/api/v1/objects/1/hierarchy/3")
        # Not implemented yet
        assert response.status_code == 500

    @pytest.mark.api
    def test_create_object_invalid_data(self, client: TestClient):
        """Test creating an object with invalid data."""
        invalid_data = {
            "name": "",  # Invalid empty name
            "version": 1,
            "type_id": "550e8400-e29b-41d4-a716-446655440000",
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        response = client.post("/api/v1/objects/", json=invalid_data)
        # Should return validation error
        assert response.status_code == 422

    @pytest.mark.api
    def test_get_nonexistent_object(self, client: TestClient):
        """Test retrieving a non-existent object."""
        response = client.get("/api/v1/objects/999")
        # Should return 404 for not found
        assert response.status_code == 404

    @pytest.mark.api
    def test_update_nonexistent_object(self, client: TestClient):
        """Test updating a non-existent object."""
        update_data = {"name": "updated_object"}
        response = client.put("/api/v1/objects/999", json=update_data)
        # Should return 404 for not found
        assert response.status_code == 404

    @pytest.mark.api
    def test_delete_nonexistent_object(self, client: TestClient):
        """Test deleting a non-existent object."""
        response = client.delete("/api/v1/objects/999")
        # Should return 404 for not found
        assert response.status_code == 404

    @pytest.mark.api
    def test_create_object_with_nonexistent_type(self, client: TestClient, sample_object_data: dict):
        """Test creating an object with a non-existent type."""
        # Use a non-existent type ID
        sample_object_data["type_id"] = "550e8400-e29b-41d4-a716-446655440001"
        
        response = client.post("/api/v1/objects/", json=sample_object_data)
        # Should return 404 for type not found
        assert response.status_code == 404

    @pytest.mark.api
    def test_update_object_with_nonexistent_type(self, client: TestClient):
        """Test updating an object with a non-existent type."""
        # Create test data using the API
        type_data = {"type_name": "test_type"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_object",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        
        create_response = client.post("/api/v1/objects/", json=object_data)
        assert create_response.status_code == 200
        created_object = create_response.json()
        object_id = created_object["id"]
        
        # Try to update with non-existent type
        update_data = {"type_id": "550e8400-e29b-41d4-a716-446655440001"}
        response = client.put(f"/api/v1/objects/{object_id}", json=update_data)
        # Should return 404 for type not found
        assert response.status_code == 404 