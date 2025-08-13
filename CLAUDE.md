# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django task management web application using ULID for primary keys and PostgreSQL/SQLite databases. The project follows standard Django conventions with a custom base model that handles ULID generation and automatic timestamping.

## Commands

### Development Setup
- `just install` - Install dependencies using uv
- `just dev-init` - Complete development setup (install, build, up, migrate, create superuser)

### Code Quality
- `just lint` - Run ruff linter with import sorting
- `just format` - Format code with ruff
- `just fix` - Auto-fix linting issues and format code

### Docker Development
- `just dev-build` - Build Docker containers
- `just dev-up` - Start development containers
- `just dev-down` - Stop development containers
- `just dev-logs` - Follow container logs
- `just dev-migrate` - Run Django migrations in container
- `just dev-makemigrations` - Create Django migrations in container
- `just dev-test` - Run Django tests in container
- `just dev-shell` - Access Django shell in container
- `just dev-psql` - Access PostgreSQL shell

### Testing
- `just dev-test` - Run tests via Docker
- `python manage.py test` - Run tests directly (if running locally)

### Database
- Uses PostgreSQL in Docker, SQLite as fallback
- Custom ULID field for primary keys instead of auto-incrementing integers
- Database connection via `DATABASE_URL` environment variable

## Architecture

### Core Components
- **BaseModel** (`utils/models.py`): Abstract base with ULID primary key and automatic timestamps
- **ULIDField** (`utils/fields.py`): Custom Django field for ULID generation
- **Task Model** (`tasks/models.py`): Main domain model with priority, status, due dates

### Project Structure
- `config/` - Django project settings and configuration
- `tasks/` - Main application with models, views, templates
- `utils/` - Shared utilities (BaseModel, ULIDField)
- `static/` - Static assets
- Templates located in both `config/templates/` and `tasks/templates/`

### Key Patterns
- Uses `environs` for environment variable handling with `.env.dev` file
- All models inherit from `BaseModel` for consistent ULID PKs and timestamps
- Class-based views following Django conventions
- Template structure supports both global and app-specific templates

### Environment Configuration
- Settings use environment variables with sensible defaults
- Debug mode controlled by `DEBUG` env var
- Database URL configurable via `DATABASE_URL`
- Static/media file paths configurable via environment variables
