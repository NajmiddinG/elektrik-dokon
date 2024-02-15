# from django.urls import path
# from .views import admin_list, login_page, ishchilar_page, magazin_page, zakazchi_page

# urlpatterns = [
#     path('asilbek/', admin_list, name="asilbek"),
#     path('shop/', magazin_page, name="shop"),
#     path('user/', zakazchi_page, name="user"),
#     path('ishchilar/', ishchilar_page, name="ishchilar"),
# ]


from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    user_login,
    dashboard,
    create_user,
    edit_user,
    ishchilar_holati,
    hisobotlar,
    start_job,
    end_job,
    set_cookie_for_all_types_of_filter_view,
    create_obyekt_worker_months,
    done_work_detail,
    edit_obyekt_worker_months,
    generate_worker_pdf,
    create_monthly_workers_report,
    elektrik_products_current_report,
    santexnika_products_current_report,
    history_sold_out_products_current_report,
    history_came_products_current_report,
    history_sold_out_to_obyekt_products_current_report,
)

app_name = 'main_app'

urlpatterns = [
    path('', user_login, name="user_login"),
    path('user/', dashboard, name="dashboard"),
    path('create_user/', create_user, name="create_user"),
    path('edit_user/<int:user_id>/', edit_user, name="edit_user"),

    path('ishchilar_holati/', ishchilar_holati, name="ishchilar_holati"),
    path('hisobotlar/', hisobotlar, name="hisobotlar"),

    path('start_job/', start_job, name="start_job"),
    path('end_job/', end_job, name="end_job"),

    path('set_cookie_for_all_types_of_filter_view/<str:name>/<int:value>/', set_cookie_for_all_types_of_filter_view, name="set_cookie_for_all_types_of_filter_view"),

    path('create_obyekt_worker_months/', create_obyekt_worker_months, name="create_obyekt_worker_months"),

    path('ishchilar_ishlari/', done_work_detail, name="done_work_detail"),

    path('edit_obyekt_worker_months/<int:done_work_id>/', edit_obyekt_worker_months, name='edit_obyekt_worker_months'),

    path('generate_worker_pdf/', generate_worker_pdf, name='generate_worker_pdf'),
    path('create_monthly_workers_report/', create_monthly_workers_report, name='create_monthly_workers_report'),
    path('elektrik_products_current_report/', elektrik_products_current_report, name='elektrik_products_current_report'),
    path('santexnika_products_current_report/', santexnika_products_current_report, name='santexnika_products_current_report'),
    path('history_sold_out_products_current_report/', history_sold_out_products_current_report, name='history_sold_out_products_current_report'),
    path('history_came_products_current_report/', history_came_products_current_report, name='history_came_products_current_report'),
    path('history_sold_out_to_obyekt_products_current_report/', history_sold_out_to_obyekt_products_current_report, name='history_sold_out_to_obyekt_products_current_report'),

]
