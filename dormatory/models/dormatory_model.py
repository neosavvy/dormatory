"""
DORMATORY SQLAlchemy Models

This module defines the core models for storing structured hierarchical data
using a flat set of tables as shown in the ERD.
"""

from datetime import datetime, UTC
from typing import Optional, List
from uuid import UUID, uuid4

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, 
    create_engine, MetaData
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

# Create declarative base
Base = declarative_base()


class Type(Base):
    """
    Defines different categories or types for the object entities.
    
    This table stores the various types that objects can have, providing
    a way to categorize and organize the hierarchical data structure.
    """
    __tablename__ = "type"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    type_name = Column(Text, nullable=False)
    
    # Relationships
    objects = relationship("Object", back_populates="type")
    
    def __repr__(self) -> str:
        return f"<Type(id={self.id}, type_name='{self.type_name}')>"


class Object(Base):
    """
    Core table representing the main data entities in the system.
    
    This is the central entity that represents objects in the hierarchical
    data structure. Each object has a type and can participate in various
    relationships through the link table.
    """
    __tablename__ = "object"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    type_id = Column(PostgresUUID(as_uuid=True), ForeignKey("type.id"), nullable=False)
    created_on = Column(Text, nullable=False)
    created_by = Column(Text, nullable=False)
    
    # Relationships
    type = relationship("Type", back_populates="objects")
    permissions = relationship("Permissions", back_populates="object")
    versioning_records = relationship("Versioning", back_populates="object")
    attributes = relationship("Attributes", back_populates="object")
    
    # Self-referencing relationships through link table
    parent_links = relationship(
        "Link",
        foreign_keys="Link.child_id",
        back_populates="child"
    )
    child_links = relationship(
        "Link", 
        foreign_keys="Link.parent_id",
        back_populates="parent"
    )
    
    def __repr__(self) -> str:
        return f"<Object(id={self.id}, name='{self.name}', type_id={self.type_id})>"


class Link(Base):
    """
    Manages hierarchical parent-child relationships between object entities.
    
    This table allows for a flexible, flat representation of tree-like structures
    by establishing parent-child relationships between objects. An object can be
    both a parent and child in different relationships.
    """
    __tablename__ = "link"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey("object.id"), nullable=False)
    parent_type = Column(String, nullable=False)
    child_type = Column(String, nullable=False)
    r_name = Column(String, nullable=False)  # Relationship name (e.g., "contains", "part_of")
    child_id = Column(Integer, ForeignKey("object.id"), nullable=False)
    
    # Relationships
    parent = relationship("Object", foreign_keys=[parent_id], back_populates="child_links")
    child = relationship("Object", foreign_keys=[child_id], back_populates="parent_links")
    
    def __repr__(self) -> str:
        return f"<Link(id={self.id}, parent_id={self.parent_id}, child_id={self.child_id}, r_name='{self.r_name}')>"


class Permissions(Base):
    """
    Stores access control information for specific object entities.
    
    This table manages permissions for objects, allowing fine-grained access
    control based on users and permission levels.
    """
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    object_id = Column(Integer, ForeignKey("object.id"), nullable=False)
    user = Column(String, nullable=False)
    permission_level = Column(String, nullable=False)
    
    # Relationships
    object = relationship("Object", back_populates="permissions")
    
    def __repr__(self) -> str:
        return f"<Permissions(id={self.id}, object_id={self.object_id}, user='{self.user}', permission_level='{self.permission_level}')>"


class Versioning(Base):
    """
    Tracks different historical versions of object entities.
    
    This table maintains version history for objects, allowing tracking of
    changes over time with version strings and timestamps.
    """
    __tablename__ = "versioning"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    object_id = Column(Integer, ForeignKey("object.id"), nullable=False)
    version = Column(String, nullable=False)  # Version string/tag
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    
    # Relationships
    object = relationship("Object", back_populates="versioning_records")
    
    def __repr__(self) -> str:
        return f"<Versioning(id={self.id}, object_id={self.object_id}, version='{self.version}')>"


class Attributes(Base):
    """
    Stores arbitrary key-value attributes associated with object entities.
    
    This table allows for flexible schema extension by storing arbitrary
    key-value pairs for objects, enabling dynamic attribute addition.
    """
    __tablename__ = "attributes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)  # Attribute name (e.g., "color", "size")
    value = Column(String, nullable=False)  # Attribute value (e.g., "red", "large")
    object_id = Column(Integer, ForeignKey("object.id"), nullable=False)
    created_on = Column(String, nullable=False)
    updated_on = Column(String, nullable=False)
    
    # Relationships
    object = relationship("Object", back_populates="attributes")
    
    def __repr__(self) -> str:
        return f"<Attributes(id={self.id}, object_id={self.object_id}, name='{self.name}', value='{self.value}')>"


# Database session management
def create_engine_and_session(database_url: str = "sqlite:///dormatory.db"):
    """
    Create SQLAlchemy engine and session factory.
    
    Args:
        database_url: Database connection URL
        
    Returns:
        Tuple of (engine, SessionLocal)
    """
    engine = create_engine(database_url, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal


def create_tables(engine):
    """
    Create all tables in the database.
    
    Args:
        engine: SQLAlchemy engine instance
    """
    Base.metadata.create_all(bind=engine)


def get_db_session(SessionLocal) -> Session:
    """
    Get a database session.
    
    Args:
        SessionLocal: Session factory
        
    Returns:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 