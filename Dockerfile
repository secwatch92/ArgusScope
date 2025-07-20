# =================================================================
#  Base Stage – Common base layer
# =================================================================
FROM python:3.12-slim AS base

# Install required OS tools to download and extract subfinder
RUN apt-get update && apt-get install -y \
    unzip \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install the subfinder tool from GitHub
RUN wget https://github.com/projectdiscovery/subfinder/releases/download/v2.6.5/subfinder_2.6.5_linux_amd64.zip && \
    unzip subfinder_2.6.5_linux_amd64.zip && \
    mv subfinder /usr/local/bin/ && \
    rm subfinder_2.6.5_linux_amd64.zip

# Adjusted environment settings for Poetry integration
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_VIRTUALENVS_IN_PROJECT=true

# --- Key change: Add the virtual environment path to PATH ---
# This ensures that all tools installed by Poetry are directly accessible.
ENV VENV_PATH=/app/.venv
ENV PATH="$VENV_PATH/bin:$PATH"

WORKDIR /app
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock ./

# =================================================================
#  Test Stage – Testing-specific layer
# =================================================================
FROM base AS test

# Install all dependencies in the project's virtual environment
RUN poetry install --no-root
COPY . .
# Now we can run the command directly
CMD ["pytest"]

# =================================================================
#  Production Stage – Final and optimized layer
# =================================================================
FROM base AS production

# Install only the main dependencies in the project's virtual environment
RUN poetry install --no-root --only main
COPY . .
EXPOSE 8000
# Now we can run uvicorn directly
CMD ["uvicorn", "argus_scope.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
