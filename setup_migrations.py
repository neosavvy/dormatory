#!/usr/bin/env python3
"""
Migration Setup Script for DORMATORY.

This script helps set up and initialize the migration system.
"""

import os
import sys
import subprocess
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are installed."""
    print("Checking dependencies...")
    
    try:
        import alembic
        print("✓ Alembic is installed")
    except ImportError:
        print("✗ Alembic is not installed")
        print("Run: pip install alembic")
        return False
    
    try:
        import sqlalchemy
        print("✓ SQLAlchemy is installed")
    except ImportError:
        print("✗ SQLAlchemy is not installed")
        print("Run: pip install sqlalchemy")
        return False
    
    try:
        import psycopg2
        print("✓ PostgreSQL driver (psycopg2) is installed")
    except ImportError:
        print("⚠ PostgreSQL driver not installed (optional)")
        print("Run: pip install psycopg2-binary")
    
    return True


def check_alembic_config():
    """Check if Alembic is properly configured."""
    print("\nChecking Alembic configuration...")
    
    required_files = [
        "alembic.ini",
        "alembic/env.py",
        "alembic/script.py.mako",
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            return False
    
    return True


def check_migration_files():
    """Check for existing migration files."""
    print("\nChecking migration files...")
    
    versions_dir = Path("alembic/versions")
    if versions_dir.exists():
        migration_files = list(versions_dir.glob("*.py"))
        if migration_files:
            print(f"✓ Found {len(migration_files)} migration file(s):")
            for file in migration_files:
                print(f"  - {file.name}")
        else:
            print("⚠ No migration files found")
    else:
        print("✗ alembic/versions directory missing")
        return False
    
    return True


def show_database_info():
    """Show current database configuration."""
    print("\nCurrent database configuration:")
    print("=" * 40)
    
    database_url = os.getenv("DATABASE_URL", "sqlite:///dormatory.db")
    print(f"Database URL: {database_url}")
    
    if database_url.startswith("sqlite"):
        print("Database Type: SQLite (Development)")
        print("Database File: dormatory.db")
    elif database_url.startswith("postgresql"):
        print("Database Type: PostgreSQL (Production)")
    else:
        print("Database Type: Unknown")
    
    print(f"\nTo change database, set DATABASE_URL environment variable:")
    print("  SQLite: export DATABASE_URL=sqlite:///dormatory.db")
    print("  PostgreSQL: export DATABASE_URL=postgresql://user:pass@localhost/dormatory")


def show_usage_examples():
    """Show usage examples."""
    print("\nMigration Usage Examples:")
    print("=" * 30)
    
    examples = [
        ("Create a new migration", "python manage_migrations.py create \"Add user table\""),
        ("Apply all migrations", "python manage_migrations.py upgrade"),
        ("Apply to specific revision", "python manage_migrations.py upgrade head"),
        ("Downgrade one migration", "python manage_migrations.py downgrade"),
        ("Show current migration", "python manage_migrations.py current"),
        ("Show migration history", "python manage_migrations.py history"),
        ("Show migration details", "python manage_migrations.py show <revision>"),
    ]
    
    for description, command in examples:
        print(f"{description}:")
        print(f"  {command}")
        print()


def test_migration_system():
    """Test the migration system."""
    print("\nTesting migration system...")
    
    try:
        # Test current migration
        result = subprocess.run(
            ["python", "manage_migrations.py", "current"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✓ Migration system is working")
            print(f"Current migration: {result.stdout.strip()}")
        else:
            print("✗ Migration system test failed")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Error testing migration system: {e}")
        return False
    
    return True


def main():
    """Main setup function."""
    print("DORMATORY Migration Setup")
    print("=" * 30)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependencies check failed!")
        return 1
    
    # Check configuration
    if not check_alembic_config():
        print("\n❌ Alembic configuration check failed!")
        return 1
    
    # Check migration files
    check_migration_files()
    
    # Show database info
    show_database_info()
    
    # Test migration system
    if not test_migration_system():
        print("\n❌ Migration system test failed!")
        return 1
    
    # Show usage examples
    show_usage_examples()
    
    print("✅ Migration setup completed successfully!")
    print("\nNext steps:")
    print("1. Review the migration files in alembic/versions/")
    print("2. Apply migrations: python manage_migrations.py upgrade")
    print("3. Test your application")
    print("4. For PostgreSQL, set DATABASE_URL and run migrations")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 