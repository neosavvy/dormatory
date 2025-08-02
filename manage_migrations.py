#!/usr/bin/env python3
"""
Migration management script for DORMATORY.

This script provides convenient commands for managing database migrations
for both SQLite and PostgreSQL databases.
"""

import os
import sys
import subprocess
from typing import Optional


def run_command(command: str, env: Optional[dict] = None) -> int:
    """
    Run a shell command and return the exit code.
    
    Args:
        command: Command to run
        env: Environment variables to set
        
    Returns:
        Exit code
    """
    if env:
        # Merge with current environment
        full_env = os.environ.copy()
        full_env.update(env)
    else:
        full_env = None
    
    result = subprocess.run(command, shell=True, env=full_env)
    return result.returncode


def show_help():
    """Show help information."""
    print("""
DORMATORY Migration Management Script

Usage: python manage_migrations.py <command> [options]

Commands:
    init                    Initialize Alembic (first time setup)
    create <message>        Create a new migration
    upgrade [revision]      Apply migrations (default: head)
    downgrade [revision]    Downgrade migrations (default: -1)
    current                 Show current migration
    history                 Show migration history
    stamp <revision>        Stamp database with revision (without running)
    show <revision>         Show migration details
    
Database Configuration:
    Set DATABASE_URL environment variable to switch databases:
    
    SQLite (default):      export DATABASE_URL=sqlite:///dormatory.db
    PostgreSQL:            export DATABASE_URL=postgresql://user:pass@localhost/dormatory
    
Examples:
    python manage_migrations.py init
    python manage_migrations.py create "Add user table"
    python manage_migrations.py upgrade
    python manage_migrations.py upgrade head
    python manage_migrations.py downgrade -1
    DATABASE_URL=postgresql://user:pass@localhost/dormatory python manage_migrations.py upgrade
    """)


def main():
    """Main function."""
    if len(sys.argv) < 2:
        show_help()
        return 1
    
    command = sys.argv[1]
    
    if command == "help" or command == "--help" or command == "-h":
        show_help()
        return 0
    
    if command == "init":
        print("Initializing Alembic...")
        return run_command("alembic init alembic")
    
    elif command == "create":
        if len(sys.argv) < 3:
            print("Error: Message required for create command")
            print("Usage: python manage_migrations.py create \"Your message\"")
            return 1
        
        message = sys.argv[2]
        print(f"Creating migration: {message}")
        return run_command(f'alembic revision --autogenerate -m "{message}"')
    
    elif command == "upgrade":
        revision = sys.argv[2] if len(sys.argv) > 2 else "head"
        print(f"Upgrading to revision: {revision}")
        return run_command(f"alembic upgrade {revision}")
    
    elif command == "downgrade":
        revision = sys.argv[2] if len(sys.argv) > 2 else "-1"
        print(f"Downgrading to revision: {revision}")
        return run_command(f"alembic downgrade {revision}")
    
    elif command == "current":
        print("Current migration:")
        return run_command("alembic current")
    
    elif command == "history":
        print("Migration history:")
        return run_command("alembic history")
    
    elif command == "stamp":
        if len(sys.argv) < 3:
            print("Error: Revision required for stamp command")
            print("Usage: python manage_migrations.py stamp <revision>")
            return 1
        
        revision = sys.argv[2]
        print(f"Stamping database with revision: {revision}")
        return run_command(f"alembic stamp {revision}")
    
    elif command == "show":
        if len(sys.argv) < 3:
            print("Error: Revision required for show command")
            print("Usage: python manage_migrations.py show <revision>")
            return 1
        
        revision = sys.argv[2]
        print(f"Showing migration: {revision}")
        return run_command(f"alembic show {revision}")
    
    else:
        print(f"Unknown command: {command}")
        show_help()
        return 1


if __name__ == "__main__":
    sys.exit(main()) 