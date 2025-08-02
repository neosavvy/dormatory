"""
Basic Usage Example for DORMATORY Models

This example demonstrates how to use the DORMATORY SQLAlchemy models
to create and manage hierarchical data structures.
"""

import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dormatory.models.dormatory_model import (
    Type, Object, Link, Permissions, Versioning, Attributes,
    create_engine_and_session, create_tables
)


def main():
    """Demonstrate basic usage of the DORMATORY models."""
    
    # Create database engine and session
    engine, SessionLocal = create_engine_and_session("sqlite:///dormatory_example.db")
    create_tables(engine)
    
    # Create a session
    session = SessionLocal()
    
    try:
        # Create some types
        folder_type = Type(type_name="folder")
        file_type = Type(type_name="file")
        user_type = Type(type_name="user")
        
        session.add_all([folder_type, file_type, user_type])
        session.commit()
        
        # Create some objects
        root_folder = Object(
            name="Root",
            version=1,
            type_id=folder_type.id,
            created_on=datetime.now().isoformat(),
            created_by="system"
        )
        
        documents_folder = Object(
            name="Documents",
            version=1,
            type_id=folder_type.id,
            created_on=datetime.now().isoformat(),
            created_by="system"
        )
        
        readme_file = Object(
            name="README.md",
            version=1,
            type_id=file_type.id,
            created_on=datetime.now().isoformat(),
            created_by="user1"
        )
        
        session.add_all([root_folder, documents_folder, readme_file])
        session.commit()
        
        # Create hierarchical relationships
        root_to_docs = Link(
            parent_id=root_folder.id,
            parent_type="folder",
            child_type="folder",
            r_name="contains",
            child_id=documents_folder.id
        )
        
        docs_to_readme = Link(
            parent_id=documents_folder.id,
            parent_type="folder",
            child_type="file",
            r_name="contains",
            child_id=readme_file.id
        )
        
        session.add_all([root_to_docs, docs_to_readme])
        session.commit()
        
        # Add some attributes
        readme_attributes = [
            Attributes(
                name="size",
                value="1024",
                object_id=readme_file.id,
                created_on=datetime.now().isoformat(),
                updated_on=datetime.now().isoformat()
            ),
            Attributes(
                name="extension",
                value=".md",
                object_id=readme_file.id,
                created_on=datetime.now().isoformat(),
                updated_on=datetime.now().isoformat()
            )
        ]
        
        session.add_all(readme_attributes)
        session.commit()
        
        # Add permissions
        readme_permission = Permissions(
            object_id=readme_file.id,
            user="user1",
            permission_level="read_write"
        )
        
        session.add(readme_permission)
        session.commit()
        
        # Add versioning
        readme_version = Versioning(
            object_id=readme_file.id,
            version="1.0.0",
            created_at=datetime.now()
        )
        
        session.add(readme_version)
        session.commit()
        
        # Query and display the hierarchy
        print("=== DORMATORY Hierarchical Data Example ===\n")
        
        # Show all objects
        print("All Objects:")
        for obj in session.query(Object).all():
            print(f"  - {obj.name} (Type: {obj.type.type_name}, ID: {obj.id})")
        
        print("\nHierarchical Structure:")
        # Find root objects (objects that are children but not parents)
        root_objects = session.query(Object).filter(
            ~Object.id.in_(
                session.query(Link.parent_id).distinct()
            )
        ).all()
        
        for root in root_objects:
            print_hierarchy(session, root, 0)
        
        print("\nObject Attributes:")
        for obj in session.query(Object).all():
            if obj.attributes:
                print(f"  {obj.name}:")
                for attr in obj.attributes:
                    print(f"    {attr.name}: {attr.value}")
        
        print("\nPermissions:")
        for perm in session.query(Permissions).all():
            obj = session.query(Object).filter(Object.id == perm.object_id).first()
            print(f"  {obj.name} - User: {perm.user}, Level: {perm.permission_level}")
        
    finally:
        session.close()


def print_hierarchy(session, obj, level):
    """Recursively print the hierarchical structure."""
    indent = "  " * level
    print(f"{indent}{obj.name} ({obj.type.type_name})")
    
    # Find children of this object
    children = session.query(Link).filter(Link.parent_id == obj.id).all()
    for child_link in children:
        child = session.query(Object).filter(Object.id == child_link.child_id).first()
        print_hierarchy(session, child, level + 1)


if __name__ == "__main__":
    main() 