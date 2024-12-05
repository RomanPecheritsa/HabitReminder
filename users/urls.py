from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserCreateAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(permission_classes=[AllowAny]), name='users_register'),
    path("login/", TokenObtainPairView.as_view(permission_classes=[AllowAny]), name="users_token"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=[AllowAny]), name="users_token_refresh"),
]