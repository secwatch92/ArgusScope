# New and optimized Dockerfile for use with Poetry

# --- Base Image ---
FROM python:3.12-slim

# --- Environment Settings ---
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Tell Poetry not to create a virtual environment inside the project directory
# and configure it for a non-interactive environment.
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

# --- Working Directory ---
WORKDIR /app

# --- Install Poetry ---
RUN pip install poetry

# --- Install Dependencies ---
# First, copy only the dependency files to leverage Docker's layer cache.
# This step is only re-run when pyproject.toml or poetry.lock changes.
COPY pyproject.toml poetry.lock ./

# Install main dependencies (without development packages like pytest).
RUN poetry install --no-root --only main

# --- Copy Project Source Code ---
COPY . .

# --- Define Port and Execution Command ---
EXPOSE 8000

# Run the application using Poetry.
# The --reload flag enables hot-reloading for development.
CMD ["poetry", "run", "uvicorn", "argus_scope.api.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
