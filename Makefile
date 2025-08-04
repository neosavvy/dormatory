# DORMATORY Makefile
# Simple commands for development and testing

# Environment file to use (default: .env)
ENV_FILE ?= .env

# Load environment variables from file
ifneq (,$(wildcard $(ENV_FILE)))
    include $(ENV_FILE)
    export
endif

.PHONY: run-dev unit-test api-test serve-coverage install supabase-up supabase-down supabase-reset supabase-studio update-supabase-env migrate makemigration test test-cov clean

# Install dependencies and Supabase CLI
install:
	uv sync
	brew install supabase/tap/supabase
	supabase init

# Start all local dev services: Supabase, update env, migrate, backend
all:
	$(MAKE) supabase-up
	$(MAKE) update-supabase-env
	$(MAKE) migrate
	$(MAKE) run-dev

# Start Supabase local stack
supabase-up:
	supabase start

# Stop Supabase local stack
supabase-down:
	supabase stop

# Reset Supabase local stack (danger: wipes data)
supabase-reset:
	supabase stop && supabase start

# Open Supabase Studio in browser
supabase-studio:
	open http://localhost:54323

# Update .env with the local Supabase anon key and URL
update-supabase-env:
	$(MAKE) update-supabase-url-from-cli
	$(MAKE) update-anon-key-from-cli
	$(MAKE) update-supabase-local-db-url

update-supabase-url-from-cli:
	@URL=$$(supabase status | grep 'API URL:' | awk '{print $$3}') ; \
	if grep -q '^SUPABASE_URL=' .env ; then \
		sed -i -e "s|^SUPABASE_URL=.*|SUPABASE_URL=$${URL}|" .env ; \
	else \
		echo "SUPABASE_URL=$${URL}" >> .env ; \
	fi

update-anon-key-from-cli:
	@ANON_KEY=$$(supabase status | grep 'anon key:' | awk '{print $$3}') ; \
	if grep -q '^SUPABASE_ANON_KEY=' .env ; then \
		sed -i -e "s|^SUPABASE_ANON_KEY=.*|SUPABASE_ANON_KEY=$${ANON_KEY}|" .env ; \
	else \
		echo "SUPABASE_ANON_KEY=$${ANON_KEY}" >> .env ; \
	fi

update-supabase-local-db-url:
	@POSTGRES_HOST="localhost" ; \
	POSTGRES_PWD="postgres" ; \
	POSTGRES_PORT="54322" ; \
	if grep -q '^POSTGRES_HOST=' .env ; then \
		sed -i -e "s|^POSTGRES_HOST=.*|POSTGRES_HOST=$${POSTGRES_HOST}|" .env ; \
	else \
		echo "POSTGRES_HOST=$${POSTGRES_HOST}" >> .env ; \
	fi ; \
	if grep -q '^POSTGRES_PASSWORD=' .env ; then \
		sed -i -e "s|^POSTGRES_PASSWORD=.*|POSTGRES_PASSWORD=$${POSTGRES_PWD}|" .env ; \
	else \
		echo "POSTGRES_PASSWORD=$${POSTGRES_PWD}" >> .env ; \
	fi ; \
	if grep -q '^POSTGRES_PORT=' .env ; then \
		sed -i -e "s|^POSTGRES_PORT=.*|POSTGRES_PORT=$${POSTGRES_PORT}|" .env ; \
	else \
		echo "POSTGRES_PORT=$${POSTGRES_PORT}" >> .env ; \
	fi ; \
	echo "✅ Updated local DB values in .env"

# Run Alembic migrations
migrate:
	DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:54322/postgres uv run alembic upgrade head

# Create a new Alembic migration (usage: make makemigration m="message")
makemigration:
	DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:54322/postgres uv run alembic revision --autogenerate -m "$(m)"

# Run the development server
run-dev:
	DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:54322/postgres uv run uvicorn dormatory.api.main:app --reload --host 0.0.0.0 --port 8000

# Stop the FastAPI backend running on port 8000
stop-backend:
	@PID=$$(lsof -ti tcp:8000) ; \
	if [ -n "$$PID" ]; then \
		kill $$PID && echo "✅ Backend on port 8000 stopped (PID $$PID)"; \
	else \
		echo "No backend process found on port 8000."; \
	fi

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

# Run tests against Supabase
test-supabase:
	DATABASE_URL=postgresql://postgres:postgres@localhost:54322/dormatory uv run pytest -v

# Stop all services: backend, Supabase, and all Docker containers
stop-all:
	$(MAKE) stop-backend
	$(MAKE) supabase-down
	@docker stop $$(docker ps -q) 2>/dev/null || true

# Deploy to cloud
deploy-cloud:
	supabase db push
	@echo "✅ Database schema deployed to cloud"

# Get cloud project info
cloud-info:
	supabase status
	@if [ -n "$$SUPABASE_URL" ]; then \
		echo "Supabase URL: $$SUPABASE_URL"; \
	else \
		echo "SUPABASE_URL not set in .env file"; \
	fi

# Run migrations on cloud
migrate-cloud:
	@if [ -z "$$DATABASE_URL" ]; then \
		echo "Error: DATABASE_URL not set. Please set it in your .env file"; \
		exit 1; \
	fi
	uv run alembic upgrade head

# Test cloud connection
test-cloud:
	@if [ -z "$$SUPABASE_URL" ] || [ -z "$$SUPABASE_ANON_KEY" ]; then \
		echo "Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set in your .env file"; \
		exit 1; \
	fi
	@echo "Testing cloud connection..."
	@curl -s "$$SUPABASE_URL/rest/v1/" -H "apikey: $$SUPABASE_ANON_KEY" || echo "Connection test failed - check your API keys"

# Link to cloud project
link-cloud:
	supabase link --project-ref vustxkrprriqlgedxgvv
	@echo "✅ Linked to dormatory-dev cloud project"

# Environment management
env-local:
	@echo "Using local environment (.env)"
	@$(MAKE) --no-print-directory run-dev ENV_FILE=.env

env-dev:
	@echo "Using development environment (.env.dev)"
	@$(MAKE) --no-print-directory run-dev ENV_FILE=.env.dev

env-prod:
	@echo "Using production environment (.env.prod)"
	@$(MAKE) --no-print-directory run-dev ENV_FILE=.env.prod

# Show current environment
show-env:
	@echo "Current environment file: $(ENV_FILE)"
	@echo "DATABASE_URL: $$DATABASE_URL"
	@echo "SUPABASE_URL: $$SUPABASE_URL"
	@echo "ENVIRONMENT: $$ENVIRONMENT"

# Clean up generated files
clean:
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete 