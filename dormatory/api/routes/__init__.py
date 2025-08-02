"""
DORMATORY API Routes Package

This package contains all the FastAPI route modules for different entities.
"""

from . import objects, types, links, permissions, versioning, attributes

__all__ = [
    "objects",
    "types",
    "links", 
    "permissions",
    "versioning",
    "attributes",
] 