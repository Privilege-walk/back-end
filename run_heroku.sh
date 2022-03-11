#!/bin/sh
python3 manage.py migrate
gunicorn privilege_walk_be.wsgi --log-file -