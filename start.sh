#!/bin/bash
# Navigate to your Django project directory
cd /home/ec2-user/app

# Activate virtual environment if you have one
source venv/bin/activate

# Start Django server in the background
nohup python3 manage.py runserver 0.0.0.0:8080 >/dev/null 2>&1 &
python3 manage.py collectstatic --noinput