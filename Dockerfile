FROM python:3.12.8-slim

WORKDIR /app

# Install system dependencies (curl for health checks)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the application
COPY . .

# Set Python path to include src directory and ensure output is not buffered
ENV PYTHONPATH=/app/src:$PYTHONPATH
ENV PYTHONUNBUFFERED=1

# Install build dependencies and project dependencies
RUN pip install --no-cache-dir hatchling && \
    pip install --no-cache-dir -e .

# Create reports and data directories
RUN mkdir -p /app/reports /app/data

# Run the application
CMD ["python", "-m", "tv_research.main"]
