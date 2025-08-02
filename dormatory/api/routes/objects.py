"""
Objects API routes for DORMATORY.

This module provides RESTful API endpoints for managing object entities.
"""

from typing import List, Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from dormatory.api.dependencies import get_db
from dormatory.models.dormatory_model import Object, Type, Link

router = APIRouter(tags=["objects"])

class ObjectCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Object name (cannot be empty)")
    version: Optional[int] = 1
    type_id: UUID
    created_on: str
    created_by: str


class ObjectUpdate(BaseModel):
    name: Optional[str] = None
    version: Optional[int] = None
    type_id: Optional[UUID] = None


class ObjectResponse(BaseModel):
    id: int
    name: str
    version: int
    type_id: UUID
    created_on: str
    created_by: str

    class Config:
        from_attributes = True


@router.post("/", response_model=ObjectResponse)
async def create_object(object_data: ObjectCreate, db: Session = Depends(get_db)):
    """
    Create a new object.
    
    Args:
        object_data: Object creation data
        db: Database session
        
    Returns:
        Created object data
    """
    # Verify that the type exists
    type_obj = db.query(Type).filter(Type.id == object_data.type_id).first()
    if not type_obj:
        raise HTTPException(status_code=404, detail="Type not found")
    
    # Create the object
    db_object = Object(
        name=object_data.name,
        version=object_data.version or 1,
        type_id=object_data.type_id,
        created_on=object_data.created_on,
        created_by=object_data.created_by
    )
    
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    
    return ObjectResponse.from_orm(db_object)


@router.get("/{object_id}", response_model=ObjectResponse)
async def get_object_by_id(object_id: int, db: Session = Depends(get_db)):
    """
    Get an object by its ID.
    
    Args:
        object_id: Object ID
        db: Database session
        
    Returns:
        Object data
    """
    db_object = db.query(Object).filter(Object.id == object_id).first()
    if not db_object:
        raise HTTPException(status_code=404, detail="Object not found")
    
    return ObjectResponse.from_orm(db_object)


@router.get("/", response_model=List[ObjectResponse])
async def get_all_objects(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    type_id: Optional[UUID] = None,
    db: Session = Depends(get_db)
):
    """
    Get all objects with optional filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        name: Filter by object name
        type_id: Filter by type ID
        db: Database session
        
    Returns:
        List of objects
    """
    query = db.query(Object)
    
    # Apply filters
    if name:
        query = query.filter(Object.name.contains(name))
    if type_id:
        query = query.filter(Object.type_id == type_id)
    
    # Apply pagination
    objects = query.offset(skip).limit(limit).all()
    
    return [ObjectResponse.from_orm(obj) for obj in objects]


@router.put("/{object_id}", response_model=ObjectResponse)
async def update_object(object_id: int, object_data: ObjectUpdate, db: Session = Depends(get_db)):
    """
    Update an existing object.
    
    Args:
        object_id: Object ID to update
        object_data: Updated object data
        db: Database session
        
    Returns:
        Updated object data
    """
    db_object = db.query(Object).filter(Object.id == object_id).first()
    if not db_object:
        raise HTTPException(status_code=404, detail="Object not found")
    
    # Update fields if provided
    if object_data.name is not None:
        db_object.name = object_data.name
    if object_data.version is not None:
        db_object.version = object_data.version
    if object_data.type_id is not None:
        # Verify that the new type exists
        type_obj = db.query(Type).filter(Type.id == object_data.type_id).first()
        if not type_obj:
            raise HTTPException(status_code=404, detail="Type not found")
        db_object.type_id = object_data.type_id
    
    db.commit()
    db.refresh(db_object)
    
    return ObjectResponse.from_orm(db_object)


@router.delete("/{object_id}")
async def delete_object(object_id: int, db: Session = Depends(get_db)):
    """
    Delete an object.
    
    Args:
        object_id: Object ID to delete
        db: Database session
        
    Returns:
        Success message
    """
    db_object = db.query(Object).filter(Object.id == object_id).first()
    if not db_object:
        raise HTTPException(status_code=404, detail="Object not found")
    
    db.delete(db_object)
    db.commit()
    
    return {"message": "Object deleted successfully"}


@router.post("/bulk", response_model=List[ObjectResponse])
async def create_objects_bulk(object_data: List[ObjectCreate], db: Session = Depends(get_db)):
    """
    Create multiple objects in a single operation.
    
    Args:
        object_data: List of object creation data
        db: Database session
        
    Returns:
        List of created objects
    """
    created_objects = []
    
    for item in object_data:
        # Verify that the type exists
        type_obj = db.query(Type).filter(Type.id == item.type_id).first()
        if not type_obj:
            raise HTTPException(status_code=404, detail=f"Type {item.type_id} not found")
        
        # Create the object
        db_object = Object(
            name=item.name,
            version=item.version or 1,
            type_id=item.type_id,
            created_on=item.created_on,
            created_by=item.created_by
        )
        
        db.add(db_object)
        created_objects.append(db_object)
    
    db.commit()
    
    # Refresh all objects to get their IDs
    for obj in created_objects:
        db.refresh(obj)
    
    return [ObjectResponse.from_orm(obj) for obj in created_objects]


@router.get("/{object_id}/children")
async def get_object_children(object_id: int, db: Session = Depends(get_db)):
    """
    Get all children of an object.
    
    Args:
        object_id: Object ID
        db: Database session
        
    Returns:
        List of child objects with relationship information
    """
    # Verify that the object exists
    db_object = db.query(Object).filter(Object.id == object_id).first()
    if not db_object:
        raise HTTPException(status_code=404, detail="Object not found")
    
    # Get all links where this object is the parent
    links = db.query(Link).filter(Link.parent_id == object_id).all()
    
    # Get the child objects
    child_ids = [link.child_id for link in links]
    children = db.query(Object).filter(Object.id.in_(child_ids)).all()
    
    return [
        {
            "id": child.id,
            "name": child.name,
            "version": child.version,
            "type_id": str(child.type_id),
            "created_on": child.created_on,
            "created_by": child.created_by,
            "relationship": next(link.r_name for link in links if link.child_id == child.id)
        }
        for child in children
    ]


@router.get("/{object_id}/parents")
async def get_object_parents(object_id: int, db: Session = Depends(get_db)):
    """
    Get all parents of an object.
    
    Args:
        object_id: Object ID
        db: Database session
        
    Returns:
        List of parent objects with relationship information
    """
    # Verify that the object exists
    db_object = db.query(Object).filter(Object.id == object_id).first()
    if not db_object:
        raise HTTPException(status_code=404, detail="Object not found")
    
    # Get all links where this object is the child
    links = db.query(Link).filter(Link.child_id == object_id).all()
    
    # Get the parent objects
    parent_ids = [link.parent_id for link in links]
    parents = db.query(Object).filter(Object.id.in_(parent_ids)).all()
    
    return [
        {
            "id": parent.id,
            "name": parent.name,
            "version": parent.version,
            "type_id": str(parent.type_id),
            "created_on": parent.created_on,
            "created_by": parent.created_by,
            "relationship": next(link.r_name for link in links if link.parent_id == parent.id)
        }
        for parent in parents
    ]


@router.get("/{object_id}/hierarchy")
async def get_object_hierarchy(object_id: int, db: Session = Depends(get_db)):
    """
    Get the complete hierarchy for an object.
    
    Args:
        object_id: Object ID
        db: Database session
        
    Returns:
        Complete hierarchy tree
    """
    # Verify that the object exists
    db_object = db.query(Object).filter(Object.id == object_id).first()
    if not db_object:
        raise HTTPException(status_code=404, detail="Object not found")
    
    def build_hierarchy(obj_id: int, visited: set = None) -> dict:
        """Recursively build the hierarchy tree."""
        if visited is None:
            visited = set()
        
        if obj_id in visited:
            return None  # Prevent circular references
        
        visited.add(obj_id)
        
        # Get the object
        obj = db.query(Object).filter(Object.id == obj_id).first()
        if not obj:
            return None
        
        # Get children
        child_links = db.query(Link).filter(Link.parent_id == obj_id).all()
        children = []
        
        for link in child_links:
            child_hierarchy = build_hierarchy(link.child_id, visited.copy())
            if child_hierarchy:
                children.append({
                    "object": child_hierarchy,
                    "relationship": link.r_name
                })
        
        return {
            "id": obj.id,
            "name": obj.name,
            "version": obj.version,
            "type_id": str(obj.type_id),
            "created_on": obj.created_on,
            "created_by": obj.created_by,
            "children": children
        }
    
    hierarchy = build_hierarchy(object_id)
    return hierarchy


@router.get("/{object_id}/hierarchy/{depth}")
async def get_object_hierarchy_with_depth(object_id: int, depth: int, db: Session = Depends(get_db)):
    """
    Get the hierarchy for an object up to a specific depth.
    
    Args:
        object_id: Object ID
        depth: Maximum depth to retrieve
        db: Database session
        
    Returns:
        Hierarchy tree up to specified depth
    """
    if depth < 0:
        raise HTTPException(status_code=422, detail="Depth must be non-negative")
    
    # Verify that the object exists
    db_object = db.query(Object).filter(Object.id == object_id).first()
    if not db_object:
        raise HTTPException(status_code=404, detail="Object not found")
    
    def build_hierarchy_with_depth(obj_id: int, current_depth: int, visited: set = None) -> dict:
        """Recursively build the hierarchy tree up to specified depth."""
        if visited is None:
            visited = set()
        
        if obj_id in visited or current_depth > depth:
            return None  # Prevent circular references or exceed depth limit
        
        visited.add(obj_id)
        
        # Get the object
        obj = db.query(Object).filter(Object.id == obj_id).first()
        if not obj:
            return None
        
        # Get children if we haven't reached the depth limit
        children = []
        if current_depth < depth:
            child_links = db.query(Link).filter(Link.parent_id == obj_id).all()
            
            for link in child_links:
                child_hierarchy = build_hierarchy_with_depth(link.child_id, current_depth + 1, visited.copy())
                if child_hierarchy:
                    children.append({
                        "object": child_hierarchy,
                        "relationship": link.r_name
                    })
        
        return {
            "id": obj.id,
            "name": obj.name,
            "version": obj.version,
            "type_id": str(obj.type_id),
            "created_on": obj.created_on,
            "created_by": obj.created_by,
            "children": children,
            "depth": current_depth
        }
    
    hierarchy = build_hierarchy_with_depth(object_id, 0)
    return hierarchy 