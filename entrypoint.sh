#!/bin/bash
echo "Waiting for the database to be available..."
until nc -z -v -w30 db 5432 && psql -h db -U user -d mydatabase -c "SELECT 1;" 2>/dev/null
do
  echo "Waiting for database connection..."
  sleep 1
done
echo "Database is up, starting the application..."
exec "$@"
