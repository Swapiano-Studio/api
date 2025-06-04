#!/bin/bash
# Build script for Render.com Django deployment

set -e

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser --noinput --username admin --email kadeksananda@gmail.com --password admin123
python manage.py loaddata shoppit/fixtures/products.json
python manage.py collectstatic --noinput
