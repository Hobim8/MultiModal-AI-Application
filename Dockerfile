# Use official Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install UV
RUN pip install uv

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy the rest of the project
COPY . .

# Expose the port
EXPOSE 8000

# Start the server
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]