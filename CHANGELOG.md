# Changelog

All notable changes to the DORMATORY project will be documented in this file.

## [Unreleased] - 2025-08-02

### Added
- **GitHub Pages Coverage Reports**: Automatic deployment of test coverage reports to https://neosavvy.github.io/dormatory/
- **GitHub Actions CI/CD**: Comprehensive test automation with coverage reporting
- **Makefile**: Development automation with commands for testing, running dev server, and serving coverage
- **Alembic Migrations**: Database migration support for both SQLite and PostgreSQL
- **Database Configuration**: Flexible database setup with environment-based configuration
- **Coverage Badges**: README badges for test status and coverage reports

### Changed
- **API Validation**: Enhanced Pydantic models with proper validation (min_length for required fields)
- **Test Infrastructure**: Improved test suite with file-based SQLite databases to fix threading issues
- **Database Models**: Updated to support flexible database configuration
- **API Endpoints**: Added root and health endpoints for better API discoverability

### Fixed
- **SQLite Threading Issues**: Resolved database connection problems in test suite
- **GitHub Actions**: Updated to use latest action versions (v4) and fixed deprecated warnings
- **Environment Configuration**: Added required GitHub Pages environment for proper deployment
- **Test Failures**: Fixed API tests to dynamically create test data instead of using hardcoded values
- **Coverage Report Hosting**: Resolved deployment issues and consolidated multiple workflows into single solution

### Technical Improvements
- **Workflow Consolidation**: Reduced from 3 conflicting workflows to 1 clean solution
- **Database Flexibility**: Support for both SQLite (development) and PostgreSQL (production)
- **Migration Management**: Alembic setup with proper versioning and rollback capabilities
- **Test Coverage**: Comprehensive test suite with 169 passing tests
- **API Documentation**: Better endpoint organization and validation

## [0.1.0] - 2025-08-02

### Added
- **Core DORMATORY Library**: Python library for storing structured hierarchical data
- **SQLAlchemy Models**: Object, Type, Link, Permission, and Versioning models
- **FastAPI Application**: RESTful API with comprehensive endpoints
- **Hierarchical Data Support**: Parent-child relationships with flexible linking
- **Type System**: UUID-based type identification for objects
- **Permission System**: User-based access control framework
- **Versioning System**: Object version tracking and management
- **Database Schema**: Complete database design with proper relationships
- **Test Suite**: Comprehensive unit and API tests (169 tests total)

### API Endpoints Implemented
- **Types API**: CRUD operations for object types
- **Objects API**: CRUD operations with hierarchy support (children, parents, hierarchy tree)
- **Links API**: Relationship management between objects
- **Permissions API**: User permission management (9 endpoints)
- **Versioning API**: Object version tracking (10 endpoints)

### Development Tools
- **uv Package Management**: Modern Python dependency management
- **pytest Testing**: Comprehensive test framework with coverage reporting
- **Alembic Migrations**: Database schema versioning
- **GitHub Actions**: Automated testing and deployment
- **Coverage Reports**: HTML coverage reports with GitHub Pages hosting

### Documentation
- **README.md**: Project overview with badges and usage examples
- **MIGRATIONS.md**: Database migration documentation
- **HELP.md**: Development and testing guidelines
- **CONTRIBUTING.md**: Contribution guidelines
- **Makefile**: Development automation commands

---

## Version History

### Recent Commits
- `84a2afd` - fix: add environment configuration for GitHub Pages deployment
- `fb59c68` - fix: clean up workflows and ensure GitHub Pages deployment  
- `61b720b` - feat: consolidate into single test and deploy workflow
- `a106f4f` - fix: update coverage pages workflow to use docs directory
- `6ae412a` - feat: add GitHub Pages coverage report hosting
- `a82e857` - fix: update GitHub Actions to use latest versions
- `328d893` - ci: add GitHub Actions for test automation and coverage reporting
- `7c5e36b` - feat(dev): add Makefile for common development tasks
- `96f7c41` - feat(api): implement Objects API hierarchy endpoints
- `d5e60fc` - feat(api): complete Types API implementation and fix test suite

---

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file. 