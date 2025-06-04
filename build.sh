#!/bin/bash
# Build script for Render.com Django deployment

set -e

pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata shoppit/fixtures/products.json
python manage.py collectstatic --noinput
