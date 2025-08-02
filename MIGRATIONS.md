# DORMATORY Database Migrations

This document explains how to use Alembic migrations in the DORMATORY project for both SQLite and PostgreSQL databases.

## Overview

The DORMATORY project uses Alembic for database migrations, supporting both SQLite (development) and PostgreSQL (production) databases. The migration system is configured to automatically detect the database type and apply appropriate settings.

## Setup

### Prerequisites

1. Install dependencies:
   ```bash
   pip install -e .
   ```

2. Initialize Alembic (first time only):
   ```bash
   python manage_migrations.py init
   ```

## Database Configuration

### Environment Variables

Set the `DATABASE_URL` environment variable to switch between databases:

- **SQLite (default)**: `sqlite:///dormatory.db`
- **PostgreSQL**: `postgresql://username:password@localhost/database_name`

### Examples

```bash
# Use SQLite (default)
export DATABASE_URL=sqlite:///dormatory.db

# Use PostgreSQL
export DATABASE_URL=postgresql://user:pass@localhost/dormatory

# Use PostgreSQL with SSL
export DATABASE_URL=postgresql://user:pass@localhost/dormatory?sslmode=require
```

## Migration Commands

### Using the Management Script

The `manage_migrations.py` script provides convenient commands:

```bash
# Create a new migration
python manage_migrations.py create "Add user table"

# Apply all migrations
python manage_migrations.py upgrade

# Apply migrations to specific revision
python manage_migrations.py upgrade head

# Downgrade one migration
python manage_migrations.py downgrade

# Downgrade to specific revision
python manage_migrations.py downgrade 001

# Show current migration
python manage_migrations.py current

# Show migration history
python manage_migrations.py history

# Stamp database with revision (without running)
python manage_migrations.py stamp head

# Show migration details
python manage_migrations.py show 001
```

### Using Alembic Directly

You can also use Alembic commands directly:

```bash
# Create migration
alembic revision --autogenerate -m "Add user table"

# Apply migrations
alembic upgrade head

# Downgrade
alembic downgrade -1

# Show current
alembic current

# Show history
alembic history
```

## Migration Workflow

### Development Workflow

1. **Create a new migration**:
   ```bash
   python manage_migrations.py create "Description of changes"
   ```

2. **Review the generated migration**:
   - Check the generated file in `alembic/versions/`
   - Modify if needed (add custom logic, data migrations, etc.)

3. **Apply the migration**:
   ```bash
   python manage_migrations.py upgrade
   ```

4. **Test your changes**:
   - Run your application
   - Run tests to ensure everything works

### Production Deployment

1. **Set the production database URL**:
   ```bash
   export DATABASE_URL=postgresql://user:pass@localhost/dormatory
   ```

2. **Apply migrations**:
   ```bash
   python manage_migrations.py upgrade
   ```

3. **Verify the deployment**:
   ```bash
   python manage_migrations.py current
   ```

## Database-Specific Considerations

### SQLite

- **Pros**: Simple, no server required, good for development
- **Cons**: Limited concurrent access, no advanced features
- **Use case**: Development, testing, small applications

### PostgreSQL

- **Pros**: Full ACID compliance, advanced features, better performance
- **Cons**: Requires server setup, more complex configuration
- **Use case**: Production, high-traffic applications

### Migration Differences

The migration system automatically handles database-specific differences:

- **UUID fields**: Automatically use PostgreSQL UUID type when available
- **Indexes**: PostgreSQL-specific index types when needed
- **Constraints**: Database-specific constraint syntax
- **Data types**: Appropriate types for each database

## Troubleshooting

### Common Issues

1. **Migration conflicts**:
   ```bash
   # Reset to a known good state
   python manage_migrations.py downgrade 001
   python manage_migrations.py upgrade
   ```

2. **Database connection issues**:
   - Check `DATABASE_URL` environment variable
   - Verify database server is running (PostgreSQL)
   - Check network connectivity

3. **Model import errors**:
   - Ensure all models are imported in `alembic/env.py`
   - Check for circular imports

### Debugging

1. **Enable verbose output**:
   ```bash
   alembic upgrade head --verbose
   ```

2. **Check migration status**:
   ```bash
   python manage_migrations.py current
   python manage_migrations.py history
   ```

3. **Inspect database schema**:
   ```bash
   # SQLite
   sqlite3 dormatory.db ".schema"
   
   # PostgreSQL
   psql -d your_database -c "\dt"
   ```

## Best Practices

1. **Always review generated migrations** before applying
2. **Test migrations** on a copy of production data
3. **Use descriptive migration messages**
4. **Keep migrations small and focused**
5. **Backup your database** before applying migrations
6. **Use version control** for migration files

## File Structure

```
dormatory/
├── alembic/
│   ├── versions/          # Migration files
│   ├── env.py            # Alembic environment
│   └── script.py.mako    # Migration template
├── alembic.ini           # Alembic configuration
├── manage_migrations.py  # Migration management script
└── MIGRATIONS.md         # This file
```

## Examples

### Creating a New Table

1. Add the model to `dormatory/models/dormatory_model.py`
2. Create migration:
   ```bash
   python manage_migrations.py create "Add user preferences table"
   ```
3. Apply migration:
   ```bash
   python manage_migrations.py upgrade
   ```

### Adding a Column

1. Modify the model in `dormatory/models/dormatory_model.py`
2. Create migration:
   ```bash
   python manage_migrations.py create "Add email column to users"
   ```
3. Apply migration:
   ```bash
   python manage_migrations.py upgrade
   ```

### Data Migration

1. Create migration:
   ```bash
   python manage_migrations.py create "Migrate user data"
   ```
2. Edit the generated migration file to add data migration logic
3. Apply migration:
   ```bash
   python manage_migrations.py upgrade
   ```

## Support

For issues with migrations:

1. Check the troubleshooting section above
2. Review Alembic documentation: https://alembic.sqlalchemy.org/
3. Check the migration files in `alembic/versions/`
4. Verify database connectivity and configuration 