#!/bin/sh

# wait for other servers to start
sleep 10

# Make migrations
su -m myuser -c "python manage.py makemigrations"

# Migrate database
su -m myuser -c "python manage.py migrate"

# Start development server on public IP interface, port 8000
su -m myuser -c "python manage.py runserver 0.0.0.0:8000"
