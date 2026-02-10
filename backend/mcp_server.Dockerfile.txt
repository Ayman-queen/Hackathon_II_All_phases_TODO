# Dockerfile for MCP Server

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

# Copy only the necessary code
COPY app/core/ app/core/
COPY app/models/ app/models/
COPY mcp/ mcp/
COPY mcp_server/ mcp_server/

# Expose port 8001
EXPOSE 8001

# Start MCP server
CMD ["python", "mcp_server/server.py"]
