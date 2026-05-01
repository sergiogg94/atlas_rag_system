FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

# Configure UV for optimal performance in a containerized environment
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY pyproject.toml uv.lock* ./

# install python dependencies (only pord)
RUN uv sync --frozen --no-dev --no-install-project

# Copy code
COPY . .

# Intall project
RUN uv sync --frozen --no-dev

# Expose port
EXPOSE 8000

# Run app
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]