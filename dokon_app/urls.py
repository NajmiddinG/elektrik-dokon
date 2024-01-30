from django.urls import path
# from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    dashboard,
    mahsulot,
    set_product_type_cookie,
    create_product_type,
    create_product,
    edit_product,
    edit_product_type,
    sell_product,
    newproduct,
    insert_new_porduct,
    obyekt_dashboard,
    sell_product_to_obyekt,
)
from .santexnikaviews import (
    dashboard_santexnika,
    mahsulot_santexnika,
    set_product_type_cookie_santexnika,
    create_product_type_santexnika,
    create_product_santexnika,
    edit_product_santexnika,
    edit_product_type_santexnika,
    sell_product_santexnika,
    newproduct_santexnika,
    insert_new_porduct_santexnika,
    obyekt_dashboard_santexnika,
    sell_product_to_obyekt_santexnika,
)

app_name = 'dokon_app'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('obyekt/', obyekt_dashboard, name='obyekt_dashboard'),
    path('yangi_tovarlar/', newproduct, name='newproduct'),
    path('mahsulot/', mahsulot, name='mahsulot'),
    path('set_product_type_cookie/<int:product_type_id>/', set_product_type_cookie, name='set_product_type_cookie'),
    path('create_product_type/', create_product_type, name='create_product_type'),
    path('create_product/', create_product, name='create_product'),
    path('edit_product_type/<int:product_type_id>/', edit_product_type, name='edit_product_type'),
    path('edit_product/<int:product_id>/', edit_product, name='edit_product'),
    path('sell_product/', sell_product, name='sell_product'),
    path('sell_product_to_obyekt/', sell_product_to_obyekt, name='sell_product_to_obyekt'),
    path('insert_new_porduct/', insert_new_porduct, name='insert_new_porduct'),

    # santexnika
    path('santexnika/', dashboard_santexnika, name='dashboard_santexnika'),
    path('obyekt_santexnika/', obyekt_dashboard_santexnika, name='obyekt_dashboard_santexnika'),
    path('yangi_tovarlar_santexnika/', newproduct_santexnika, name='newproduct_santexnika'),
    path('mahsulot_santexnika/', mahsulot_santexnika, name='mahsulot_santexnika'),
    path('set_product_type_cookie/<int:product_type_id>_santexnika/', set_product_type_cookie_santexnika, name='set_product_type_cookie_santexnika'),
    path('create_product_type_santexnika/', create_product_type_santexnika, name='create_product_type_santexnika'),
    path('create_product_santexnika/', create_product_santexnika, name='create_product_santexnika'),
    path('edit_product_type_santexnika/<int:product_type_id>/', edit_product_type_santexnika, name='edit_product_type_santexnika'),
    path('edit_product_santexnika/<int:product_id>/', edit_product_santexnika, name='edit_product_santexnika'),
    path('sell_product_santexnika/', sell_product_santexnika, name='sell_product_santexnika'),
    path('sell_product_to_obyekt_santexnika/', sell_product_to_obyekt_santexnika, name='sell_product_to_obyekt_santexnika'),
    path('insert_new_porduct_santexnika/', insert_new_porduct_santexnika, name='insert_new_porduct_santexnika'),

    # path('get_products/', get_products, name='get_products'),
    # path('', dashboard, name='dashboard'),
    # path('', dashboard, name='dashboard'),
    # path('', LoginView.as_view(), name="login"),
    # path('logout/', LogoutView.as_view(), name="logout"),
]