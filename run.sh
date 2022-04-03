#!/bin/sh

# DB Migrations
python3 manage.py makemigrations
python3 manage.py migrate

# The running command
gunicorn privilege_walk_be.wsgi --workers 3