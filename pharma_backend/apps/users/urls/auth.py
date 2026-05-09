"""
Auth URL routes: register, login, refresh, logout, me.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views.auth import LoginView, LogoutView, MeView, RegisterView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
    path("auth/logout/", LogoutView.as_view(), name="auth-logout"),
    path("auth/me/", MeView.as_view(), name="auth-me"),
]
