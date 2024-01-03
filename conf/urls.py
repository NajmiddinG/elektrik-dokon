from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from main_app.views import user_login


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user_login, name='user_login'),
    path('', include('main_app.urls'), name='main_app'),
    path('dokon/', include('dokon_app.urls'), name='dokon_app'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
