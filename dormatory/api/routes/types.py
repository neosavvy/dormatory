"""
Types API routes for DORMATORY.

This module provides RESTful API endpoints for managing type entities.
"""

from typing import List, Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from dormatory.api.dependencies import get_db
from dormatory.models.dormatory_model import Type, Object

router = APIRouter(tags=["types"])


class TypeCreate(BaseModel):
    type_name: str


class TypeUpdate(BaseModel):
    type_name: Optional[str] = None


class TypeResponse(BaseModel):
    id: UUID
    type_name: str

    class Config:
        from_attributes = True


class ObjectResponse(BaseModel):
    id: int
    name: str
    version: int
    type_id: UUID
    created_on: str
    created_by: str

    class Config:
        from_attributes = True


@router.post("/", response_model=TypeResponse)
async def create_type(type_data: TypeCreate, db: Session = Depends(get_db)):
    """
    Create a new type.
    
    Args:
        type_data: Type creation data
        db: Database session
        
    Returns:
        Created type data
    """
    # Create the type
    db_type = Type(type_name=type_data.type_name)
    
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    
    return TypeResponse.from_orm(db_type)


@router.get("/{type_id}", response_model=TypeResponse)
async def get_type_by_id(type_id: UUID, db: Session = Depends(get_db)):
    """
    Get a type by its ID.
    
    Args:
        type_id: Type ID
        db: Database session
        
    Returns:
        Type data
    """
    db_type = db.query(Type).filter(Type.id == type_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Type not found")
    
    return TypeResponse.from_orm(db_type)


@router.get("/", response_model=List[TypeResponse])
async def get_all_types(
    skip: int = 0,
    limit: int = 100,
    type_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all types with optional filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        type_name: Filter by type name
        db: Database session
        
    Returns:
        List of types
    """
    query = db.query(Type)
    
    # Apply filters
    if type_name:
        query = query.filter(Type.type_name.contains(type_name))
    
    # Apply pagination
    types = query.offset(skip).limit(limit).all()
    
    return [TypeResponse.from_orm(type_obj) for type_obj in types]


@router.put("/{type_id}", response_model=TypeResponse)
async def update_type(type_id: UUID, type_data: TypeUpdate, db: Session = Depends(get_db)):
    """
    Update an existing type.
    
    Args:
        type_id: Type ID to update
        type_data: Updated type data
        db: Database session
        
    Returns:
        Updated type data
    """
    db_type = db.query(Type).filter(Type.id == type_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Type not found")
    
    # Update fields if provided
    if type_data.type_name is not None:
        db_type.type_name = type_data.type_name
    
    db.commit()
    db.refresh(db_type)
    
    return TypeResponse.from_orm(db_type)


@router.delete("/{type_id}")
async def delete_type(type_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a type.
    
    Args:
        type_id: Type ID to delete
        db: Database session
        
    Returns:
        Success message
    """
    db_type = db.query(Type).filter(Type.id == type_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Type not found")
    
    db.delete(db_type)
    db.commit()
    
    return {"message": "Type deleted successfully"}


@router.post("/bulk", response_model=List[TypeResponse])
async def create_types_bulk(type_data: List[TypeCreate], db: Session = Depends(get_db)):
    """
    Create multiple types in a single operation.
    
    Args:
        type_data: List of type creation data
        db: Database session
        
    Returns:
        List of created types
    """
    created_types = []
    
    for item in type_data:
        # Create the type
        db_type = Type(type_name=item.type_name)
        
        db.add(db_type)
        created_types.append(db_type)
    
    db.commit()
    
    # Refresh all types to get their IDs
    for type_obj in created_types:
        db.refresh(type_obj)
    
    return [TypeResponse.from_orm(type_obj) for type_obj in created_types]


@router.get("/{type_id}/objects", response_model=List[ObjectResponse])
async def get_objects_by_type(type_id: UUID, db: Session = Depends(get_db)):
    """
    Get all objects of a specific type.
    
    Args:
        type_id: Type ID
        db: Database session
        
    Returns:
        List of objects of the specified type
    """
    # First verify the type exists
    db_type = db.query(Type).filter(Type.id == type_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Type not found")
    
    # Get all objects of this type
    objects = db.query(Object).filter(Object.type_id == type_id).all()
    
    return [ObjectResponse.from_orm(obj) for obj in objects] 