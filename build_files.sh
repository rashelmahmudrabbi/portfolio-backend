#!/bin/bash
# This script is executed by Vercel during the build phase.
# It runs database migrations and collects static files.

python manage.py migrate --noinput
python manage.py collectstatic --noinput
