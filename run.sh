#!/bin/sh

# DB Migrations
python3 manage.py makemigrations
python3 manage.py migrate

# The running command
daphne -b 0.0.0.0 -p 8000 privilege_walk_be.asgi:application