#!/bin/bash
set -e

pip install -r requirements.txt
python manage.py migrate --noinput

# Create superuser if none exists
echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
if not User.objects.exists(): \
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell

python manage.py loaddata shoppit/fixtures/products.json
python manage.py collectstatic --noinput