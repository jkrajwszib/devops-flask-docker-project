# =========================
# STAGE 1 — builder
# =========================
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies (build + Postgres headers)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Create venv for deterministic PATH across stages
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements first (better cache)
COPY app/requirements.txt .

# Install Python deps into venv
RUN /opt/venv/bin/pip install --upgrade pip \
 && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy application source + tests (tests only needed for test stage)
COPY app/src ./src
COPY app/tests ./tests
COPY app/migrations ./migrations
COPY app/seed ./seed


# =========================
# STAGE 2 — test
# =========================
FROM builder AS test

WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH"

# Environment for tests
ENV DATABASE_URL=postgresql+psycopg2://test:test@127.0.0.1:5432/testdb

# Run pytest — if tests fail, build fails
RUN /opt/venv/bin/python -m pytest -q


# =========================
# STAGE 3 — final
# =========================
FROM python:3.12-slim AS final

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Runtime deps only (Postgres client library)
RUN apt-get update && apt-get install -y \
    libpq5 \
 && rm -rf /var/lib/apt/lists/*

# Copy venv from builder (contains all Python deps including gunicorn)
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code only (no tests)
COPY app/src ./src

EXPOSE 8000

CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:8000", "src.app:create_app()"]