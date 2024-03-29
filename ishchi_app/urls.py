from django.urls import path
from .views import (
    dashboard,
    obyekt_ishi,
    done_work_post,
    done_work_list,
    done_work_detail,
    allow_add,
)

app_name = 'ishchi_app'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('obyekt_ishi/', obyekt_ishi, name='obyekt_ishi'),
    path('done_work_post/', done_work_post, name='done_work_post'),

    path('done_work_list/', done_work_list, name='done_work_list'),
    path('done_work_detail/', done_work_detail, name='done_work_detail'),

    path('allow_add/', allow_add, name='allow_add'),
    
]