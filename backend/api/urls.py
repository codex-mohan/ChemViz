from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UploadCSVView,
    DatasetViewSet,
    DatasetHistoryView,
    RegisterView,
    LoginView,
    ValidateTokenView,
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
    path("validate-token/", ValidateTokenView.as_view(), name="validate-token"),
]
