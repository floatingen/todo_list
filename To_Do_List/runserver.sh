#!/bin/bash

cd /usr/src/main/
export PYTHONPATH=/usr/src/main/;$PYTHONPATH
export DJANGO_SUPERUSER_PASSWORD=admin99password

python manage.py makemigrations
python manage.py migrate --noinput
python manage.py createsuperuser --noinput --username=admin --email=vladislav.seleznev99@gmail.com
python manage.py runserver 0.0.0.0:8000