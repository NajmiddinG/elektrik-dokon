from django.urls import path
from .views import (
    dashboard,
)

app_name = 'ishchi_app'

urlpatterns = [
    path('', dashboard, name='dashboard'),
]