"""
Links API routes for DORMATORY.

This module provides RESTful API endpoints for managing link entities.
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from dormatory.api.dependencies import get_db
from dormatory.models.dormatory_model import Link, Object

router = APIRouter(tags=["links"])


class LinkCreate(BaseModel):
    parent_id: int
    parent_type: str
    child_type: str
    r_name: str
    child_id: int


class LinkUpdate(BaseModel):
    parent_type: Optional[str] = None
    child_type: Optional[str] = None
    r_name: Optional[str] = None


class LinkResponse(BaseModel):
    id: int
    parent_id: int
    parent_type: str
    child_type: str
    r_name: str
    child_id: int

    class Config:
        from_attributes = True


@router.post("/", response_model=LinkResponse)
async def create_link(link_data: LinkCreate, db: Session = Depends(get_db)):
    """
    Create a new link.
    
    Args:
        link_data: Link creation data
        db: Database session
        
    Returns:
        Created link data
    """
    # Verify that the parent object exists
    parent_obj = db.query(Object).filter(Object.id == link_data.parent_id).first()
    if not parent_obj:
        raise HTTPException(status_code=404, detail="Parent object not found")
    
    # Verify that the child object exists
    child_obj = db.query(Object).filter(Object.id == link_data.child_id).first()
    if not child_obj:
        raise HTTPException(status_code=404, detail="Child object not found")
    
    # Check for circular reference (parent cannot be child of its own child)
    if link_data.parent_id == link_data.child_id:
        raise HTTPException(status_code=422, detail="Cannot create self-referencing link")
    
    # Check if link already exists
    existing_link = db.query(Link).filter(
        Link.parent_id == link_data.parent_id,
        Link.child_id == link_data.child_id,
        Link.r_name == link_data.r_name
    ).first()
    
    if existing_link:
        raise HTTPException(status_code=409, detail="Link already exists")
    
    # Create the link
    db_link = Link(
        parent_id=link_data.parent_id,
        parent_type=link_data.parent_type,
        child_type=link_data.child_type,
        r_name=link_data.r_name,
        child_id=link_data.child_id
    )
    
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    
    return LinkResponse.from_orm(db_link)


@router.get("/{link_id}", response_model=LinkResponse)
async def get_link_by_id(link_id: int, db: Session = Depends(get_db)):
    """
    Get a link by its ID.
    
    Args:
        link_id: Link ID
        db: Database session
        
    Returns:
        Link data
    """
    db_link = db.query(Link).filter(Link.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    return LinkResponse.from_orm(db_link)


@router.get("/", response_model=List[LinkResponse])
async def get_all_links(
    skip: int = 0,
    limit: int = 100,
    parent_id: Optional[int] = None,
    child_id: Optional[int] = None,
    r_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all links with optional filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        parent_id: Filter by parent ID
        child_id: Filter by child ID
        r_name: Filter by relationship name
        db: Database session
        
    Returns:
        List of links
    """
    query = db.query(Link)
    
    # Apply filters
    if parent_id:
        query = query.filter(Link.parent_id == parent_id)
    if child_id:
        query = query.filter(Link.child_id == child_id)
    if r_name:
        query = query.filter(Link.r_name == r_name)
    
    # Apply pagination
    links = query.offset(skip).limit(limit).all()
    
    return [LinkResponse.from_orm(link) for link in links]


@router.put("/{link_id}", response_model=LinkResponse)
async def update_link(link_id: int, link_data: LinkUpdate, db: Session = Depends(get_db)):
    """
    Update an existing link.
    
    Args:
        link_id: Link ID to update
        link_data: Updated link data
        db: Database session
        
    Returns:
        Updated link data
    """
    db_link = db.query(Link).filter(Link.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    # Update fields if provided
    if link_data.parent_type is not None:
        db_link.parent_type = link_data.parent_type
    if link_data.child_type is not None:
        db_link.child_type = link_data.child_type
    if link_data.r_name is not None:
        db_link.r_name = link_data.r_name
    
    db.commit()
    db.refresh(db_link)
    
    return LinkResponse.from_orm(db_link)


@router.delete("/{link_id}")
async def delete_link(link_id: int, db: Session = Depends(get_db)):
    """
    Delete a link.
    
    Args:
        link_id: Link ID to delete
        db: Database session
        
    Returns:
        Success message
    """
    db_link = db.query(Link).filter(Link.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    db.delete(db_link)
    db.commit()
    
    return {"message": "Link deleted successfully"}


@router.post("/bulk", response_model=List[LinkResponse])
async def create_links_bulk(link_data: List[LinkCreate], db: Session = Depends(get_db)):
    """
    Create multiple links in a single operation.
    
    Args:
        link_data: List of link creation data
        db: Database session
        
    Returns:
        List of created links
    """
    created_links = []
    
    for item in link_data:
        # Verify that the parent object exists
        parent_obj = db.query(Object).filter(Object.id == item.parent_id).first()
        if not parent_obj:
            raise HTTPException(status_code=404, detail=f"Parent object {item.parent_id} not found")
        
        # Verify that the child object exists
        child_obj = db.query(Object).filter(Object.id == item.child_id).first()
        if not child_obj:
            raise HTTPException(status_code=404, detail=f"Child object {item.child_id} not found")
        
        # Check for circular reference
        if item.parent_id == item.child_id:
            raise HTTPException(status_code=422, detail="Cannot create self-referencing link")
        
        # Check if link already exists
        existing_link = db.query(Link).filter(
            Link.parent_id == item.parent_id,
            Link.child_id == item.child_id,
            Link.r_name == item.r_name
        ).first()
        
        if existing_link:
            raise HTTPException(status_code=409, detail=f"Link already exists between parent {item.parent_id} and child {item.child_id}")
        
        # Create the link
        db_link = Link(
            parent_id=item.parent_id,
            parent_type=item.parent_type,
            child_type=item.child_type,
            r_name=item.r_name,
            child_id=item.child_id
        )
        
        db.add(db_link)
        created_links.append(db_link)
    
    db.commit()
    
    # Refresh all links to get their IDs
    for link in created_links:
        db.refresh(link)
    
    return [LinkResponse.from_orm(link) for link in created_links]


@router.get("/parent/{parent_id}/children")
async def get_children_by_parent(parent_id: int, db: Session = Depends(get_db)):
    """
    Get all children of a parent object.
    
    Args:
        parent_id: Parent object ID
        db: Database session
        
    Returns:
        List of child objects
    """
    # Verify that the parent object exists
    parent_obj = db.query(Object).filter(Object.id == parent_id).first()
    if not parent_obj:
        raise HTTPException(status_code=404, detail="Parent object not found")
    
    # Get all links where this object is the parent
    links = db.query(Link).filter(Link.parent_id == parent_id).all()
    
    # Get the child objects
    child_ids = [link.child_id for link in links]
    children = db.query(Object).filter(Object.id.in_(child_ids)).all()
    
    return [
        {
            "id": child.id,
            "name": child.name,
            "type_id": str(child.type_id),
            "relationship": next(link.r_name for link in links if link.child_id == child.id)
        }
        for child in children
    ]


@router.get("/child/{child_id}/parents")
async def get_parents_by_child(child_id: int, db: Session = Depends(get_db)):
    """
    Get all parents of a child object.
    
    Args:
        child_id: Child object ID
        db: Database session
        
    Returns:
        List of parent objects
    """
    # Verify that the child object exists
    child_obj = db.query(Object).filter(Object.id == child_id).first()
    if not child_obj:
        raise HTTPException(status_code=404, detail="Child object not found")
    
    # Get all links where this object is the child
    links = db.query(Link).filter(Link.child_id == child_id).all()
    
    # Get the parent objects
    parent_ids = [link.parent_id for link in links]
    parents = db.query(Object).filter(Object.id.in_(parent_ids)).all()
    
    return [
        {
            "id": parent.id,
            "name": parent.name,
            "type_id": str(parent.type_id),
            "relationship": next(link.r_name for link in links if link.parent_id == parent.id)
        }
        for parent in parents
    ]


@router.get("/relationship/{r_name}")
async def get_links_by_relationship(r_name: str, db: Session = Depends(get_db)):
    """
    Get all links with a specific relationship name.
    
    Args:
        r_name: Relationship name
        db: Database session
        
    Returns:
        List of links with this relationship
    """
    links = db.query(Link).filter(Link.r_name == r_name).all()
    
    return [LinkResponse.from_orm(link) for link in links]


@router.post("/hierarchy")
async def create_hierarchy(hierarchy_data: dict, db: Session = Depends(get_db)):
    """
    Create a complete hierarchy structure.
    
    Args:
        hierarchy_data: Hierarchy creation data
        db: Database session
        
    Returns:
        Created hierarchy structure
    """
    # TODO: Implement hierarchy creation
    raise HTTPException(status_code=500, detail="Not implemented") 