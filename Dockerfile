FROM python:3.13-slim-bookworm

# Set work directory into container
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt .

# Instal dipendencies Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all project into work directory
COPY . .

# Run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "11111"]

