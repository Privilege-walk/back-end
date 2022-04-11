#!/bin/sh

# DB Migrations
python3 manage.py makemigrations
python3 manage.py migrate

# The running command
python3 manage.py runserver