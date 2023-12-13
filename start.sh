#!/bin/bash
# Navigate to your Django project directory
cd /home/ec2-user/app

python3 manage.py collectstatic --noinput
# Start Django server in the background
nohup python3 manage.py runserver 0.0.0.0:8080 >/dev/null 2>&1 &