"""
URL routes for the Categorie resource.
"""
from django.urls import path

from apps.categories.views.categorie import CategorieViewSet

categorie_list = CategorieViewSet.as_view({"get": "list", "post": "create"})
categorie_detail = CategorieViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    path("categories/", categorie_list, name="categorie-list"),
    path("categories/<int:pk>/", categorie_detail, name="categorie-detail"),
]
