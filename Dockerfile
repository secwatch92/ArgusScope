# =================================================================
#  Base Stage - لایه پایه مشترک
# =================================================================
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./

# =================================================================
#  Test Stage - لایه مخصوص تست (با تمام وابستگی‌ها)
# =================================================================
FROM base AS test

# نصب تمام وابستگی‌ها (اصلی + توسعه)
RUN poetry install --no-root
COPY . .

# تعریف دستور پیش‌فرض برای این لایه (اجرای تست‌ها)
CMD ["poetry", "run", "pytest"]


# =================================================================
#  Production Stage - لایه نهایی و بهینه (فقط وابستگی‌های اصلی)
# =================================================================
FROM base AS production

# نصب فقط وابستگی‌های اصلی
RUN poetry install --no-root --only main
COPY . .

EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "argus_scope.api.server:app", "--host", "0.0.0.0", "--port", "8000"]