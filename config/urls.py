from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # Web urls
    path('', include('core.urls')),
<<<<<<< HEAD
    path('accounts/', include('allauth.urls')),
=======
>>>>>>> 11b04389547943f6cd409ae4f74ccc304e0b5e71
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
