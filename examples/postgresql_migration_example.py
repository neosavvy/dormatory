#!/usr/bin/env python3
"""
PostgreSQL Migration Example for DORMATORY.

This example demonstrates how to use migrations with PostgreSQL.
You'll need a PostgreSQL server running to test this.
"""

import os
import subprocess
import sys


def setup_postgresql_example():
    """Set up PostgreSQL migration example."""
    print("PostgreSQL Migration Example")
    print("=" * 40)
    
    # Example PostgreSQL connection string
    postgres_url = "postgresql://username:password@localhost/dormatory"
    
    print(f"Example PostgreSQL URL: {postgres_url}")
    print("\nTo use PostgreSQL migrations:")
    print("1. Install PostgreSQL server")
    print("2. Create a database named 'dormatory'")
    print("3. Set the DATABASE_URL environment variable:")
    print(f"   export DATABASE_URL='{postgres_url}'")
    print("4. Run migrations:")
    print("   python manage_migrations.py upgrade")
    
    print("\nExample commands:")
    print("=" * 20)
    
    commands = [
        "# Set PostgreSQL URL",
        "export DATABASE_URL='postgresql://username:password@localhost/dormatory'",
        "",
        "# Create initial migration (if not exists)",
        "python manage_migrations.py create 'Initial PostgreSQL migration'",
        "",
        "# Apply migrations",
        "python manage_migrations.py upgrade",
        "",
        "# Check current migration",
        "python manage_migrations.py current",
        "",
        "# Show migration history",
        "python manage_migrations.py history",
    ]
    
    for cmd in commands:
        print(cmd)
    
    print("\nNote: Replace 'username', 'password', and 'localhost' with your actual PostgreSQL credentials.")


def test_postgresql_connection():
    """Test PostgreSQL connection if available."""
    postgres_url = os.getenv("DATABASE_URL")
    
    if postgres_url and postgres_url.startswith("postgresql"):
        print(f"\nTesting PostgreSQL connection with: {postgres_url}")
        
        try:
            # Test migration commands
            result = subprocess.run(
                ["python", "manage_migrations.py", "current"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print("✓ PostgreSQL migration test successful")
                print(f"Output: {result.stdout.strip()}")
            else:
                print("✗ PostgreSQL migration test failed")
                print(f"Error: {result.stderr}")
                
        except Exception as e:
            print(f"✗ Error testing PostgreSQL: {e}")
    else:
        print("\nNo PostgreSQL DATABASE_URL found.")
        print("Set DATABASE_URL to test PostgreSQL migrations.")


if __name__ == "__main__":
    setup_postgresql_example()
    test_postgresql_connection() 