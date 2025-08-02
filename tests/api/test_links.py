"""
API tests for links endpoints.

These tests validate the links API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from uuid import UUID

from dormatory.models.dormatory_model import Type, Object, Link


class TestLinksAPI:
    """Test links API endpoints."""

    @pytest.mark.api
    def test_create_link(self, client: TestClient):
        """Test creating a new link."""
        # Create types first using the API
        type_data_1 = {"type_name": "folder"}
        type_response_1 = client.post("/api/v1/types/", json=type_data_1)
        assert type_response_1.status_code == 200
        type_result_1 = type_response_1.json()
        
        type_data_2 = {"type_name": "file"}
        type_response_2 = client.post("/api/v1/types/", json=type_data_2)
        assert type_response_2.status_code == 200
        type_result_2 = type_response_2.json()
        
        # Create objects using the API
        object_data_1 = {
            "name": "parent_folder",
            "version": 1,
            "type_id": type_result_1["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_1 = client.post("/api/v1/objects/", json=object_data_1)
        assert object_response_1.status_code == 200
        object_result_1 = object_response_1.json()
        
        object_data_2 = {
            "name": "child_file",
            "version": 1,
            "type_id": type_result_2["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_2 = client.post("/api/v1/objects/", json=object_data_2)
        assert object_response_2.status_code == 200
        object_result_2 = object_response_2.json()
        
        # Create link
        link_data = {
            "parent_id": object_result_1["id"],
            "parent_type": "folder",
            "child_type": "file",
            "r_name": "contains",
            "child_id": object_result_2["id"]
        }
        
        response = client.post("/api/v1/links/", json=link_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "parent_id" in data
        assert "child_id" in data
        assert data["parent_id"] == object_result_1["id"]
        assert data["child_id"] == object_result_2["id"]
        assert data["r_name"] == "contains"

    @pytest.mark.api
    def test_get_link_by_id(self, client: TestClient):
        """Test retrieving a link by ID."""
        # Create test data using the API
        type_data_1 = {"type_name": "folder"}
        type_response_1 = client.post("/api/v1/types/", json=type_data_1)
        assert type_response_1.status_code == 200
        type_result_1 = type_response_1.json()
        
        type_data_2 = {"type_name": "file"}
        type_response_2 = client.post("/api/v1/types/", json=type_data_2)
        assert type_response_2.status_code == 200
        type_result_2 = type_response_2.json()
        
        object_data_1 = {
            "name": "parent_folder",
            "version": 1,
            "type_id": type_result_1["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_1 = client.post("/api/v1/objects/", json=object_data_1)
        assert object_response_1.status_code == 200
        object_result_1 = object_response_1.json()
        
        object_data_2 = {
            "name": "child_file",
            "version": 1,
            "type_id": type_result_2["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_2 = client.post("/api/v1/objects/", json=object_data_2)
        assert object_response_2.status_code == 200
        object_result_2 = object_response_2.json()
        
        link_data = {
            "parent_id": object_result_1["id"],
            "parent_type": "folder",
            "child_type": "file",
            "r_name": "contains",
            "child_id": object_result_2["id"]
        }
        
        create_response = client.post("/api/v1/links/", json=link_data)
        assert create_response.status_code == 200
        created_link = create_response.json()
        link_id = created_link["id"]
        
        response = client.get(f"/api/v1/links/{link_id}")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "parent_id" in data
        assert "child_id" in data
        assert data["parent_id"] == object_result_1["id"]
        assert data["child_id"] == object_result_2["id"]

    @pytest.mark.api
    def test_get_all_links(self, client: TestClient):
        """Test retrieving all links."""
        # Create test data using the API
        type_data_1 = {"type_name": "folder"}
        type_response_1 = client.post("/api/v1/types/", json=type_data_1)
        assert type_response_1.status_code == 200
        type_result_1 = type_response_1.json()
        
        type_data_2 = {"type_name": "file"}
        type_response_2 = client.post("/api/v1/types/", json=type_data_2)
        assert type_response_2.status_code == 200
        type_result_2 = type_response_2.json()
        
        object_data_1 = {
            "name": "parent_folder",
            "version": 1,
            "type_id": type_result_1["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_1 = client.post("/api/v1/objects/", json=object_data_1)
        assert object_response_1.status_code == 200
        object_result_1 = object_response_1.json()
        
        object_data_2 = {
            "name": "child_file",
            "version": 1,
            "type_id": type_result_2["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_2 = client.post("/api/v1/objects/", json=object_data_2)
        assert object_response_2.status_code == 200
        object_result_2 = object_response_2.json()
        
        # Create two links
        link_data_1 = {
            "parent_id": object_result_1["id"],
            "parent_type": "folder",
            "child_type": "file",
            "r_name": "contains",
            "child_id": object_result_2["id"]
        }
        client.post("/api/v1/links/", json=link_data_1)
        
        link_data_2 = {
            "parent_id": object_result_1["id"],
            "parent_type": "folder",
            "child_type": "file",
            "r_name": "references",
            "child_id": object_result_2["id"]
        }
        client.post("/api/v1/links/", json=link_data_2)
        
        response = client.get("/api/v1/links/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2
        if data:  # If list is not empty
            assert "id" in data[0]
            assert "parent_id" in data[0]
            assert "child_id" in data[0]

    @pytest.mark.api
    def test_get_all_links_with_filters(self, client: TestClient):
        """Test retrieving links with filters."""
        # Create test data using the API
        type_data_1 = {"type_name": "folder"}
        type_response_1 = client.post("/api/v1/types/", json=type_data_1)
        assert type_response_1.status_code == 200
        type_result_1 = type_response_1.json()
        
        type_data_2 = {"type_name": "file"}
        type_response_2 = client.post("/api/v1/types/", json=type_data_2)
        assert type_response_2.status_code == 200
        type_result_2 = type_response_2.json()
        
        object_data_1 = {
            "name": "parent_folder",
            "version": 1,
            "type_id": type_result_1["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_1 = client.post("/api/v1/objects/", json=object_data_1)
        assert object_response_1.status_code == 200
        object_result_1 = object_response_1.json()
        
        object_data_2 = {
            "name": "child_file",
            "version": 1,
            "type_id": type_result_2["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_2 = client.post("/api/v1/objects/", json=object_data_2)
        assert object_response_2.status_code == 200
        object_result_2 = object_response_2.json()
        
        link_data = {
            "parent_id": object_result_1["id"],
            "parent_type": "folder",
            "child_type": "file",
            "r_name": "contains",
            "child_id": object_result_2["id"]
        }
        client.post("/api/v1/links/", json=link_data)
        
        response = client.get(f"/api/v1/links/?parent_id={object_result_1['id']}&child_id={object_result_2['id']}&r_name=contains")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    @pytest.mark.api
    def test_update_link(self, client: TestClient):
        """Test updating an existing link."""
        # Create test data using the API
        type_data_1 = {"type_name": "folder"}
        type_response_1 = client.post("/api/v1/types/", json=type_data_1)
        assert type_response_1.status_code == 200
        type_result_1 = type_response_1.json()
        
        type_data_2 = {"type_name": "file"}
        type_response_2 = client.post("/api/v1/types/", json=type_data_2)
        assert type_response_2.status_code == 200
        type_result_2 = type_response_2.json()
        
        object_data_1 = {
            "name": "parent_folder",
            "version": 1,
            "type_id": type_result_1["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_1 = client.post("/api/v1/objects/", json=object_data_1)
        assert object_response_1.status_code == 200
        object_result_1 = object_response_1.json()
        
        object_data_2 = {
            "name": "child_file",
            "version": 1,
            "type_id": type_result_2["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_2 = client.post("/api/v1/objects/", json=object_data_2)
        assert object_response_2.status_code == 200
        object_result_2 = object_response_2.json()
        
        link_data = {
            "parent_id": object_result_1["id"],
            "parent_type": "folder",
            "child_type": "file",
            "r_name": "contains",
            "child_id": object_result_2["id"]
        }
        
        create_response = client.post("/api/v1/links/", json=link_data)
        assert create_response.status_code == 200
        created_link = create_response.json()
        link_id = created_link["id"]
        
        update_data = {"r_name": "updated_relationship"}
        response = client.put(f"/api/v1/links/{link_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "r_name" in data
        assert data["r_name"] == "updated_relationship"

    @pytest.mark.api
    def test_delete_link(self, client: TestClient):
        """Test deleting a link."""
        # Create test data using the API
        type_data_1 = {"type_name": "folder"}
        type_response_1 = client.post("/api/v1/types/", json=type_data_1)
        assert type_response_1.status_code == 200
        type_result_1 = type_response_1.json()
        
        type_data_2 = {"type_name": "file"}
        type_response_2 = client.post("/api/v1/types/", json=type_data_2)
        assert type_response_2.status_code == 200
        type_result_2 = type_response_2.json()
        
        object_data_1 = {
            "name": "parent_folder",
            "version": 1,
            "type_id": type_result_1["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_1 = client.post("/api/v1/objects/", json=object_data_1)
        assert object_response_1.status_code == 200
        object_result_1 = object_response_1.json()
        
        object_data_2 = {
            "name": "child_file",
            "version": 1,
            "type_id": type_result_2["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_2 = client.post("/api/v1/objects/", json=object_data_2)
        assert object_response_2.status_code == 200
        object_result_2 = object_response_2.json()
        
        link_data = {
            "parent_id": object_result_1["id"],
            "parent_type": "folder",
            "child_type": "file",
            "r_name": "contains",
            "child_id": object_result_2["id"]
        }
        
        create_response = client.post("/api/v1/links/", json=link_data)
        assert create_response.status_code == 200
        created_link = create_response.json()
        link_id = created_link["id"]
        
        response = client.delete(f"/api/v1/links/{link_id}")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    @pytest.mark.api
    def test_create_links_bulk(self, client: TestClient):
        """Test creating multiple links in bulk."""
        # Create test data using the API
        type_data_1 = {"type_name": "folder"}
        type_response_1 = client.post("/api/v1/types/", json=type_data_1)
        assert type_response_1.status_code == 200
        type_result_1 = type_response_1.json()
        
        type_data_2 = {"type_name": "file"}
        type_response_2 = client.post("/api/v1/types/", json=type_data_2)
        assert type_response_2.status_code == 200
        type_result_2 = type_response_2.json()
        
        object_data_1 = {
            "name": "parent_folder",
            "version": 1,
            "type_id": type_result_1["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_1 = client.post("/api/v1/objects/", json=object_data_1)
        assert object_response_1.status_code == 200
        object_result_1 = object_response_1.json()
        
        object_data_2 = {
            "name": "child_file",
            "version": 1,
            "type_id": type_result_2["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_2 = client.post("/api/v1/objects/", json=object_data_2)
        assert object_response_2.status_code == 200
        object_result_2 = object_response_2.json()
        
        link_data_1 = {
            "parent_id": object_result_1["id"],
            "parent_type": "folder",
            "child_type": "file",
            "r_name": "contains",
            "child_id": object_result_2["id"]
        }
        
        link_data_2 = {
            "parent_id": object_result_1["id"],
            "parent_type": "folder",
            "child_type": "file",
            "r_name": "references",
            "child_id": object_result_2["id"]
        }
        
        bulk_data = [link_data_1, link_data_2]
        response = client.post("/api/v1/links/bulk", json=bulk_data)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

    @pytest.mark.api
    def test_get_children_by_parent(self, client: TestClient):
        """Test retrieving children by parent."""
        # Create test data using the API
        type_data_1 = {"type_name": "folder"}
        type_response_1 = client.post("/api/v1/types/", json=type_data_1)
        assert type_response_1.status_code == 200
        type_result_1 = type_response_1.json()
        
        type_data_2 = {"type_name": "file"}
        type_response_2 = client.post("/api/v1/types/", json=type_data_2)
        assert type_response_2.status_code == 200
        type_result_2 = type_response_2.json()
        
        object_data_1 = {
            "name": "parent_folder",
            "version": 1,
            "type_id": type_result_1["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_1 = client.post("/api/v1/objects/", json=object_data_1)
        assert object_response_1.status_code == 200
        object_result_1 = object_response_1.json()
        
        object_data_2 = {
            "name": "child_file",
            "version": 1,
            "type_id": type_result_2["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_2 = client.post("/api/v1/objects/", json=object_data_2)
        assert object_response_2.status_code == 200
        object_result_2 = object_response_2.json()
        
        link_data = {
            "parent_id": object_result_1["id"],
            "parent_type": "folder",
            "child_type": "file",
            "r_name": "contains",
            "child_id": object_result_2["id"]
        }
        client.post("/api/v1/links/", json=link_data)
        
        response = client.get(f"/api/v1/links/parent/{object_result_1['id']}/children")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "id" in data[0]
        assert "name" in data[0]
        assert "relationship" in data[0]

    @pytest.mark.api
    def test_get_parents_by_child(self, client: TestClient):
        """Test retrieving parents by child."""
        # Create test data using the API
        type_data_1 = {"type_name": "folder"}
        type_response_1 = client.post("/api/v1/types/", json=type_data_1)
        assert type_response_1.status_code == 200
        type_result_1 = type_response_1.json()
        
        type_data_2 = {"type_name": "file"}
        type_response_2 = client.post("/api/v1/types/", json=type_data_2)
        assert type_response_2.status_code == 200
        type_result_2 = type_response_2.json()
        
        object_data_1 = {
            "name": "parent_folder",
            "version": 1,
            "type_id": type_result_1["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_1 = client.post("/api/v1/objects/", json=object_data_1)
        assert object_response_1.status_code == 200
        object_result_1 = object_response_1.json()
        
        object_data_2 = {
            "name": "child_file",
            "version": 1,
            "type_id": type_result_2["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_2 = client.post("/api/v1/objects/", json=object_data_2)
        assert object_response_2.status_code == 200
        object_result_2 = object_response_2.json()
        
        link_data = {
            "parent_id": object_result_1["id"],
            "parent_type": "folder",
            "child_type": "file",
            "r_name": "contains",
            "child_id": object_result_2["id"]
        }
        client.post("/api/v1/links/", json=link_data)
        
        response = client.get(f"/api/v1/links/child/{object_result_2['id']}/parents")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "id" in data[0]
        assert "name" in data[0]
        assert "relationship" in data[0]

    @pytest.mark.api
    def test_get_links_by_relationship(self, client: TestClient):
        """Test retrieving links by relationship name."""
        # Create test data using the API
        type_data_1 = {"type_name": "folder"}
        type_response_1 = client.post("/api/v1/types/", json=type_data_1)
        assert type_response_1.status_code == 200
        type_result_1 = type_response_1.json()
        
        type_data_2 = {"type_name": "file"}
        type_response_2 = client.post("/api/v1/types/", json=type_data_2)
        assert type_response_2.status_code == 200
        type_result_2 = type_response_2.json()
        
        object_data_1 = {
            "name": "parent_folder",
            "version": 1,
            "type_id": type_result_1["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_1 = client.post("/api/v1/objects/", json=object_data_1)
        assert object_response_1.status_code == 200
        object_result_1 = object_response_1.json()
        
        object_data_2 = {
            "name": "child_file",
            "version": 1,
            "type_id": type_result_2["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_2 = client.post("/api/v1/objects/", json=object_data_2)
        assert object_response_2.status_code == 200
        object_result_2 = object_response_2.json()
        
        link_data = {
            "parent_id": object_result_1["id"],
            "parent_type": "folder",
            "child_type": "file",
            "r_name": "contains",
            "child_id": object_result_2["id"]
        }
        client.post("/api/v1/links/", json=link_data)
        
        response = client.get("/api/v1/links/relationship/contains")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "r_name" in data[0]
        assert data[0]["r_name"] == "contains"

    @pytest.mark.api
    def test_create_hierarchy(self, client: TestClient):
        """Test creating a complete hierarchy structure."""
        response = client.post("/api/v1/links/hierarchy", json={})
        # Not implemented yet
        assert response.status_code == 500

    @pytest.mark.api
    def test_create_link_invalid_data(self, client: TestClient):
        """Test creating a link with invalid data."""
        invalid_data = {"parent_id": 999, "child_id": 999, "r_name": "test"}
        response = client.post("/api/v1/links/", json=invalid_data)
        assert response.status_code == 422  # Validation error

    @pytest.mark.api
    def test_get_nonexistent_link(self, client: TestClient):
        """Test retrieving a nonexistent link."""
        response = client.get("/api/v1/links/999")
        assert response.status_code == 404

    @pytest.mark.api
    def test_update_nonexistent_link(self, client: TestClient):
        """Test updating a nonexistent link."""
        update_data = {"r_name": "updated_relationship"}
        response = client.put("/api/v1/links/999", json=update_data)
        assert response.status_code == 404

    @pytest.mark.api
    def test_delete_nonexistent_link(self, client: TestClient):
        """Test deleting a nonexistent link."""
        response = client.delete("/api/v1/links/999")
        assert response.status_code == 404

    @pytest.mark.api
    def test_create_link_with_nonexistent_parent(self, client: TestClient):
        """Test creating a link with nonexistent parent object."""
        # Create test data using the API
        type_data = {"type_name": "file"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "child_file",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response = client.post("/api/v1/objects/", json=object_data)
        assert object_response.status_code == 200
        object_result = object_response.json()
        
        link_data = {
            "parent_id": 999,  # Nonexistent parent
            "parent_type": "folder",
            "child_type": "file",
            "r_name": "contains",
            "child_id": object_result["id"]
        }
        
        response = client.post("/api/v1/links/", json=link_data)
        assert response.status_code == 404
        assert "Parent object not found" in response.json()["detail"]

    @pytest.mark.api
    def test_create_link_with_nonexistent_child(self, client: TestClient):
        """Test creating a link with nonexistent child object."""
        # Create test data using the API
        type_data = {"type_name": "folder"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "parent_folder",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response = client.post("/api/v1/objects/", json=object_data)
        assert object_response.status_code == 200
        object_result = object_response.json()
        
        link_data = {
            "parent_id": object_result["id"],
            "parent_type": "folder",
            "child_type": "file",
            "r_name": "contains",
            "child_id": 999  # Nonexistent child
        }
        
        response = client.post("/api/v1/links/", json=link_data)
        assert response.status_code == 404
        assert "Child object not found" in response.json()["detail"]

    @pytest.mark.api
    def test_create_self_referencing_link(self, client: TestClient):
        """Test creating a self-referencing link (should fail)."""
        # Create test data using the API
        type_data = {"type_name": "folder"}
        type_response = client.post("/api/v1/types/", json=type_data)
        assert type_response.status_code == 200
        type_result = type_response.json()
        
        object_data = {
            "name": "test_folder",
            "version": 1,
            "type_id": type_result["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response = client.post("/api/v1/objects/", json=object_data)
        assert object_response.status_code == 200
        object_result = object_response.json()
        
        link_data = {
            "parent_id": object_result["id"],
            "parent_type": "folder",
            "child_type": "folder",
            "r_name": "contains",
            "child_id": object_result["id"]  # Same as parent
        }
        
        response = client.post("/api/v1/links/", json=link_data)
        assert response.status_code == 422
        assert "self-referencing" in response.json()["detail"]

    @pytest.mark.api
    def test_create_duplicate_link(self, client: TestClient):
        """Test creating a duplicate link (should fail)."""
        # Create test data using the API
        type_data_1 = {"type_name": "folder"}
        type_response_1 = client.post("/api/v1/types/", json=type_data_1)
        assert type_response_1.status_code == 200
        type_result_1 = type_response_1.json()
        
        type_data_2 = {"type_name": "file"}
        type_response_2 = client.post("/api/v1/types/", json=type_data_2)
        assert type_response_2.status_code == 200
        type_result_2 = type_response_2.json()
        
        object_data_1 = {
            "name": "parent_folder",
            "version": 1,
            "type_id": type_result_1["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_1 = client.post("/api/v1/objects/", json=object_data_1)
        assert object_response_1.status_code == 200
        object_result_1 = object_response_1.json()
        
        object_data_2 = {
            "name": "child_file",
            "version": 1,
            "type_id": type_result_2["id"],
            "created_on": "2024-01-01T00:00:00",
            "created_by": "test_user"
        }
        object_response_2 = client.post("/api/v1/objects/", json=object_data_2)
        assert object_response_2.status_code == 200
        object_result_2 = object_response_2.json()
        
        link_data = {
            "parent_id": object_result_1["id"],
            "parent_type": "folder",
            "child_type": "file",
            "r_name": "contains",
            "child_id": object_result_2["id"]
        }
        
        # Create first link
        response1 = client.post("/api/v1/links/", json=link_data)
        assert response1.status_code == 200
        
        # Try to create duplicate link
        response2 = client.post("/api/v1/links/", json=link_data)
        assert response2.status_code == 409
        assert "already exists" in response2.json()["detail"] 