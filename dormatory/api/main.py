"""
DORMATORY FastAPI Application

Main FastAPI application for the DORMATORY hierarchical data storage API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import objects, types, links, permissions, versioning, attributes
from .dependencies import engine
from dormatory.models.dormatory_model import create_tables

# Create FastAPI app
app = FastAPI(
    title="DORMATORY API",
    description="API for storing and querying structured hierarchical data using flat tables",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    """Create database tables on application startup."""
    create_tables(engine)

# Include routers
app.include_router(objects.router, prefix="/api/v1/objects", tags=["objects"])
app.include_router(types.router, prefix="/api/v1/types", tags=["types"])
app.include_router(links.router, prefix="/api/v1/links", tags=["links"])
app.include_router(permissions.router, prefix="/api/v1/permissions", tags=["permissions"])
app.include_router(versioning.router, prefix="/api/v1/versioning", tags=["versioning"])
app.include_router(attributes.router, prefix="/api/v1/attributes", tags=["attributes"])


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to DORMATORY API",
        "version": "0.1.0",
        "docs": "/docs",
        "description": "API for hierarchical data storage using flat tables"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "dormatory-api"} 