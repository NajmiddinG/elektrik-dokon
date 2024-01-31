from django.urls import path
# from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    dashboard,
    create_obyekt,
    edit_obyekt,
    obyekt_ishi,
    set_obyekt_cookie,
    create_obyekt_ishi,
    edit_obyekt_ishi,
    create_obyekt_job_type,
    create_work_amount_job_type,
    set_obyekt_cookie2,
    create_obyekt_given_amount,
    edit_obyekt_given_amount,
    given_money_views,
    calculate_all_from_zero_view,
    create_obyekt_instruktsiya
)
app_name = 'obyekt_app'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('create_obyekt/', create_obyekt, name='create_obyekt'),
    path('edit_obyekt/<int:obyekt_id>/', edit_obyekt, name='edit_obyekt'),
    path('create_obyekt_job_type/', create_obyekt_job_type, name='create_obyekt_job_type'),

    path('obyekt_ishi/', obyekt_ishi, name='obyekt_ishi'),
    path('create_obyekt_ishi/', create_obyekt_ishi, name='create_obyekt_ishi'),
    path('edit_obyekt_ishi/<int:obyekt_id>/', edit_obyekt_ishi, name='edit_obyekt_ishi'),
    path('create_work_amount_job_type/', create_work_amount_job_type, name='create_work_amount_job_type'),

    path('create_obyekt_instruktsiya/', create_obyekt_instruktsiya, name='create_obyekt_instruktsiya'),

    path('create_obyekt_given_amount/', create_obyekt_given_amount, name='create_obyekt_given_amount'),
    path('edit_obyekt_given_amount/', edit_obyekt_given_amount, name='edit_obyekt_given_amount'),

    path('set_obyekt_cookie/<int:obyekt_id>/', set_obyekt_cookie, name='set_obyekt_cookie'),
    path('set_obyekt_cookie2/<int:obyekt_id>/', set_obyekt_cookie2, name='set_obyekt_cookie2'),

    path('given_money_views/', given_money_views, name='given_money_views'),
    path('calculate_all_from_zero_view/', calculate_all_from_zero_view, name='calculate_all_from_zero_view'),


    # path('obyekt/', obyekt_dashboard, name='obyekt_dashboard'),
    # path('yangi_tovarlar/', newproduct, name='newproduct'),
    # path('mahsulot/', mahsulot, name='mahsulot'),
    # path('set_product_type_cookie/<int:product_type_id>/', set_product_type_cookie, name='set_product_type_cookie'),
    # path('create_product_type/', create_product_type, name='create_product_type'),
    # path('create_product/', create_product, name='create_product'),
    # path('edit_product_type/<int:product_type_id>/', edit_product_type, name='edit_product_type'),
    # path('edit_product/<int:product_id>/', edit_product, name='edit_product'),
    # path('sell_product/', sell_product, name='sell_product'),
    # path('sell_product_to_obyekt/', sell_product_to_obyekt, name='sell_product_to_obyekt'),
    # path('insert_new_porduct/', insert_new_porduct, name='insert_new_porduct'),

    # # santexnika
    # path('santexnika/', dashboard_santexnika, name='dashboard_santexnika'),
    # path('obyekt_santexnika/', obyekt_dashboard_santexnika, name='obyekt_dashboard_santexnika'),
    # path('yangi_tovarlar_santexnika/', newproduct_santexnika, name='newproduct_santexnika'),
    # path('mahsulot_santexnika/', mahsulot_santexnika, name='mahsulot_santexnika'),
    # path('set_product_type_cookie/<int:product_type_id>_santexnika/', set_product_type_cookie_santexnika, name='set_product_type_cookie_santexnika'),
    # path('create_product_type_santexnika/', create_product_type_santexnika, name='create_product_type_santexnika'),
    # path('create_product_santexnika/', create_product_santexnika, name='create_product_santexnika'),
    # path('edit_product_type_santexnika/<int:product_type_id>/', edit_product_type_santexnika, name='edit_product_type_santexnika'),
    # path('edit_product_santexnika/<int:product_id>/', edit_product_santexnika, name='edit_product_santexnika'),
    # path('sell_product_santexnika/', sell_product_santexnika, name='sell_product_santexnika'),
    # path('sell_product_to_obyekt_santexnika/', sell_product_to_obyekt_santexnika, name='sell_product_to_obyekt_santexnika'),
    # path('insert_new_porduct_santexnika/', insert_new_porduct_santexnika, name='insert_new_porduct_santexnika'),

    # path('get_products/', get_products, name='get_products'),
    # path('', dashboard, name='dashboard'),
    # path('', dashboard, name='dashboard'),
    # path('', LoginView.as_view(), name="login"),
    # path('logout/', LogoutView.as_view(), name="logout"),
]