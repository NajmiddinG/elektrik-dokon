from django.urls import path
from .views import (
    dashboard,
    obyekt_ishi
)

app_name = 'ishchi_app'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('obyekt_ishi/', obyekt_ishi, name='obyekt_ishi'),
]