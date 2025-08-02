"""
Unit tests for DORMATORY hierarchical data operations.

These tests validate the business logic for working with hierarchical data structures.
"""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dormatory.models.dormatory_model import (
    Base, Type, Object, Link, Permissions, Versioning, Attributes,
    create_tables
)


class TestHierarchicalOperations:
    """Test hierarchical data operations and business logic."""

    @pytest.fixture
    def engine_and_session(self):
        """Create test database engine and session."""
        engine = create_engine("sqlite:///:memory:", echo=False)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        create_tables(engine)
        session = SessionLocal()
        try:
            yield engine, session
        finally:
            session.close()
            engine.dispose()

    @pytest.fixture
    def sample_hierarchy(self, engine_and_session):
        """Create a sample hierarchical structure for testing."""
        engine, session = engine_and_session
        
        # Create types
        folder_type = Type(type_name="folder")
        file_type = Type(type_name="file")
        document_type = Type(type_name="document")
        session.add_all([folder_type, file_type, document_type])
        session.commit()
        
        # Create objects
        root = Object(
            name="root",
            version=1,
            type_id=folder_type.id,
            created_on="2024-01-01T00:00:00",
            created_by="user1"
        )
        folder1 = Object(
            name="folder1",
            version=1,
            type_id=folder_type.id,
            created_on="2024-01-01T00:00:00",
            created_by="user1"
        )
        folder2 = Object(
            name="folder2",
            version=1,
            type_id=folder_type.id,
            created_on="2024-01-01T00:00:00",
            created_by="user1"
        )
        file1 = Object(
            name="file1.txt",
            version=1,
            type_id=file_type.id,
            created_on="2024-01-01T00:00:00",
            created_by="user1"
        )
        file2 = Object(
            name="file2.txt",
            version=1,
            type_id=file_type.id,
            created_on="2024-01-01T00:00:00",
            created_by="user1"
        )
        doc1 = Object(
            name="document1.pdf",
            version=1,
            type_id=document_type.id,
            created_on="2024-01-01T00:00:00",
            created_by="user1"
        )
        
        session.add_all([root, folder1, folder2, file1, file2, doc1])
        session.commit()
        
        # Create hierarchical links
        # root -> folder1
        link1 = Link(
            parent_id=root.id,
            parent_type="folder",
            child_type="folder",
            r_name="contains",
            child_id=folder1.id
        )
        # root -> folder2
        link2 = Link(
            parent_id=root.id,
            parent_type="folder",
            child_type="folder",
            r_name="contains",
            child_id=folder2.id
        )
        # folder1 -> file1
        link3 = Link(
            parent_id=folder1.id,
            parent_type="folder",
            child_type="file",
            r_name="contains",
            child_id=file1.id
        )
        # folder2 -> file2
        link4 = Link(
            parent_id=folder2.id,
            parent_type="folder",
            child_type="file",
            r_name="contains",
            child_id=file2.id
        )
        # folder2 -> doc1
        link5 = Link(
            parent_id=folder2.id,
            parent_type="folder",
            child_type="document",
            r_name="contains",
            child_id=doc1.id
        )
        
        session.add_all([link1, link2, link3, link4, link5])
        session.commit()
        
        return {
            'session': session,
            'objects': {
                'root': root,
                'folder1': folder1,
                'folder2': folder2,
                'file1': file1,
                'file2': file2,
                'doc1': doc1
            },
            'links': [link1, link2, link3, link4, link5]
        }

    @pytest.mark.unit
    def test_get_children(self, sample_hierarchy):
        """Test getting children of an object."""
        session = sample_hierarchy['session']
        root = sample_hierarchy['objects']['root']
        folder1 = sample_hierarchy['objects']['folder1']
        folder2 = sample_hierarchy['objects']['folder2']
        
        # Get children of root
        children_links = session.query(Link).filter_by(parent_id=root.id).all()
        children_ids = [link.child_id for link in children_links]
        
        assert len(children_ids) == 2
        assert folder1.id in children_ids
        assert folder2.id in children_ids

    @pytest.mark.unit
    def test_get_parents(self, sample_hierarchy):
        """Test getting parents of an object."""
        session = sample_hierarchy['session']
        root = sample_hierarchy['objects']['root']
        folder1 = sample_hierarchy['objects']['folder1']
        file1 = sample_hierarchy['objects']['file1']
        
        # Get parents of folder1
        parent_links = session.query(Link).filter_by(child_id=folder1.id).all()
        parent_ids = [link.parent_id for link in parent_links]
        
        assert len(parent_ids) == 1
        assert root.id in parent_ids
        
        # Get parents of file1
        file_parent_links = session.query(Link).filter_by(child_id=file1.id).all()
        file_parent_ids = [link.parent_id for link in file_parent_links]
        
        assert len(file_parent_ids) == 1
        assert folder1.id in file_parent_ids

    @pytest.mark.unit
    def test_get_hierarchy_depth(self, sample_hierarchy):
        """Test getting hierarchy with depth limit."""
        session = sample_hierarchy['session']
        root = sample_hierarchy['objects']['root']
        folder1 = sample_hierarchy['objects']['folder1']
        folder2 = sample_hierarchy['objects']['folder2']
        file1 = sample_hierarchy['objects']['file1']
        
        def get_hierarchy_at_depth(object_id, depth=1):
            """Get hierarchy at specific depth."""
            if depth == 0:
                return [object_id]
            
            children_links = session.query(Link).filter_by(parent_id=object_id).all()
            result = [object_id]
            for link in children_links:
                result.extend(get_hierarchy_at_depth(link.child_id, depth - 1))
            return result
        
        # Get hierarchy at depth 1 (immediate children)
        depth1_hierarchy = get_hierarchy_at_depth(root.id, 1)
        assert root.id in depth1_hierarchy
        assert folder1.id in depth1_hierarchy
        assert folder2.id in depth1_hierarchy
        assert file1.id not in depth1_hierarchy  # Should not be included at depth 1

    @pytest.mark.unit
    def test_get_complete_hierarchy(self, sample_hierarchy):
        """Test getting complete hierarchy for an object."""
        session = sample_hierarchy['session']
        root = sample_hierarchy['objects']['root']
        
        def get_complete_hierarchy(object_id, visited=None):
            """Get complete hierarchy recursively."""
            if visited is None:
                visited = set()
            
            if object_id in visited:
                return []
            
            visited.add(object_id)
            result = [object_id]
            
            children_links = session.query(Link).filter_by(parent_id=object_id).all()
            for link in children_links:
                result.extend(get_complete_hierarchy(link.child_id, visited))
            
            return result
        
        # Get complete hierarchy from root
        complete_hierarchy = get_complete_hierarchy(root.id)
        
        # Should include all objects
        expected_objects = [
            sample_hierarchy['objects']['root'].id,
            sample_hierarchy['objects']['folder1'].id,
            sample_hierarchy['objects']['folder2'].id,
            sample_hierarchy['objects']['file1'].id,
            sample_hierarchy['objects']['file2'].id,
            sample_hierarchy['objects']['doc1'].id
        ]
        
        for obj_id in expected_objects:
            assert obj_id in complete_hierarchy

    @pytest.mark.unit
    def test_get_objects_by_type(self, sample_hierarchy):
        """Test getting objects by type."""
        session = sample_hierarchy['session']
        folder_type = session.query(Type).filter_by(type_name="folder").first()
        file_type = session.query(Type).filter_by(type_name="file").first()
        document_type = session.query(Type).filter_by(type_name="document").first()
        
        # Get all folders
        folders = session.query(Object).filter_by(type_id=folder_type.id).all()
        assert len(folders) == 3  # root, folder1, folder2
        
        # Get all files
        files = session.query(Object).filter_by(type_id=file_type.id).all()
        assert len(files) == 2  # file1, file2
        
        # Get all documents
        documents = session.query(Object).filter_by(type_id=document_type.id).all()
        assert len(documents) == 1  # doc1

    @pytest.mark.unit
    def test_get_objects_by_relationship(self, sample_hierarchy):
        """Test getting objects by relationship type."""
        session = sample_hierarchy['session']
        root = sample_hierarchy['objects']['root']
        folder2 = sample_hierarchy['objects']['folder2']
        
        # Get all objects with "contains" relationship from root
        contains_links = session.query(Link).filter_by(
            parent_id=root.id, r_name="contains"
        ).all()
        contains_children = [link.child_id for link in contains_links]
        
        assert len(contains_children) == 2
        
        # Get all objects with "contains" relationship from folder2
        folder2_contains = session.query(Link).filter_by(
            parent_id=folder2.id, r_name="contains"
        ).all()
        folder2_children = [link.child_id for link in folder2_contains]
        
        assert len(folder2_children) == 2  # file2 and doc1

    @pytest.mark.unit
    def test_hierarchy_path(self, sample_hierarchy):
        """Test getting path from root to specific object."""
        session = sample_hierarchy['session']
        root = sample_hierarchy['objects']['root']
        folder1 = sample_hierarchy['objects']['folder1']
        file1 = sample_hierarchy['objects']['file1']
        
        def get_path_to_object(target_id, current_id=None, path=None):
            """Get path from root to target object."""
            if current_id is None:
                current_id = root.id
            if path is None:
                path = []
            
            path.append(current_id)
            
            if current_id == target_id:
                return path
            
            children_links = session.query(Link).filter_by(parent_id=current_id).all()
            for link in children_links:
                result = get_path_to_object(target_id, link.child_id, path.copy())
                if result:
                    return result
            
            return None
        
        # Get path to file1
        path_to_file1 = get_path_to_object(file1.id)
        expected_path = [root.id, folder1.id, file1.id]
        assert path_to_file1 == expected_path

    @pytest.mark.unit
    def test_hierarchy_validation(self, sample_hierarchy):
        """Test hierarchy validation (no circular references)."""
        session = sample_hierarchy['session']
        root = sample_hierarchy['objects']['root']
        folder1 = sample_hierarchy['objects']['folder1']
        
        def check_for_circular_references(object_id, visited=None):
            """Check for circular references in hierarchy."""
            if visited is None:
                visited = set()
            
            if object_id in visited:
                return True  # Circular reference found
            
            visited.add(object_id)
            children_links = session.query(Link).filter_by(parent_id=object_id).all()
            
            for link in children_links:
                if check_for_circular_references(link.child_id, visited.copy()):
                    return True
            
            return False
        
        # Check for circular references
        has_circular = check_for_circular_references(root.id)
        assert not has_circular  # Should not have circular references

    @pytest.mark.unit
    def test_hierarchy_statistics(self, sample_hierarchy):
        """Test calculating hierarchy statistics."""
        session = sample_hierarchy['session']
        root = sample_hierarchy['objects']['root']
        
        def get_hierarchy_stats(object_id):
            """Get statistics about hierarchy from given object."""
            def count_objects_recursive(obj_id, visited=None):
                if visited is None:
                    visited = set()
                
                if obj_id in visited:
                    return 0
                
                visited.add(obj_id)
                count = 1
                
                children_links = session.query(Link).filter_by(parent_id=obj_id).all()
                for link in children_links:
                    count += count_objects_recursive(link.child_id, visited)
                
                return count
            
            def get_max_depth(obj_id, current_depth=0, visited=None):
                if visited is None:
                    visited = set()
                
                if obj_id in visited:
                    return current_depth
                
                visited.add(obj_id)
                max_depth = current_depth
                
                children_links = session.query(Link).filter_by(parent_id=obj_id).all()
                for link in children_links:
                    depth = get_max_depth(link.child_id, current_depth + 1, visited.copy())
                    max_depth = max(max_depth, depth)
                
                return max_depth
            
            total_objects = count_objects_recursive(object_id)
            max_depth = get_max_depth(object_id)
            
            return {
                'total_objects': total_objects,
                'max_depth': max_depth
            }
        
        # Get statistics for root hierarchy
        stats = get_hierarchy_stats(root.id)
        
        assert stats['total_objects'] == 6  # root, folder1, folder2, file1, file2, doc1
        assert stats['max_depth'] == 2  # root -> folder -> file

    @pytest.mark.unit
    def test_hierarchy_search(self, sample_hierarchy):
        """Test searching within hierarchy."""
        session = sample_hierarchy['session']
        root = sample_hierarchy['objects']['root']
        
        def search_in_hierarchy(object_id, search_term, visited=None):
            """Search for objects by name within hierarchy."""
            if visited is None:
                visited = set()
            
            if object_id in visited:
                return []
            
            visited.add(object_id)
            results = []
            
            # Check current object
            current_obj = session.query(Object).filter_by(id=object_id).first()
            if search_term.lower() in current_obj.name.lower():
                results.append(current_obj)
            
            # Search children
            children_links = session.query(Link).filter_by(parent_id=object_id).all()
            for link in children_links:
                results.extend(search_in_hierarchy(link.child_id, search_term, visited.copy()))
            
            return results
        
        # Search for files
        files = search_in_hierarchy(root.id, "file")
        assert len(files) == 2  # file1.txt, file2.txt
        
        # Search for folders (note: root is not named "folder", so only folder1 and folder2)
        folders = search_in_hierarchy(root.id, "folder")
        assert len(folders) == 2  # folder1, folder2 (root is not named "folder")
        
        # Search for documents
        documents = search_in_hierarchy(root.id, "document")
        assert len(documents) == 1  # document1.pdf 