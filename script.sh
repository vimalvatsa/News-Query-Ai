#!/bin/bash
python task.py 
redis-server
python manage.py runserver 0.0.0.0:80 >> Local.log &
fg %1
