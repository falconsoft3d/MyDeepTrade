#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is ready!"

# Wait for Django app to be ready
echo "Waiting for Django app..."
sleep 10

# Run work order scheduler
echo "Starting work order scheduler..."
python manage.py run_workorders
