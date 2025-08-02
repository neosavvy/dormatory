# DORMATORY

A Python library for storing structured hierarchical data using a flat set of tables.

## Overview

DORMATORY provides an efficient way to store and query hierarchical data structures in flat database tables. This approach offers better performance and simpler querying compared to traditional nested data structures while maintaining the hierarchical relationships.

## Features

- Store hierarchical data in flat table structures
- Efficient querying of parent-child relationships
- Support for complex nested data structures
- Type-safe data handling
- Optimized for read and write operations

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

# Run tests (when implemented)
uv run pytest
```

## Project Structure

```
dormatory/
├── main.py              # Main entry point
├── pyproject.toml       # Project configuration
├── README.md           # This file
├── LICENSE             # MIT License
├── CONTRIBUTING.md     # Contributing guidelines
└── .gitignore         # Git ignore rules
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to fork the repository and contribute to the project.
