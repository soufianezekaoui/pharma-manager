"""
Root URL configuration for Pharma Manager.
"""
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # OpenAPI schema & docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # Application routes
    path("api/", include("apps.categories.urls.categorie")),
    path("api/", include("apps.medicaments.urls.medicament")),
    path("api/", include("apps.users.urls.auth")),
    path("api/", include("apps.users.urls.user")),
    path("api/", include("apps.ventes.urls.vente")),
]
