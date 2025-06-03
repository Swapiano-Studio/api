from django.urls import path
from .views import register_user, update_biodata

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('update_biodata/', update_biodata, name='update_biodata'),
]