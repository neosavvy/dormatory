# Environment Setup for DORMATORY

## Security Best Practices

✅ **No hardcoded secrets in Makefile** - All sensitive data now comes from environment files
✅ **Environment files ignored by git** - `.env*` files are in `.gitignore`
✅ **Multiple environment support** - Separate files for local, dev, and production

## Environment Files

### Available Files
- `env.example` - Template showing all required variables
- `.env` - Local development (default)
- `.env.dev` - Cloud development environment
- `.env.prod` - Production environment

### Creating Environment Files

1. **Copy the template**:
   ```bash
   cp env.example .env
   ```

2. **Edit the file** and uncomment the section you need:
   ```bash
   # For local development
   DATABASE_URL=sqlite:///dormatory.db
   
   # For cloud development
   # DATABASE_URL=postgresql://postgres:password@db.project-ref.supabase.co:5432/postgres
   # SUPABASE_URL=https://project-ref.supabase.co
   # SUPABASE_ANON_KEY=your-anon-key
   ```

## Using Different Environments

### Local Development (SQLite)
```bash
make run-dev                    # Uses .env (default)
make env-local                  # Explicitly use .env
```

### Local Supabase Development
```bash
# Create .env.dev with local Supabase settings
cp env.example .env.dev
# Edit .env.dev to uncomment local Supabase section

make env-dev                    # Use .env.dev
```

### Cloud Development
```bash
# Create .env.dev with cloud settings
cp env.example .env.dev
# Edit .env.dev with your cloud project details

make env-dev                    # Use .env.dev
```

### Production
```bash
# Create .env.prod with production settings
cp env.example .env.prod
# Edit .env.prod with production details

make env-prod                   # Use .env.prod
```

## Environment Variables

### Required Variables
- `DATABASE_URL` - Database connection string
- `SUPABASE_URL` - Supabase API URL (for cloud environments)
- `SUPABASE_ANON_KEY` - Public API key (for cloud environments)
- `SUPABASE_SERVICE_ROLE_KEY` - Secret API key (for cloud environments)

### Optional Variables
- `ENVIRONMENT` - Environment name (development, production)
- `DEBUG` - Enable debug mode (true/false)
- `LOG_LEVEL` - Logging level (INFO, DEBUG, etc.)

## Commands

### Environment Management
```bash
make show-env                  # Show current environment variables
make env-local                 # Run with .env
make env-dev                   # Run with .env.dev
make env-prod                  # Run with .env.prod
```

### Cloud Deployment
```bash
make link-cloud                # Link to cloud project
make deploy-cloud              # Deploy schema to cloud
make migrate-cloud             # Run migrations on cloud (uses DATABASE_URL)
make test-cloud                # Test cloud connection (uses SUPABASE_URL and SUPABASE_ANON_KEY)
```

## Security Checklist

- [ ] No secrets in Makefile
- [ ] Environment files in .gitignore
- [ ] Different files for different environments
- [ ] Template file shows required variables
- [ ] Commands validate required variables exist

## Example Environment Files

### .env (Local SQLite)
```bash
DATABASE_URL=sqlite:///dormatory.db
ENVIRONMENT=development
DEBUG=true
```

### .env.dev (Cloud Development)
```bash
DATABASE_URL=postgresql://postgres:password@db.project-ref.supabase.co:5432/postgres
SUPABASE_URL=https://project-ref.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
ENVIRONMENT=development
DEBUG=true
```

### .env.prod (Production)
```bash
DATABASE_URL=postgresql://postgres:secure-password@db.prod-project.supabase.co:5432/postgres
SUPABASE_URL=https://prod-project.supabase.co
SUPABASE_ANON_KEY=your-production-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-production-service-role-key
ENVIRONMENT=production
DEBUG=false
```

## Troubleshooting

### "Error: DATABASE_URL not set"
- Check that your environment file exists
- Verify the variable is not commented out
- Use `make show-env` to see current variables

### "Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set"
- Ensure you're using the correct environment file
- Check that the variables are not commented out
- Verify the values are correct for your environment

### Environment not loading
- Check file permissions on environment files
- Verify the file exists and has correct syntax
- Use `make show-env` to debug 