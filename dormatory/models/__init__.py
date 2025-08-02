"""
DORMATORY Models Package

This package contains SQLAlchemy models for storing structured hierarchical data
using a flat set of tables.
"""

from .dormatory_model import (
    Object,
    Type,
    Link,
    Permissions,
    Versioning,
    Attributes,
)

__all__ = [
    "Object",
    "Type", 
    "Link",
    "Permissions",
    "Versioning",
    "Attributes",
] 