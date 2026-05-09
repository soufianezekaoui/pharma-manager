"""
URL routes for the Medicament resource.
"""
from django.urls import path

from apps.medicaments.views import MedicamentViewSet

medicament_list = MedicamentViewSet.as_view({"get": "list", "post": "create"})
medicament_detail = MedicamentViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)
medicament_restock = MedicamentViewSet.as_view({"post": "restock"})
medicament_alertes = MedicamentViewSet.as_view({"get": "alertes_stock"})
medicament_expires = MedicamentViewSet.as_view({"get": "expires"})

urlpatterns = [
    path("medicaments/", medicament_list, name="medicament-list"),
    path("medicaments/alertes-stock/", medicament_alertes, name="medicament-alertes-stock"),
    path("medicaments/expires/", medicament_expires, name="medicament-expires"),
    path("medicaments/<int:pk>/", medicament_detail, name="medicament-detail"),
    path("medicaments/<int:pk>/restock/", medicament_restock, name="medicament-restock"),
]
