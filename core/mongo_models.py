from mongoengine import Document, StringField, EmailField, BooleanField, DateTimeField
from datetime import datetime

class CustomUserDoc(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    first_name = StringField()
    last_name = StringField()
    city = StringField()
    state = StringField()
    address = StringField()
    phone_number = StringField()
    password = StringField(required=True)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    date_joined = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'customuser'}
