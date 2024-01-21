from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from main_app.views import user_login, logout_user


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user_login, name='user_login'),
    path('logout_user/', logout_user, name='logout_user'),
    path('', include('main_app.urls'), name='main_app'),
    path('dokon/', include('dokon_app.urls'), name='dokon_app'),
    path('obyekt/', include('obyekt_app.urls'), name='obyekt_app'),
    path('ishchi/', include('ishchi_app.urls'), name='ishchi_app'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
