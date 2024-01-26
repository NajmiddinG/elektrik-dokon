from django.urls import path
from .views import (
    dashboard,
    obyekt_ishi,
    done_work_post,
)

app_name = 'ishchi_app'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('obyekt_ishi/', obyekt_ishi, name='obyekt_ishi'),
    path('done_work_post/', done_work_post, name='done_work_post'),
]