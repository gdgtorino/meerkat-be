FROM python:3.13-slim-bookworm

# Set work directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry and install all dependencies (including dev)
RUN poetry config virtualenvs.create false && \
  poetry install --no-root

# Copy application code
COPY . .

# Expose port
EXPOSE 11111

# Run with auto-reload for development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "11111", "--reload"]
