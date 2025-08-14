# Use a Python image with uv pre-installed.
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS base

# Set environment variables.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install the project into `/app`.
WORKDIR /app

FROM base AS development

# Install the project's dependencies using the lockfile and settings.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Then, add the rest of the project source code and install it.
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Place executables in the environment at the front of the path.
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`.
ENTRYPOINT []

# Run the Django development server by default.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM base AS production

# Install production dependencies only.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Create non-root user for security.
RUN addgroup -g 1001 -S django && \
    adduser -S django -u 1001 -G django

# Copy source code and install project.
COPY --chown=django:django . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Create directories for static and media files.
RUN mkdir -p /app/static /app/media && \
    chown -R django:django /app

# Place executables in the environment at the front of the path.
ENV PATH="/app/.venv/bin:$PATH"

# Collect static files.
RUN python manage.py collectstatic --noinput

# Switch to non-root user.
USER django

# Reset the entrypoint, don't invoke `uv`.
ENTRYPOINT []

# Use gunicorn for production
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
