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
from .views import user_login, dashboard, create_user, edit_user


app_name = 'main_app'

urlpatterns = [
    path('', user_login, name="user_login"),
    path('user/', dashboard, name="dashboard"),
    path('create_user/', create_user, name="create_user"),
    path('edit_user/<int:user_id>/', edit_user, name="edit_user"),
]
