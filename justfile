default:
    just --list --unsorted

install:
    uv sync

update:
    uv lock --upgrade

generate-secret:
    @uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

lint:
    uv run ruff check --extend-select I

format:
    uv run ruff format

fix:
    uv run ruff check --extend-select I --fix
    uv run ruff format

clean:
    rm -rf .ruff_cache
    rm -rf .pytest_cache
    fd -I __pycache__ --type d --prune -x rm -r
    rm -rf db.sqlite3

# Docker development commands:

dev-init:
    just install
    just dev-build
    just dev-up
    just dev-makemigrations
    just dev-migrate
    just dev-createsuperuser

dev-build:
    docker-compose build

dev-up:
    docker-compose up -d

dev-down:
    docker-compose down

dev-logs:
    docker-compose logs -f

dev-shell:
    docker-compose exec web python manage.py shell

dev-migrate:
    docker-compose exec web python manage.py migrate

dev-makemigrations:
    docker-compose exec web python manage.py makemigrations

dev-createsuperuser:
    docker-compose exec web python manage.py createsuperuser --noinput

dev-collectstatic:
    docker-compose exec web python manage.py collectstatic --noinput

dev-test:
    docker-compose exec web python manage.py test

dev-restart:
    docker-compose restart

[confirm]
dev-clean:
    docker-compose down -v
    docker system prune -f

dev-psql:
    docker-compose exec db psql -U blog

dev-status:
    docker-compose ps

# Docker production commands:

prod-build:
    docker-compose -f docker-compose.prod.yml build --no-cache

prod-up:
    docker-compose -f docker-compose.prod.yml up -d

prod-down:
    docker-compose -f docker-compose.prod.yml down

prod-logs:
    docker-compose -f docker-compose.prod.yml logs -f

prod-shell:
    docker-compose -f docker-compose.prod.yml exec web python manage.py shell

prod-migrate:
    docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

prod-restart:
    docker-compose -f docker-compose.prod.yml restart

prod-psql:
    docker-compose -f docker-compose.prod.yml exec db psql -U blog

prod-status:
    docker-compose -f docker-compose.prod.yml ps
