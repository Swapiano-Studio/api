#!/bin/bash
# Build script for Render.com Django deployment

set -e

pip install -r requirements.txt
python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model();\nif not User.objects.exists():\n    User.objects.create_superuser('admin', 'kadeksanandanova@gmail.com', 'Admin123#')" | python manage.py shell
python manage.py loaddata shoppit/fixtures/products.json
python manage.py collectstatic --noinput
