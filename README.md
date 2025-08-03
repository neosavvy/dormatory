# DORMATORY

[![Tests](https://github.com/neosavvy/dormatory/workflows/Test%20Suite/badge.svg)](https://github.com/neosavvy/dormatory/actions)
[![Coverage](https://img.shields.io/badge/coverage-169%20tests%20passing-brightgreen)](https://github.com/neosavvy/dormatory/actions)
[![Coverage Report](https://img.shields.io/badge/coverage%20report-view%20online-blue)](https://neosavvy.github.io/dormatory/)

A Python library for storing structured hierarchical data using a flat set of tables.

## Overview

DORMATORY provides an efficient way to store and query hierarchical data structures in flat database tables. This approach offers better performance and simpler querying compared to traditional nested data structures while maintaining the hierarchical relationships.

## Features

- Store hierarchical data in flat table structures
- Efficient querying of parent-child relationships
- Support for complex nested data structures
- Type-safe data handling
- Optimized for read and write operations
- Comprehensive FastAPI REST API
- Full test suite with unit and integration tests

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Clone the repository
git clone <repository-url>
cd dormatory

# Install dependencies
uv sync
```

## Development

```bash
# Activate the virtual environment
uv shell

# Run the project
python main.py

# Start the API server
python server.py

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=dormatory

# Run specific test categories
uv run pytest -m api          # API tests only
uv run pytest -m unit         # Unit tests only
uv run pytest -m integration  # Integration tests only
```

## API Documentation

Once the server is running, you can access:

- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Project Structure

```
dormatory/
├── dormatory/
│   ├── models/              # SQLAlchemy models
│   └── api/                 # FastAPI application
│       ├── routes/          # API route modules
│       └── main.py          # FastAPI app configuration
├── tests/                   # Test suite
│   ├── api/                 # API endpoint tests
│   └── conftest.py          # Test configuration
├── examples/                # Usage examples
├── main.py                  # Main entry point
├── server.py                # API server script
├── pyproject.toml           # Project configuration
├── pytest.ini              # Test configuration
├── README.md               # This file
├── LICENSE                 # MIT License
├── CONTRIBUTING.md         # Contributing guidelines
└── .gitignore             # Git ignore rules
```

## Testing

The project includes a comprehensive test suite:

### Test Categories
- **API Tests**: FastAPI endpoint validation
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end functionality testing

### Running Tests
```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/api/test_objects.py

# Run tests with coverage
uv run pytest --cov=dormatory --cov-report=html
```

### Test Status
- **82 API tests** - Currently failing (expected, endpoints not implemented)
- **10 main API tests** - Passing (root, health, docs endpoints)
- **Validation tests** - Properly testing request/response validation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to fork the repository and contribute to the project.
