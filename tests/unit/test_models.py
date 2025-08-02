"""
Unit tests for DORMATORY SQLAlchemy models.

These tests validate the model definitions, relationships, and basic operations.
"""

import pytest
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dormatory.models.dormatory_model import (
    Base, Type, Object, Link, Permissions, Versioning, Attributes,
    create_engine_and_session, create_tables, get_db_session
)


class TestModelCreation:
    """Test model creation and basic properties."""

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

    @pytest.mark.unit
    def test_type_creation(self, engine_and_session):
        """Test creating a Type model."""
        engine, session = engine_and_session
        
        # Create a type
        type_obj = Type(type_name="test_type")
        session.add(type_obj)
        session.commit()
        
        # Verify the type was created
        assert type_obj.id is not None
        assert isinstance(type_obj.id, UUID)  # UUID object, not string
        assert type_obj.type_name == "test_type"
        
        # Verify we can retrieve it
        retrieved_type = session.query(Type).filter_by(type_name="test_type").first()
        assert retrieved_type is not None
        assert retrieved_type.id == type_obj.id

    @pytest.mark.unit
    def test_object_creation(self, engine_and_session):
        """Test creating an Object model."""
        engine, session = engine_and_session
        
        # Create a type first
        type_obj = Type(type_name="test_type")
        session.add(type_obj)
        session.commit()
        
        # Create an object
        object_obj = Object(
            name="test_object",
            version=1,
            type_id=type_obj.id,
            created_on="2024-01-01T00:00:00",
            created_by="test_user"
        )
        session.add(object_obj)
        session.commit()
        
        # Verify the object was created
        assert object_obj.id is not None
        assert object_obj.name == "test_object"
        assert object_obj.version == 1
        assert object_obj.type_id == type_obj.id
        assert object_obj.created_by == "test_user"

    @pytest.mark.unit
    def test_object_default_version(self, engine_and_session):
        """Test that Object version defaults to 1."""
        engine, session = engine_and_session
        
        # Create a type first
        type_obj = Type(type_name="test_type")
        session.add(type_obj)
        session.commit()
        
        # Create an object without specifying version
        object_obj = Object(
            name="test_object",
            type_id=type_obj.id,
            created_on="2024-01-01T00:00:00",
            created_by="test_user"
        )
        session.add(object_obj)
        session.commit()
        
        # Verify default version is 1
        assert object_obj.version == 1

    @pytest.mark.unit
    def test_link_creation(self, engine_and_session):
        """Test creating a Link model."""
        engine, session = engine_and_session
        
        # Create parent and child objects
        type_obj = Type(type_name="folder")
        session.add(type_obj)
        session.commit()
        
        parent_obj = Object(
            name="parent_folder",
            version=1,
            type_id=type_obj.id,
            created_on="2024-01-01T00:00:00",
            created_by="test_user"
        )
        child_obj = Object(
            name="child_file",
            version=1,
            type_id=type_obj.id,
            created_on="2024-01-01T00:00:00",
            created_by="test_user"
        )
        session.add_all([parent_obj, child_obj])
        session.commit()
        
        # Create a link
        link = Link(
            parent_id=parent_obj.id,
            parent_type="folder",
            child_type="file",
            r_name="contains",
            child_id=child_obj.id
        )
        session.add(link)
        session.commit()
        
        # Verify the link was created
        assert link.id is not None
        assert link.parent_id == parent_obj.id
        assert link.child_id == child_obj.id
        assert link.r_name == "contains"

    @pytest.mark.unit
    def test_permissions_creation(self, engine_and_session):
        """Test creating a Permissions model."""
        engine, session = engine_and_session
        
        # Create an object first
        type_obj = Type(type_name="document")
        session.add(type_obj)
        session.commit()
        
        object_obj = Object(
            name="test_document",
            version=1,
            type_id=type_obj.id,
            created_on="2024-01-01T00:00:00",
            created_by="test_user"
        )
        session.add(object_obj)
        session.commit()
        
        # Create a permission
        permission = Permissions(
            object_id=object_obj.id,
            user="test_user",
            permission_level="read_write"
        )
        session.add(permission)
        session.commit()
        
        # Verify the permission was created
        assert permission.id is not None
        assert permission.object_id == object_obj.id
        assert permission.user == "test_user"
        assert permission.permission_level == "read_write"

    @pytest.mark.unit
    def test_versioning_creation(self, engine_and_session):
        """Test creating a Versioning model."""
        engine, session = engine_and_session
        
        # Create an object first
        type_obj = Type(type_name="document")
        session.add(type_obj)
        session.commit()
        
        object_obj = Object(
            name="test_document",
            version=1,
            type_id=type_obj.id,
            created_on="2024-01-01T00:00:00",
            created_by="test_user"
        )
        session.add(object_obj)
        session.commit()
        
        # Create a versioning record
        versioning = Versioning(
            object_id=object_obj.id,
            version="1.0.0",
            created_at=datetime.now()
        )
        session.add(versioning)
        session.commit()
        
        # Verify the versioning was created
        assert versioning.id is not None
        assert versioning.object_id == object_obj.id
        assert versioning.version == "1.0.0"
        assert versioning.created_at is not None

    @pytest.mark.unit
    def test_versioning_default_created_at(self, engine_and_session):
        """Test that Versioning created_at defaults to current time."""
        engine, session = engine_and_session
        
        # Create an object first
        type_obj = Type(type_name="document")
        session.add(type_obj)
        session.commit()
        
        object_obj = Object(
            name="test_document",
            version=1,
            type_id=type_obj.id,
            created_on="2024-01-01T00:00:00",
            created_by="test_user"
        )
        session.add(object_obj)
        session.commit()
        
        # Create a versioning record without specifying created_at
        versioning = Versioning(
            object_id=object_obj.id,
            version="1.0.0"
        )
        session.add(versioning)
        session.commit()
        
        # Verify created_at was set automatically
        assert versioning.created_at is not None
        assert isinstance(versioning.created_at, datetime)

    @pytest.mark.unit
    def test_attributes_creation(self, engine_and_session):
        """Test creating an Attributes model."""
        engine, session = engine_and_session
        
        # Create an object first
        type_obj = Type(type_name="document")
        session.add(type_obj)
        session.commit()
        
        object_obj = Object(
            name="test_document",
            version=1,
            type_id=type_obj.id,
            created_on="2024-01-01T00:00:00",
            created_by="test_user"
        )
        session.add(object_obj)
        session.commit()
        
        # Create an attribute
        attribute = Attributes(
            name="color",
            value="red",
            object_id=object_obj.id,
            created_on="2024-01-01T00:00:00",
            updated_on="2024-01-01T00:00:00"
        )
        session.add(attribute)
        session.commit()
        
        # Verify the attribute was created
        assert attribute.id is not None
        assert attribute.name == "color"
        assert attribute.value == "red"
        assert attribute.object_id == object_obj.id


class TestModelRepr:
    """Test __repr__ methods for all models."""

    @pytest.mark.unit
    def test_type_repr(self):
        """Test Type __repr__ method."""
        type_obj = Type(type_name="test_type")
        type_obj.id = UUID('12345678-1234-5678-1234-567812345678')
        
        repr_str = repr(type_obj)
        assert "Type" in repr_str
        assert "test_type" in repr_str
        assert "12345678-1234-5678-1234-567812345678" in repr_str

    @pytest.mark.unit
    def test_object_repr(self):
        """Test Object __repr__ method."""
        object_obj = Object(
            name="test_object",
            version=1,
            type_id=UUID('12345678-1234-5678-1234-567812345678'),
            created_on="2024-01-01T00:00:00",
            created_by="test_user"
        )
        object_obj.id = 1
        
        repr_str = repr(object_obj)
        assert "Object" in repr_str
        assert "test_object" in repr_str
        assert "1" in repr_str

    @pytest.mark.unit
    def test_link_repr(self):
        """Test Link __repr__ method."""
        link = Link(
            parent_id=1,
            parent_type="folder",
            child_type="file",
            r_name="contains",
            child_id=2
        )
        link.id = 1
        
        repr_str = repr(link)
        assert "Link" in repr_str
        assert "contains" in repr_str
        assert "1" in repr_str
        assert "2" in repr_str

    @pytest.mark.unit
    def test_permissions_repr(self):
        """Test Permissions __repr__ method."""
        permission = Permissions(
            object_id=1,
            user="test_user",
            permission_level="read"
        )
        permission.id = 1
        
        repr_str = repr(permission)
        assert "Permissions" in repr_str
        assert "test_user" in repr_str
        assert "read" in repr_str

    @pytest.mark.unit
    def test_versioning_repr(self):
        """Test Versioning __repr__ method."""
        versioning = Versioning(
            object_id=1,
            version="1.0.0",
            created_at=datetime.now()
        )
        versioning.id = 1
        
        repr_str = repr(versioning)
        assert "Versioning" in repr_str
        assert "1.0.0" in repr_str

    @pytest.mark.unit
    def test_attributes_repr(self):
        """Test Attributes __repr__ method."""
        attribute = Attributes(
            name="color",
            value="red",
            object_id=1,
            created_on="2024-01-01T00:00:00",
            updated_on="2024-01-01T00:00:00"
        )
        attribute.id = 1
        
        repr_str = repr(attribute)
        assert "Attributes" in repr_str
        assert "color" in repr_str
        assert "red" in repr_str


class TestModelRelationships:
    """Test model relationships and foreign key constraints."""

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

    @pytest.mark.unit
    def test_object_type_relationship(self, engine_and_session):
        """Test the relationship between Object and Type."""
        engine, session = engine_and_session
        
        # Create a type
        type_obj = Type(type_name="document")
        session.add(type_obj)
        session.commit()
        
        # Create objects of this type
        object1 = Object(
            name="doc1",
            version=1,
            type_id=type_obj.id,
            created_on="2024-01-01T00:00:00",
            created_by="user1"
        )
        object2 = Object(
            name="doc2",
            version=1,
            type_id=type_obj.id,
            created_on="2024-01-01T00:00:00",
            created_by="user2"
        )
        session.add_all([object1, object2])
        session.commit()
        
        # Verify objects are linked to the type
        assert object1.type_id == type_obj.id
        assert object2.type_id == type_obj.id
        
        # Query objects by type
        objects_of_type = session.query(Object).filter_by(type_id=type_obj.id).all()
        assert len(objects_of_type) == 2
        assert object1 in objects_of_type
        assert object2 in objects_of_type

    @pytest.mark.unit
    def test_link_parent_child_relationship(self, engine_and_session):
        """Test the parent-child relationship through Links."""
        engine, session = engine_and_session
        
        # Create a type
        type_obj = Type(type_name="item")
        session.add(type_obj)
        session.commit()
        
        # Create parent and child objects
        parent = Object(
            name="parent",
            version=1,
            type_id=type_obj.id,
            created_on="2024-01-01T00:00:00",
            created_by="user1"
        )
        child1 = Object(
            name="child1",
            version=1,
            type_id=type_obj.id,
            created_on="2024-01-01T00:00:00",
            created_by="user1"
        )
        child2 = Object(
            name="child2",
            version=1,
            type_id=type_obj.id,
            created_on="2024-01-01T00:00:00",
            created_by="user1"
        )
        session.add_all([parent, child1, child2])
        session.commit()
        
        # Create links
        link1 = Link(
            parent_id=parent.id,
            parent_type="folder",
            child_type="file",
            r_name="contains",
            child_id=child1.id
        )
        link2 = Link(
            parent_id=parent.id,
            parent_type="folder",
            child_type="file",
            r_name="contains",
            child_id=child2.id
        )
        session.add_all([link1, link2])
        session.commit()
        
        # Query children of parent
        children_links = session.query(Link).filter_by(parent_id=parent.id).all()
        assert len(children_links) == 2
        
        # Query parents of child
        parent_links = session.query(Link).filter_by(child_id=child1.id).all()
        assert len(parent_links) == 1
        assert parent_links[0].parent_id == parent.id

    @pytest.mark.unit
    def test_permissions_object_relationship(self, engine_and_session):
        """Test the relationship between Permissions and Object."""
        engine, session = engine_and_session
        
        # Create an object
        type_obj = Type(type_name="document")
        session.add(type_obj)
        session.commit()
        
        object_obj = Object(
            name="test_document",
            version=1,
            type_id=type_obj.id,
            created_on="2024-01-01T00:00:00",
            created_by="owner"
        )
        session.add(object_obj)
        session.commit()
        
        # Create permissions for this object
        perm1 = Permissions(
            object_id=object_obj.id,
            user="user1",
            permission_level="read"
        )
        perm2 = Permissions(
            object_id=object_obj.id,
            user="user2",
            permission_level="write"
        )
        session.add_all([perm1, perm2])
        session.commit()
        
        # Query permissions for the object
        object_permissions = session.query(Permissions).filter_by(object_id=object_obj.id).all()
        assert len(object_permissions) == 2
        
        # Query permissions for a specific user
        user_permissions = session.query(Permissions).filter_by(user="user1").all()
        assert len(user_permissions) == 1
        assert user_permissions[0].permission_level == "read"

    @pytest.mark.unit
    def test_versioning_object_relationship(self, engine_and_session):
        """Test the relationship between Versioning and Object."""
        engine, session = engine_and_session
        
        # Create an object
        type_obj = Type(type_name="document")
        session.add(type_obj)
        session.commit()
        
        object_obj = Object(
            name="test_document",
            version=1,
            type_id=type_obj.id,
            created_on="2024-01-01T00:00:00",
            created_by="user1"
        )
        session.add(object_obj)
        session.commit()
        
        # Create versioning records
        version1 = Versioning(
            object_id=object_obj.id,
            version="1.0.0",
            created_at=datetime.now()
        )
        version2 = Versioning(
            object_id=object_obj.id,
            version="2.0.0",
            created_at=datetime.now()
        )
        session.add_all([version1, version2])
        session.commit()
        
        # Query versioning for the object
        object_versions = session.query(Versioning).filter_by(object_id=object_obj.id).all()
        assert len(object_versions) == 2
        
        # Query specific version
        specific_version = session.query(Versioning).filter_by(
            object_id=object_obj.id, version="1.0.0"
        ).first()
        assert specific_version is not None
        assert specific_version.version == "1.0.0"

    @pytest.mark.unit
    def test_attributes_object_relationship(self, engine_and_session):
        """Test the relationship between Attributes and Object."""
        engine, session = engine_and_session
        
        # Create an object
        type_obj = Type(type_name="document")
        session.add(type_obj)
        session.commit()
        
        object_obj = Object(
            name="test_document",
            version=1,
            type_id=type_obj.id,
            created_on="2024-01-01T00:00:00",
            created_by="user1"
        )
        session.add(object_obj)
        session.commit()
        
        # Create attributes for this object
        attr1 = Attributes(
            name="color",
            value="red",
            object_id=object_obj.id,
            created_on="2024-01-01T00:00:00",
            updated_on="2024-01-01T00:00:00"
        )
        attr2 = Attributes(
            name="size",
            value="large",
            object_id=object_obj.id,
            created_on="2024-01-01T00:00:00",
            updated_on="2024-01-01T00:00:00"
        )
        session.add_all([attr1, attr2])
        session.commit()
        
        # Query attributes for the object
        object_attributes = session.query(Attributes).filter_by(object_id=object_obj.id).all()
        assert len(object_attributes) == 2
        
        # Query specific attribute by name
        color_attr = session.query(Attributes).filter_by(
            object_id=object_obj.id, name="color"
        ).first()
        assert color_attr is not None
        assert color_attr.value == "red"

    @pytest.mark.unit
    def test_object_relationship_navigation(self, engine_and_session):
        """Test navigating relationships from Object model."""
        engine, session = engine_and_session
        
        # Create type and object
        type_obj = Type(type_name="document")
        session.add(type_obj)
        session.commit()
        
        object_obj = Object(
            name="test_document",
            version=1,
            type_id=type_obj.id,
            created_on="2024-01-01T00:00:00",
            created_by="user1"
        )
        session.add(object_obj)
        session.commit()
        
        # Create related records
        permission = Permissions(
            object_id=object_obj.id,
            user="test_user",
            permission_level="read"
        )
        versioning = Versioning(
            object_id=object_obj.id,
            version="1.0.0",
            created_at=datetime.now()
        )
        attribute = Attributes(
            name="color",
            value="red",
            object_id=object_obj.id,
            created_on="2024-01-01T00:00:00",
            updated_on="2024-01-01T00:00:00"
        )
        session.add_all([permission, versioning, attribute])
        session.commit()
        
        # Test relationship navigation
        # Refresh object to load relationships
        session.refresh(object_obj)
        
        # Test type relationship
        assert object_obj.type is not None
        assert object_obj.type.type_name == "document"
        
        # Test permissions relationship
        assert len(object_obj.permissions) == 1
        assert object_obj.permissions[0].user == "test_user"
        
        # Test versioning relationship
        assert len(object_obj.versioning_records) == 1
        assert object_obj.versioning_records[0].version == "1.0.0"
        
        # Test attributes relationship
        assert len(object_obj.attributes) == 1
        assert object_obj.attributes[0].name == "color"


class TestModelValidation:
    """Test model validation and constraints."""

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

    @pytest.mark.unit
    def test_type_name_required(self, engine_and_session):
        """Test that type_name is required for Type model."""
        engine, session = engine_and_session
        
        # Try to create a type without name
        type_obj = Type()  # Missing type_name
        session.add(type_obj)
        
        # This should raise an error
        with pytest.raises(Exception):
            session.commit()

    @pytest.mark.unit
    def test_object_required_fields(self, engine_and_session):
        """Test that required fields are enforced for Object model."""
        engine, session = engine_and_session
        
        # Create a type first
        type_obj = Type(type_name="test_type")
        session.add(type_obj)
        session.commit()
        
        # Try to create an object without required fields
        object_obj = Object()  # Missing all required fields
        session.add(object_obj)
        
        # This should raise an error
        with pytest.raises(Exception):
            session.commit()

    @pytest.mark.unit
    def test_link_required_fields(self, engine_and_session):
        """Test that required fields are enforced for Link model."""
        engine, session = engine_and_session
        
        # Try to create a link without required fields
        link = Link()  # Missing all required fields
        session.add(link)
        
        # This should raise an error
        with pytest.raises(Exception):
            session.commit()

    @pytest.mark.unit
    def test_permissions_required_fields(self, engine_and_session):
        """Test that required fields are enforced for Permissions model."""
        engine, session = engine_and_session
        
        # Try to create a permission without required fields
        permission = Permissions()  # Missing all required fields
        session.add(permission)
        
        # This should raise an error
        with pytest.raises(Exception):
            session.commit()

    @pytest.mark.unit
    def test_versioning_required_fields(self, engine_and_session):
        """Test that required fields are enforced for Versioning model."""
        engine, session = engine_and_session
        
        # Try to create a versioning record without required fields
        versioning = Versioning()  # Missing all required fields
        session.add(versioning)
        
        # This should raise an error
        with pytest.raises(Exception):
            session.commit()

    @pytest.mark.unit
    def test_attributes_required_fields(self, engine_and_session):
        """Test that required fields are enforced for Attributes model."""
        engine, session = engine_and_session
        
        # Try to create an attribute without required fields
        attribute = Attributes()  # Missing all required fields
        session.add(attribute)
        
        # This should raise an error
        with pytest.raises(Exception):
            session.commit()


class TestDatabaseOperations:
    """Test database operations and utility functions."""

    @pytest.mark.unit
    def test_create_engine_and_session(self):
        """Test the create_engine_and_session utility function."""
        engine, SessionLocal = create_engine_and_session("sqlite:///:memory:")
        
        assert engine is not None
        assert SessionLocal is not None
        
        # Test that we can create a session
        session = SessionLocal()
        assert session is not None
        session.close()

    @pytest.mark.unit
    def test_create_tables(self):
        """Test the create_tables utility function."""
        engine = create_engine("sqlite:///:memory:", echo=False)
        
        # Create tables
        create_tables(engine)
        
        # Verify tables exist by checking if we can query them
        from sqlalchemy import inspect
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        
        expected_tables = ['type', 'object', 'link', 'permissions', 'versioning', 'attributes']
        for table in expected_tables:
            assert table in table_names

    @pytest.mark.unit
    def test_database_transactions(self):
        """Test database transaction behavior."""
        engine = create_engine("sqlite:///:memory:", echo=False)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        create_tables(engine)
        session = SessionLocal()
        
        try:
            # Create a type
            type_obj = Type(type_name="test_type")
            session.add(type_obj)
            session.commit()
            
            # Verify it was committed
            assert type_obj.id is not None
            
            # Test rollback
            new_type = Type(type_name="rollback_test")
            session.add(new_type)
            session.rollback()
            
            # The new type should not be in the database
            retrieved = session.query(Type).filter_by(type_name="rollback_test").first()
            assert retrieved is None
            
            # But the original should still be there
            original = session.query(Type).filter_by(type_name="test_type").first()
            assert original is not None
        finally:
            session.close()
            engine.dispose()

    @pytest.mark.unit
    def test_get_db_session_generator(self):
        """Test the get_db_session generator function."""
        engine = create_engine("sqlite:///:memory:", echo=False)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        create_tables(engine)
        
        # Test the generator function
        session_gen = get_db_session(SessionLocal)
        session = next(session_gen)
        
        assert session is not None
        assert hasattr(session, 'close')
        assert hasattr(session, 'is_active')
        
        # Test that it's a generator function
        assert hasattr(session_gen, '__iter__')
        assert hasattr(session_gen, '__next__') 