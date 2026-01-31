from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UploadCSVView,
    DatasetViewSet,
    DatasetHistoryView, # Keep only if not fully merged into ViewSet, but logically History is just list? actually keep it for now or merge.
    RegisterView,
    LoginView,
    home,
)

router = DefaultRouter()
router.register(r"datasets", DatasetViewSet, basename="dataset")

urlpatterns = [
    path("", include(router.urls)),
    path("upload/", UploadCSVView.as_view(), name="upload"),
    path("history/", DatasetHistoryView.as_view(), name="history"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
]
