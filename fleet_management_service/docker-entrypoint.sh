#!/usr/bin/env bash

sleep 3

python manage.py makemigrations --settings=project.settings.fms
python manage.py migrate --settings=project.settings.fms

python manage.py consume_penalty_events --settings=project.settings.fms &

python manage.py runserver 0.0.0.0:8888 --settings=project.settings.fms
