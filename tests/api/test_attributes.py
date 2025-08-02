"""
API tests for attributes endpoints.

These tests validate the attributes API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from uuid import UUID

from dormatory.models.dormatory_model import Type, Object, Attributes


class TestAttributesAPI:
    """Test attributes API endpoints."""

    @pytest.mark.api
    def test_create_attribute(self, client: TestClient):
        """Test creating a new attribute."""
        # Create type first using the API
        type_data = {"type_name": "file"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        # Create object using the API
        object_data = {
            "name": "test_file",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response = client.post("/api/v1/objects/", json=object_data)
        assert object_response.status_code == 200
        object_result = object_response.json()
        
        # Create attribute
        attribute_data = {
            "name": "color",
            "value": "red",
            "object_id": object_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        
        response = client.post("/api/v1/attributes/", json=attribute_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "name" in data
        assert "value" in data
        assert data["name"] == "color"
        assert data["value"] == "red"
        assert data["object_id"] == object_result["id"]

    @pytest.mark.api
    def test_get_attribute_by_id(self, client: TestClient):
        """Test retrieving an attribute by ID."""
        # Create test data using the API
        type_data = {"type_name": "file"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_file",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response = client.post("/api/v1/objects/", json=object_data)
        assert object_response.status_code == 200
        object_result = object_response.json()
        
        attribute_data = {
            "name": "color",
            "value": "red",
            "object_id": object_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        
        create_response = client.post("/api/v1/attributes/", json=attribute_data)
        assert create_response.status_code == 200
        created_attribute = create_response.json()
        attribute_id = created_attribute["id"]
        
        response = client.get(f"/api/v1/attributes/{attribute_id}")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "name" in data
        assert "value" in data
        assert data["name"] == "color"
        assert data["value"] == "red"

    @pytest.mark.api
    def test_get_all_attributes(self, client: TestClient):
        """Test retrieving all attributes."""
        # Create test data using the API
        type_data = {"type_name": "file"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_file",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response = client.post("/api/v1/objects/", json=object_data)
        assert object_response.status_code == 200
        object_result = object_response.json()
        
        # Create two attributes
        attribute_data_1 = {
            "name": "color",
            "value": "red",
            "object_id": object_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        client.post("/api/v1/attributes/", json=attribute_data_1)
        
        attribute_data_2 = {
            "name": "size",
            "value": "large",
            "object_id": object_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        client.post("/api/v1/attributes/", json=attribute_data_2)
        
        response = client.get("/api/v1/attributes/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2
        if data:  # If list is not empty
            assert "id" in data[0]
            assert "name" in data[0]
            assert "value" in data[0]

    @pytest.mark.api
    def test_get_all_attributes_with_filters(self, client: TestClient):
        """Test retrieving attributes with filters."""
        # Create test data using the API
        type_data = {"type_name": "file"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_file",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response = client.post("/api/v1/objects/", json=object_data)
        assert object_response.status_code == 200
        object_result = object_response.json()
        
        attribute_data = {
            "name": "color",
            "value": "red",
            "object_id": object_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        client.post("/api/v1/attributes/", json=attribute_data)
        
        response = client.get(f"/api/v1/attributes/?object_id={object_result['id']}&name=color")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    @pytest.mark.api
    def test_update_attribute(self, client: TestClient):
        """Test updating an existing attribute."""
        # Create test data using the API
        type_data = {"type_name": "file"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_file",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response = client.post("/api/v1/objects/", json=object_data)
        assert object_response.status_code == 200
        object_result = object_response.json()
        
        attribute_data = {
            "name": "color",
            "value": "red",
            "object_id": object_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        
        create_response = client.post("/api/v1/attributes/", json=attribute_data)
        assert create_response.status_code == 200
        created_attribute = create_response.json()
        attribute_id = created_attribute["id"]
        
        update_data = {"value": "blue"}
        response = client.put(f"/api/v1/attributes/{attribute_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "value" in data
        assert data["value"] == "blue"

    @pytest.mark.api
    def test_delete_attribute(self, client: TestClient):
        """Test deleting an attribute."""
        # Create test data using the API
        type_data = {"type_name": "file"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_file",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response = client.post("/api/v1/objects/", json=object_data)
        assert object_response.status_code == 200
        object_result = object_response.json()
        
        attribute_data = {
            "name": "color",
            "value": "red",
            "object_id": object_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        
        create_response = client.post("/api/v1/attributes/", json=attribute_data)
        assert create_response.status_code == 200
        created_attribute = create_response.json()
        attribute_id = created_attribute["id"]
        
        response = client.delete(f"/api/v1/attributes/{attribute_id}")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    @pytest.mark.api
    def test_create_attributes_bulk(self, client: TestClient):
        """Test creating multiple attributes in bulk."""
        # Create test data using the API
        type_data = {"type_name": "file"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_file",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response = client.post("/api/v1/objects/", json=object_data)
        assert object_response.status_code == 200
        object_result = object_response.json()
        
        attribute_data_1 = {
            "name": "color",
            "value": "red",
            "object_id": object_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        
        attribute_data_2 = {
            "name": "size",
            "value": "large",
            "object_id": object_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        
        bulk_data = [attribute_data_1, attribute_data_2]
        response = client.post("/api/v1/attributes/bulk", json=bulk_data)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

    @pytest.mark.api
    def test_get_attributes_by_object(self, client: TestClient):
        """Test retrieving attributes by object."""
        # Create test data using the API
        type_data = {"type_name": "file"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_file",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response = client.post("/api/v1/objects/", json=object_data)
        assert object_response.status_code == 200
        object_result = object_response.json()
        
        attribute_data = {
            "name": "color",
            "value": "red",
            "object_id": object_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        client.post("/api/v1/attributes/", json=attribute_data)
        
        response = client.get(f"/api/v1/attributes/object/{object_result['id']}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "id" in data[0]
        assert "name" in data[0]
        assert "value" in data[0]

    @pytest.mark.api
    def test_get_attribute_by_name(self, client: TestClient):
        """Test retrieving attributes by name."""
        # Create test data using the API
        type_data = {"type_name": "file"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_file",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response = client.post("/api/v1/objects/", json=object_data)
        assert object_response.status_code == 200
        object_result = object_response.json()
        
        attribute_data = {
            "name": "color",
            "value": "red",
            "object_id": object_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        client.post("/api/v1/attributes/", json=attribute_data)
        
        response = client.get("/api/v1/attributes/name/color")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "name" in data[0]
        assert data[0]["name"] == "color"

    @pytest.mark.api
    def test_get_object_attributes_map(self, client: TestClient):
        """Test retrieving attributes as a key-value map."""
        # Create test data using the API
        type_data = {"type_name": "file"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_file",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response = client.post("/api/v1/objects/", json=object_data)
        assert object_response.status_code == 200
        object_result = object_response.json()
        
        attribute_data_1 = {
            "name": "color",
            "value": "red",
            "object_id": object_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        client.post("/api/v1/attributes/", json=attribute_data_1)
        
        attribute_data_2 = {
            "name": "size",
            "value": "large",
            "object_id": object_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        client.post("/api/v1/attributes/", json=attribute_data_2)
        
        response = client.get(f"/api/v1/attributes/object/{object_result['id']}/map")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "color" in data
        assert "size" in data
        assert data["color"] == "red"
        assert data["size"] == "large"

    @pytest.mark.api
    def test_set_object_attributes(self, client: TestClient):
        """Test setting multiple attributes for an object."""
        # Create test data using the API
        type_data = {"type_name": "file"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_file",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response = client.post("/api/v1/objects/", json=object_data)
        assert object_response.status_code == 200
        object_result = object_response.json()
        
        attributes = {"color": "blue", "size": "medium", "type": "document"}
        response = client.post(f"/api/v1/attributes/object/{object_result['id']}/set", json=attributes)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "3 attributes" in data["message"]

    @pytest.mark.api
    def test_delete_attribute_by_name(self, client: TestClient):
        """Test deleting an attribute by name."""
        # Create test data using the API
        type_data = {"type_name": "file"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_file",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response = client.post("/api/v1/objects/", json=object_data)
        assert object_response.status_code == 200
        object_result = object_response.json()
        
        attribute_data = {
            "name": "color",
            "value": "red",
            "object_id": object_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        client.post("/api/v1/attributes/", json=attribute_data)
        
        response = client.delete(f"/api/v1/attributes/object/{object_result['id']}/name/color")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "deleted" in data["message"]

    @pytest.mark.api
    def test_search_attributes(self, client: TestClient):
        """Test searching attributes by name or value."""
        # Create test data using the API
        type_data = {"type_name": "file"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_file",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response = client.post("/api/v1/objects/", json=object_data)
        assert object_response.status_code == 200
        object_result = object_response.json()
        
        attribute_data = {
            "name": "color",
            "value": "red",
            "object_id": object_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        client.post("/api/v1/attributes/", json=attribute_data)
        
        response = client.get("/api/v1/attributes/search/red")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "value" in data[0]
        assert "red" in data[0]["value"]

    @pytest.mark.api
    def test_create_attribute_invalid_data(self, client: TestClient):
        """Test creating an attribute with invalid data."""
        invalid_data = {"name": "color", "value": "red"}  # Missing required fields
        response = client.post("/api/v1/attributes/", json=invalid_data)
        assert response.status_code == 422  # Validation error

    @pytest.mark.api
    def test_get_nonexistent_attribute(self, client: TestClient):
        """Test retrieving a nonexistent attribute."""
        response = client.get("/api/v1/attributes/999")
        assert response.status_code == 404

    @pytest.mark.api
    def test_update_nonexistent_attribute(self, client: TestClient):
        """Test updating a nonexistent attribute."""
        update_data = {"value": "blue"}
        response = client.put("/api/v1/attributes/999", json=update_data)
        assert response.status_code == 404

    @pytest.mark.api
    def test_delete_nonexistent_attribute(self, client: TestClient):
        """Test deleting a nonexistent attribute."""
        response = client.delete("/api/v1/attributes/999")
        assert response.status_code == 404

    @pytest.mark.api
    def test_create_attribute_with_nonexistent_object(self, client: TestClient):
        """Test creating an attribute with nonexistent object."""
        attribute_data = {
            "name": "color",
            "value": "red",
            "object_id": 999,  # Nonexistent object
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        
        response = client.post("/api/v1/attributes/", json=attribute_data)
        assert response.status_code == 404
        assert "Object not found" in response.json()["detail"]

    @pytest.mark.api
    def test_create_duplicate_attribute(self, client: TestClient):
        """Test creating a duplicate attribute (should fail)."""
        # Create test data using the API
        type_data = {"type_name": "file"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_file",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response = client.post("/api/v1/objects/", json=object_data)
        assert object_response.status_code == 200
        object_result = object_response.json()
        
        attribute_data = {
            "name": "color",
            "value": "red",
            "object_id": object_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        
        # Create first attribute
        response1 = client.post("/api/v1/attributes/", json=attribute_data)
        assert response1.status_code == 200
        
        # Try to create duplicate attribute
        response2 = client.post("/api/v1/attributes/", json=attribute_data)
        assert response2.status_code == 409
        assert "already exists" in response2.json()["detail"]

    @pytest.mark.api
    def test_update_attribute_name_conflict(self, client: TestClient):
        """Test updating an attribute name to conflict with existing attribute."""
        # Create test data using the API
        type_data = {"type_name": "file"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_file",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response = client.post("/api/v1/objects/", json=object_data)
        assert object_response.status_code == 200
        object_result = object_response.json()
        
        # Create two attributes
        attribute_data_1 = {
            "name": "color",
            "value": "red",
            "object_id": object_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        response1 = client.post("/api/v1/attributes/", json=attribute_data_1)
        assert response1.status_code == 200
        attribute1_id = response1.json()["id"]
        
        attribute_data_2 = {
            "name": "size",
            "value": "large",
            "object_id": object_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "updated_on": "2024-01-01T00:00:00"
        }
        response2 = client.post("/api/v1/attributes/", json=attribute_data_2)
        assert response2.status_code == 200
        attribute2_id = response2.json()["id"]
        
        # Try to update second attribute to have same name as first
        update_data = {"name": "color"}
        response3 = client.put(f"/api/v1/attributes/{attribute2_id}", json=update_data)
        assert response3.status_code == 409
        assert "already exists" in response3.json()["detail"] 