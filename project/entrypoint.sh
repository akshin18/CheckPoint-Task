#!/bin/bash

# Wait for the database to be ready
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  echo "Waiting for the database..."
  sleep 2
done

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py create_superuser


# Start the application
exec "$@"