"""
Attributes API routes for DORMATORY.

This module provides RESTful API endpoints for managing attribute entities.
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from dormatory.api.dependencies import get_db
from dormatory.models.dormatory_model import Attributes, Object

router = APIRouter(tags=["attributes"])


class AttributeCreate(BaseModel):
    name: str
    value: str
    object_id: int
    created_on: str
    updated_on: str


class AttributeUpdate(BaseModel):
    name: Optional[str] = None
    value: Optional[str] = None
    updated_on: Optional[str] = None


class AttributeResponse(BaseModel):
    id: int
    name: str
    value: str
    object_id: int
    created_on: str
    updated_on: str

    class Config:
        from_attributes = True


@router.post("/", response_model=AttributeResponse)
async def create_attribute(attribute_data: AttributeCreate, db: Session = Depends(get_db)):
    """
    Create a new attribute.
    
    Args:
        attribute_data: Attribute creation data
        db: Database session
        
    Returns:
        Created attribute data
    """
    # Verify that the object exists
    object_obj = db.query(Object).filter(Object.id == attribute_data.object_id).first()
    if not object_obj:
        raise HTTPException(status_code=404, detail="Object not found")
    
    # Check if attribute already exists for this object
    existing_attribute = db.query(Attributes).filter(
        Attributes.object_id == attribute_data.object_id,
        Attributes.name == attribute_data.name
    ).first()
    
    if existing_attribute:
        raise HTTPException(status_code=409, detail="Attribute already exists for this object")
    
    # Create the attribute
    db_attribute = Attributes(
        name=attribute_data.name,
        value=attribute_data.value,
        object_id=attribute_data.object_id,
        created_on=attribute_data.created_on,
        updated_on=attribute_data.updated_on
    )
    
    db.add(db_attribute)
    db.commit()
    db.refresh(db_attribute)
    
    return AttributeResponse.from_orm(db_attribute)


@router.get("/{attribute_id}", response_model=AttributeResponse)
async def get_attribute_by_id(attribute_id: int, db: Session = Depends(get_db)):
    """
    Get an attribute by its ID.
    
    Args:
        attribute_id: Attribute ID
        db: Database session
        
    Returns:
        Attribute data
    """
    db_attribute = db.query(Attributes).filter(Attributes.id == attribute_id).first()
    if not db_attribute:
        raise HTTPException(status_code=404, detail="Attribute not found")
    
    return AttributeResponse.from_orm(db_attribute)


@router.get("/", response_model=List[AttributeResponse])
async def get_all_attributes(
    skip: int = 0,
    limit: int = 100,
    object_id: Optional[int] = None,
    name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all attributes with optional filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        object_id: Filter by object ID
        name: Filter by attribute name
        db: Database session
        
    Returns:
        List of attributes
    """
    query = db.query(Attributes)
    
    # Apply filters
    if object_id:
        query = query.filter(Attributes.object_id == object_id)
    if name:
        query = query.filter(Attributes.name == name)
    
    # Apply pagination
    attributes = query.offset(skip).limit(limit).all()
    
    return [AttributeResponse.from_orm(attr) for attr in attributes]


@router.put("/{attribute_id}", response_model=AttributeResponse)
async def update_attribute(attribute_id: int, attribute_data: AttributeUpdate, db: Session = Depends(get_db)):
    """
    Update an existing attribute.
    
    Args:
        attribute_id: Attribute ID to update
        attribute_data: Updated attribute data
        db: Database session
        
    Returns:
        Updated attribute data
    """
    db_attribute = db.query(Attributes).filter(Attributes.id == attribute_id).first()
    if not db_attribute:
        raise HTTPException(status_code=404, detail="Attribute not found")
    
    # Update fields if provided
    if attribute_data.name is not None:
        # Check if the new name conflicts with existing attribute for the same object
        if attribute_data.name != db_attribute.name:
            existing_attribute = db.query(Attributes).filter(
                Attributes.object_id == db_attribute.object_id,
                Attributes.name == attribute_data.name,
                Attributes.id != attribute_id
            ).first()
            
            if existing_attribute:
                raise HTTPException(status_code=409, detail="Attribute name already exists for this object")
        
        db_attribute.name = attribute_data.name
    
    if attribute_data.value is not None:
        db_attribute.value = attribute_data.value
    
    if attribute_data.updated_on is not None:
        db_attribute.updated_on = attribute_data.updated_on
    
    db.commit()
    db.refresh(db_attribute)
    
    return AttributeResponse.from_orm(db_attribute)


@router.delete("/{attribute_id}")
async def delete_attribute(attribute_id: int, db: Session = Depends(get_db)):
    """
    Delete an attribute.
    
    Args:
        attribute_id: Attribute ID to delete
        db: Database session
        
    Returns:
        Success message
    """
    db_attribute = db.query(Attributes).filter(Attributes.id == attribute_id).first()
    if not db_attribute:
        raise HTTPException(status_code=404, detail="Attribute not found")
    
    db.delete(db_attribute)
    db.commit()
    
    return {"message": "Attribute deleted successfully"}


@router.post("/bulk", response_model=List[AttributeResponse])
async def create_attributes_bulk(attribute_data: List[AttributeCreate], db: Session = Depends(get_db)):
    """
    Create multiple attributes in a single operation.
    
    Args:
        attribute_data: List of attribute creation data
        db: Database session
        
    Returns:
        List of created attributes
    """
    created_attributes = []
    
    for item in attribute_data:
        # Verify that the object exists
        object_obj = db.query(Object).filter(Object.id == item.object_id).first()
        if not object_obj:
            raise HTTPException(status_code=404, detail=f"Object {item.object_id} not found")
        
        # Check if attribute already exists for this object
        existing_attribute = db.query(Attributes).filter(
            Attributes.object_id == item.object_id,
            Attributes.name == item.name
        ).first()
        
        if existing_attribute:
            raise HTTPException(status_code=409, detail=f"Attribute {item.name} already exists for object {item.object_id}")
        
        # Create the attribute
        db_attribute = Attributes(
            name=item.name,
            value=item.value,
            object_id=item.object_id,
            created_on=item.created_on,
            updated_on=item.updated_on
        )
        
        db.add(db_attribute)
        created_attributes.append(db_attribute)
    
    db.commit()
    
    # Refresh all attributes to get their IDs
    for attr in created_attributes:
        db.refresh(attr)
    
    return [AttributeResponse.from_orm(attr) for attr in created_attributes]


@router.get("/object/{object_id}")
async def get_attributes_by_object(object_id: int, db: Session = Depends(get_db)):
    """
    Get all attributes for a specific object.
    
    Args:
        object_id: Object ID
        db: Database session
        
    Returns:
        List of attributes for the object
    """
    # Verify that the object exists
    object_obj = db.query(Object).filter(Object.id == object_id).first()
    if not object_obj:
        raise HTTPException(status_code=404, detail="Object not found")
    
    attributes = db.query(Attributes).filter(Attributes.object_id == object_id).all()
    
    return [AttributeResponse.from_orm(attr) for attr in attributes]


@router.get("/name/{name}")
async def get_attribute_by_name(name: str, db: Session = Depends(get_db)):
    """
    Get all attributes with a specific name.
    
    Args:
        name: Attribute name
        db: Database session
        
    Returns:
        List of attributes with this name
    """
    attributes = db.query(Attributes).filter(Attributes.name == name).all()
    
    return [AttributeResponse.from_orm(attr) for attr in attributes]


@router.get("/object/{object_id}/map")
async def get_object_attributes_map(object_id: int, db: Session = Depends(get_db)):
    """
    Get all attributes for an object as a key-value map.
    
    Args:
        object_id: Object ID
        db: Database session
        
    Returns:
        Dictionary of attribute name-value pairs
    """
    # Verify that the object exists
    object_obj = db.query(Object).filter(Object.id == object_id).first()
    if not object_obj:
        raise HTTPException(status_code=404, detail="Object not found")
    
    attributes = db.query(Attributes).filter(Attributes.object_id == object_id).all()
    
    return {attr.name: attr.value for attr in attributes}


@router.post("/object/{object_id}/set")
async def set_object_attributes(object_id: int, attributes: dict, db: Session = Depends(get_db)):
    """
    Set multiple attributes for an object.
    
    Args:
        object_id: Object ID
        attributes: Dictionary of attribute name-value pairs
        db: Database session
        
    Returns:
        Success message
    """
    # Verify that the object exists
    object_obj = db.query(Object).filter(Object.id == object_id).first()
    if not object_obj:
        raise HTTPException(status_code=404, detail="Object not found")
    
    from datetime import datetime, UTC
    
    current_time = datetime.now(UTC).isoformat()
    created_attributes = []
    
    for name, value in attributes.items():
        # Check if attribute already exists
        existing_attribute = db.query(Attributes).filter(
            Attributes.object_id == object_id,
            Attributes.name == name
        ).first()
        
        if existing_attribute:
            # Update existing attribute
            existing_attribute.value = str(value)
            existing_attribute.updated_on = current_time
        else:
            # Create new attribute
            db_attribute = Attributes(
                name=name,
                value=str(value),
                object_id=object_id,
                created_on=current_time,
                updated_on=current_time
            )
            db.add(db_attribute)
            created_attributes.append(db_attribute)
    
    db.commit()
    
    return {"message": f"Set {len(attributes)} attributes for object {object_id}"}


@router.delete("/object/{object_id}/name/{name}")
async def delete_attribute_by_name(object_id: int, name: str, db: Session = Depends(get_db)):
    """
    Delete a specific attribute by name for an object.
    
    Args:
        object_id: Object ID
        name: Attribute name
        db: Database session
        
    Returns:
        Success message
    """
    # Verify that the object exists
    object_obj = db.query(Object).filter(Object.id == object_id).first()
    if not object_obj:
        raise HTTPException(status_code=404, detail="Object not found")
    
    # Find and delete the attribute
    db_attribute = db.query(Attributes).filter(
        Attributes.object_id == object_id,
        Attributes.name == name
    ).first()
    
    if not db_attribute:
        raise HTTPException(status_code=404, detail="Attribute not found")
    
    db.delete(db_attribute)
    db.commit()
    
    return {"message": f"Attribute '{name}' deleted for object {object_id}"}


@router.get("/search/{query}")
async def search_attributes(query: str, db: Session = Depends(get_db)):
    """
    Search attributes by name or value.
    
    Args:
        query: Search query
        db: Database session
        
    Returns:
        List of matching attributes
    """
    # Search in both name and value fields
    attributes = db.query(Attributes).filter(
        (Attributes.name.contains(query)) | (Attributes.value.contains(query))
    ).all()
    
    return [AttributeResponse.from_orm(attr) for attr in attributes] 