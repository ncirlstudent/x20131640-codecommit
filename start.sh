#!/bin/bash
# Navigate to your Django project directory
cd /home/ec2-user/app

sudo chmod -R 755 static/
sudo chmod -R 755 media/
sudo python3 manage.py collectstatic --noinput
# Start Django server in the background
sudo nohup python3 manage.py runserver 0.0.0.0:8080 >/dev/null 2>&1 &
