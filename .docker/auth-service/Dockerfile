# Django Authentication Service Dockerfile
FROM python:3.10.17-slim

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=auth_service.settings
ENV PYTHONPATH=/app/src

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements-auth.txt .
RUN pip install --no-cache-dir -r requirements-auth.txt

# Copy project
COPY . .

# Make manage.py executable
RUN chmod +x src/auth_service/manage.py

# Expose port
EXPOSE 8001

# Run Django development server
CMD ["bash", "scripts/django-startup.sh"]