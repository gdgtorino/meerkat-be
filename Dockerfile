FROM python:3.13-slim-bookworm

# Set work directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry and install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only main

# Copy application code
COPY app/ ./app/

# Expose port
EXPOSE 11111

# Run app
CMD ["python", "-m", "app.main"]
