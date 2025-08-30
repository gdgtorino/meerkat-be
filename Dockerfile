# Use an official Python runtime as a parent image
# We choose a slim-buster image for a smaller footprint, suitable for production.
# Adjust the Python version (e.g., 3.10, 3.11) as per your project's needs.
FROM python:3.12

# Set the working directory in the container
# All subsequent commands will be executed relative to this directory.
WORKDIR /app

# create a non-root user to run the application
# This enhances security by avoiding running the app as the root user.
# The --system flag creates a system user, and --no-create-home avoids creating a home directory.
RUN adduser --system --no-create-home meerkat

# Install system dependencies required for some Python packages (e.g., psycopg2, Pillow)
# This step is optional but often necessary. Remove if you don't have such dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    # Add any other system dependencies here, e.g., libjpeg-dev for Pillow
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker's build cache.
# If requirements.txt doesn't change, this layer won't be rebuilt.
COPY requirements.txt .

# Install any needed Python packages specified in requirements.txt
# Using --no-cache-dir to prevent pip from storing downloaded packages, reducing image size.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
# The 'app' directory containing 'main.py' will be copied here.
# Ensure your project structure has 'app/main.py' at the root of your project.
COPY ./app /app/app
# If you have other files at the root of your project (e.g., .env files, config.yaml), copy them too:
# COPY .env /app/.env
# COPY config.yaml /app/config.yaml

# Changing user to a non-root user for better security
# It's a good practice to run applications as a non-root user in production environments.
USER meerkat

# Expose the port that FastAPI will run on
# Uvicorn, the ASGI server for FastAPI, typically runs on port 8000 by default.
EXPOSE 8080

# Define the command to run the application using Uvicorn
# - "app.main:app" refers to the 'app' object inside 'main.py' within the 'app' package.
# - "--host 0.0.0.0" makes the application accessible from outside the container.
# - "--port 8000" specifies the port.
# - "--workers 4" (optional) specifies the number of Uvicorn worker processes.
#   Adjust based on your server's CPU cores for better performance in production.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
