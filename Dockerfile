# Use official Python image
FROM python:3.12-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Install system packages required for mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y default-mysql-client

# Copy project files
COPY . .

# Expose application port
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "hotel_management.wsgi:application", "--bind", "0.0.0.0:8000"]