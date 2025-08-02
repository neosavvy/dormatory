"""
DORMATORY API Package

This package contains FastAPI endpoints for CRUD operations on hierarchical data.
"""

from .main import app
from .routes import objects, types, links, permissions, versioning, attributes

__all__ = [
    "app",
    "objects",
    "types", 
    "links",
    "permissions",
    "versioning",
    "attributes",
] 