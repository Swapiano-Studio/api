#!/bin/bash
# Build script for Render.com Django deployment

set -e

pip install -r requirements.txt
python manage.py migrate
# Create superuser only if no user exists (avoid line breaks in python -c)
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model();\nif not User.objects.exists(): User.objects.create_superuser('admin', 'kadeksanandanova@gmail.com', 'Admin123#')"
python manage.py loaddata shoppit/fixtures/products.json
python manage.py collectstatic --noinput
