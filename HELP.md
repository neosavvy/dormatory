# DORMATORY Help Guide

This guide provides comprehensive information about using and developing the DORMATORY project.

## 🚀 Quick Start

### Basic Commands
```bash
# Activate virtual environment
uv shell

# Run the main application
python main.py

# Start the API server
python server.py

# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=dormatory
```

## 📁 Project Structure

```
dormatory/
├── dormatory/                    # Main package
│   ├── models/                   # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── dormatory_model.py   # Core data models
│   └── api/                      # FastAPI application
│       ├── __init__.py
│       ├── main.py              # FastAPI app setup
│       └── routes/              # API route modules
│           ├── __init__.py
│           ├── objects.py       # Object CRUD operations
│           ├── types.py         # Type management
│           ├── links.py         # Parent-child relationships
│           ├── permissions.py   # Access control
│           ├── versioning.py    # Version history
│           └── attributes.py    # Flexible attributes
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Test configuration
│   └── api/                     # API endpoint tests
│       ├── __init__.py
│       ├── test_main.py         # Root/health endpoints
│       ├── test_objects.py      # Object API tests
│       ├── test_types.py        # Type API tests
│       ├── test_links.py        # Link API tests
│       ├── test_permissions.py  # Permission API tests
│       ├── test_versioning.py   # Versioning API tests
│       └── test_attributes.py   # Attribute API tests
├── examples/                     # Usage examples
│   ├── __init__.py
│   └── basic_usage.py           # Basic model usage
├── main.py                      # Main entry point
├── server.py                    # API server script
├── pyproject.toml              # Project configuration
├── pytest.ini                  # Test configuration
├── README.md                   # Project documentation
├── LICENSE                     # MIT License
├── CONTRIBUTING.md             # Contributing guidelines
└── .gitignore                 # Git ignore rules
```

## 🧪 Testing Commands

### Basic Testing
```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with short traceback
uv run pytest --tb=short

# Run specific test file
uv run pytest tests/api/test_objects.py

# Run specific test class
uv run pytest tests/api/test_objects.py::TestObjectsAPI

# Run specific test method
uv run pytest tests/api/test_objects.py::TestObjectsAPI::test_create_object
```

### Test Categories
```bash
# Run API tests only
uv run pytest -m api

# Run unit tests only
uv run pytest -m unit

# Run integration tests only
uv run pytest -m integration

# Run slow tests only
uv run pytest -m slow
```

### Coverage Testing
```bash
# Run tests with coverage
uv run pytest --cov=dormatory

# Run tests with coverage and HTML report
uv run pytest --cov=dormatory --cov-report=html

# Run tests with coverage and XML report
uv run pytest --cov=dormatory --cov-report=xml

# Run tests with coverage and terminal report
uv run pytest --cov=dormatory --cov-report=term
```

### Test Debugging
```bash
# Run tests and stop on first failure
uv run pytest -x

# Run tests and show local variables on failure
uv run pytest -l

# Run tests with maximum verbosity
uv run pytest -vvv

# Run tests and show print statements
uv run pytest -s
```

## 🌐 API Development

### Starting the Server
```bash
# Start development server
python server.py

# Start with custom host/port
uv run uvicorn dormatory.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### API Endpoints

#### Main Endpoints
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation
- `GET /redoc` - Alternative API documentation

#### Objects API (`/api/v1/objects`)
- `POST /` - Create object
- `GET /{object_id}` - Get object by ID
- `GET /` - List objects with filtering
- `PUT /{object_id}` - Update object
- `DELETE /{object_id}` - Delete object
- `POST /bulk` - Bulk create objects
- `GET /{object_id}/children` - Get children
- `GET /{object_id}/parents` - Get parents
- `GET /{object_id}/hierarchy` - Get complete hierarchy

#### Types API (`/api/v1/types`)
- `POST /` - Create type
- `GET /{type_id}` - Get type by ID
- `GET /` - List types with filtering
- `PUT /{type_id}` - Update type
- `DELETE /{type_id}` - Delete type
- `POST /bulk` - Bulk create types
- `GET /{type_id}/objects` - Get objects by type

#### Links API (`/api/v1/links`)
- `POST /` - Create parent-child relationship
- `GET /{link_id}` - Get link by ID
- `GET /` - List links with filtering
- `PUT /{link_id}` - Update link
- `DELETE /{link_id}` - Delete link
- `POST /bulk` - Bulk create links
- `GET /parent/{parent_id}/children` - Get children by parent
- `GET /child/{child_id}/parents` - Get parents by child
- `GET /relationship/{r_name}` - Get links by relationship
- `POST /hierarchy` - Create complete hierarchy

#### Permissions API (`/api/v1/permissions`)
- `POST /` - Create permission
- `GET /{permission_id}` - Get permission by ID
- `GET /` - List permissions with filtering
- `PUT /{permission_id}` - Update permission
- `DELETE /{permission_id}` - Delete permission
- `POST /bulk` - Bulk create permissions
- `GET /object/{object_id}` - Get permissions by object
- `GET /user/{user}` - Get permissions by user
- `GET /check/{object_id}/{user}` - Check user permission

#### Versioning API (`/api/v1/versioning`)
- `POST /` - Create versioning record
- `GET /{versioning_id}` - Get versioning by ID
- `GET /` - List versioning with filtering
- `PUT /{versioning_id}` - Update versioning
- `DELETE /{versioning_id}` - Delete versioning
- `POST /bulk` - Bulk create versioning
- `GET /object/{object_id}` - Get versioning by object
- `GET /object/{object_id}/latest` - Get latest version
- `GET /object/{object_id}/version/{version}` - Get specific version
- `POST /object/{object_id}/version` - Create new version

#### Attributes API (`/api/v1/attributes`)
- `POST /` - Create attribute
- `GET /{attribute_id}` - Get attribute by ID
- `GET /` - List attributes with filtering
- `PUT /{attribute_id}` - Update attribute
- `DELETE /{attribute_id}` - Delete attribute
- `POST /bulk` - Bulk create attributes
- `GET /object/{object_id}` - Get attributes by object
- `GET /object/{object_id}/name/{name}` - Get attribute by name
- `GET /object/{object_id}/attributes` - Get attributes as map
- `POST /object/{object_id}/attributes` - Set multiple attributes
- `DELETE /object/{object_id}/name/{name}` - Delete attribute by name
- `GET /search` - Search attributes

## 🔧 Development Commands

### Package Management
```bash
# Add a new dependency
uv add package_name

# Add development dependency
uv add --dev package_name

# Update dependencies
uv sync

# Show dependency tree
uv tree
```

### Code Quality
```bash
# Run linting (if ruff is added)
uv run ruff check .

# Run formatting (if ruff is added)
uv run ruff format .

# Run type checking (if mypy is added)
uv run mypy dormatory/
```

### Database Operations
```bash
# Run the basic usage example
uv run python examples/basic_usage.py

# Create database tables
python -c "from dormatory.models.dormatory_model import create_tables, create_engine_and_session; engine, _ = create_engine_and_session(); create_tables(engine)"
```

## 📊 Current Status

### Test Status
- **82 API tests** - Currently failing (expected, endpoints not implemented)
- **10 main API tests** - Passing (root, health, docs endpoints)
- **Validation tests** - Properly testing request/response validation

### Implementation Status
- ✅ **Project Structure** - Complete
- ✅ **SQLAlchemy Models** - Complete
- ✅ **FastAPI Routes** - Stubs created
- ✅ **Test Suite** - Complete
- ❌ **API Implementation** - Not started
- ❌ **Database Integration** - Not started
- ❌ **Business Logic** - Not started

## 🐛 Troubleshooting

### Common Issues

#### Test Failures
- **Expected**: Most API tests currently fail (500 errors) since endpoints aren't implemented
- **Unexpected**: If you see 200 responses instead of 500, check endpoint implementation

#### Import Errors
```bash
# If you get import errors, make sure you're in the virtual environment
uv shell

# Or run commands with uv run
uv run python main.py
```

#### Database Issues
```bash
# If you get database errors, check the connection string
# Default is SQLite in-memory for tests
# For development, you might want to use a file-based SQLite
```

#### API Server Issues
```bash
# If the server won't start, check if port 8000 is in use
# You can change the port in server.py
# Or kill the process using port 8000
lsof -ti:8000 | xargs kill -9
```

## 📚 Next Steps

1. **Implement API Endpoints**: Start with basic CRUD operations
2. **Add Database Integration**: Connect models to actual database
3. **Add Business Logic**: Implement hierarchical data operations
4. **Add Authentication**: Implement user authentication and authorization
5. **Add Validation**: Enhance request/response validation
6. **Add Documentation**: Improve API documentation
7. **Add Integration Tests**: Test complete workflows
8. **Add Performance Tests**: Test with large datasets

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:
- Forking the repository
- Setting up development environment
- Code style guidelines
- Testing requirements
- Pull request process

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details. 