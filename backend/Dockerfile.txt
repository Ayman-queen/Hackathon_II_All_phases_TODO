# T-401: Refactor Dockerfiles into multi-stage production builds.

# ---- Builder Stage ----
FROM python:3.13 as builder

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtual environment
RUN uv venv && uv sync --no-cache

# ---- Final Stage ----
FROM python:3.13-slim

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /.venv

# Set path to use venv
ENV PATH="/app/.venv/bin:$PATH"

# Install system dependencies for runtime
RUN apt-get update && apt-get install -y \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Expose port 8000
EXPOSE 8000

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
