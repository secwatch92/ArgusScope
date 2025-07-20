# =================================================================
#  Base Stage - Common layer for both environments
# =================================================================
FROM python:3.12-slim AS base

# Install required OS packages
RUN apt-get update && apt-get install -y \
    unzip \
    wget \
    && rm -rf /var/lib/apt/lists/*

# --- Corrected: Install the latest secure version of subfinder (v2.8.0) ---
RUN wget https://github.com/projectdiscovery/subfinder/releases/download/v2.8.0/subfinder_2.8.0_linux_amd64.zip && \
    unzip subfinder_2.8.0_linux_amd64.zip && \
    mv subfinder /usr/local/bin/ && \
    rm subfinder_2.8.0_linux_amd64.zip

# Poetry Environment Configuration
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_VIRTUALENVS_IN_PROJECT=true

# Add the virtual environment's bin directory to the PATH
ENV VENV_PATH=/app/.venv
ENV PATH="$VENV_PATH/bin:$PATH"

WORKDIR /app
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock ./

# =================================================================
#  Test Stage - For running tests
# =================================================================
FROM base AS test

# Install all dependencies, including development packages
# Removing --no-root allows the project itself to be installed in editable mode
RUN poetry install
COPY . .
CMD ["pytest"]

# =================================================================
#  Production Stage - Optimized for deployment
# =================================================================
FROM base AS production

# Install only the main application dependencies
RUN poetry install --no-root --only main
COPY . .
EXPOSE 8000
CMD ["uvicorn", "argus_scope.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
