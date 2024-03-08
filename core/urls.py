from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from api.views import custom404

handler404 = custom404

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    
    path("", TemplateView.as_view(template_name="index.html")),
    path("api/", include("api.urls")),
    # path("admin/", admin.site.urls),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
