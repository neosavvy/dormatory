# DORMATORY Makefile
# Simple commands for development and testing

.PHONY: run-dev unit-test api-test serve-coverage

# Run the development server
run-dev:
	uv run uvicorn dormatory.api.main:app --reload --host 0.0.0.0 --port 8000

# Run unit tests only
unit-test:
	uv run pytest tests/unit/ -v

# Run API tests only
api-test:
	uv run pytest tests/api/ -v

# Serve coverage report
serve-coverage:
	python -m http.server 8080 --directory htmlcov

# Run all tests
test:
	uv run pytest -v

# Run tests with coverage
test-cov:
	uv run pytest --cov=dormatory --cov-report=html -v

# Clean up generated files
clean:
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete 