
from django.contrib import admin
from django.urls import path, include,re_path
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('geeks_tools/', include('geeks_tools.urls')),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    re_path(r'auth/', include('drf_social_oauth2.urls', namespace='drf'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)