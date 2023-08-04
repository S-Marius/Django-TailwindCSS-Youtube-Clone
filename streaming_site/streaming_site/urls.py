from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("", include("core.urls")),
    path("video/", include("video.urls")),
    path("analytics/", include("analytics.urls")),
    path("admin/", admin.site.urls),
]

# Serve media files during development 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)