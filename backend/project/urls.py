from django.urls import path, include
from django.contrib import admin
from api.views import health_check

urlpatterns = [
    path("", health_check, name="health_check"),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]
