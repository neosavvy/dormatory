"""
DORMATORY - A Python library for storing structured hierarchical data using flat tables.
"""

from dormatory.models import Object, Type, Link, Permissions, Versioning, Attributes


def main():
    """Main entry point for DORMATORY."""
    print("Welcome to DORMATORY!")
    print("A Python library for storing structured hierarchical data using flat tables.")
    print()
    print("Available Models:")
    print(f"  - {Object.__name__}: Core entities in the hierarchical structure")
    print(f"  - {Type.__name__}: Categories/types for objects")
    print(f"  - {Link.__name__}: Parent-child relationships")
    print(f"  - {Permissions.__name__}: Access control")
    print(f"  - {Versioning.__name__}: Version history")
    print(f"  - {Attributes.__name__}: Flexible key-value attributes")
    print()
    print("Available Commands:")
    print("  - Run example: python examples/basic_usage.py")
    print("  - Start API server: python server.py")
    print("  - View API docs: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
