#!/bin/sh

# DB Migrations
python3 manage.py makemigrations
python3 manage.py migrate

# The running command
daphne run privilege_walk_be.asgi:application