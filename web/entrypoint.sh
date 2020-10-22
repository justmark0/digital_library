#!/bin/sh

#source venv/bin/activate

echo "Waiting for postgres..."

while ! nc -z db 5432; 
do
	sleep 0.1
done
echo "PostgreSQL started"

#python main.py create_db
#python main.py runserver -h 0.0.0.0

exec "$@"
