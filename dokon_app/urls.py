from django.urls import path
# from django.contrib.auth.views import LoginView, LogoutView
from .views import dashboard, mahsulot, set_product_type_cookie, create_product_type, create_product, edit_product, edit_product_type, sell_product

app_name = 'dokon_app'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('mahsulot/', mahsulot, name='mahsulot'),
    path('set_product_type_cookie/<int:product_type_id>/', set_product_type_cookie, name='set_product_type_cookie'),
    path('create_product_type/', create_product_type, name='create_product_type'),
    path('create_product/', create_product, name='create_product'),
    path('edit_product_type/<int:product_type_id>/', edit_product_type, name='edit_product_type'),
    path('edit_product/<int:product_id>/', edit_product, name='edit_product'),
    path('sell_product/', sell_product, name='sell_product'),
    # path('get_products/', get_products, name='get_products'),
    # path('', dashboard, name='dashboard'),
    # path('', dashboard, name='dashboard'),
    # path('', LoginView.as_view(), name="login"),
    # path('logout/', LogoutView.as_view(), name="logout"),
]