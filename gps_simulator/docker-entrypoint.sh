#!/usr/bin/env bash

sleep 3

python manage.py makemigrations --settings=project.settings.gs
python manage.py migrate --settings=project.settings.gs

python manage.py consume_start_trip_events --settings=project.settings.gs &

python manage.py emit_gps_events --settings=project.settings.gs
