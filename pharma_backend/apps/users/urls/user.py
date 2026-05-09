"""
User management URL routes (pharmacist admin).
"""
from django.urls import path

from apps.users.views import UserViewSet

user_list = UserViewSet.as_view({"get": "list"})
user_detail = UserViewSet.as_view(
    {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
)
change_password = UserViewSet.as_view({"post": "change_password"})

urlpatterns = [
    path("users/", user_list, name="user-list"),
    path("users/<int:pk>/", user_detail, name="user-detail"),
    path("users/change-password/", change_password, name="user-change-password"),
]
