#!/bin/bash
aws s3 cp s3://doc-analyser/config/DocSearchConfig.json DocSearchConfig.json
set -m
cron
python manage.py runserver 0.0.0.0:80 >> Local.log &
fg %1
