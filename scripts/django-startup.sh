#!/bin/bash
# Django startup script for Oráculo Authentication Service

echo "Starting Django Authentication Service..."

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is ready!"

# Change to Django project directory
cd /app/src

# Run migrations
echo "Running Django migrations..."
python auth_service/manage.py migrate

# Collect static files
echo "Collecting static files..."
python auth_service/manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "Creating Django superuser..."
python auth_service/manage.py create_superuser_if_none

# Start Django development server
echo "Starting Django server on port 8001..."
python auth_service/manage.py runserver 0.0.0.0:8001