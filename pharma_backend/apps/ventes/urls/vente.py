"""
URL routes for the Vente resource.
"""
from django.urls import path

from apps.ventes.views.vente import VenteViewSet

vente_list = VenteViewSet.as_view({"get": "list", "post": "create"})
vente_detail = VenteViewSet.as_view({"get": "retrieve", "delete": "destroy"})
vente_statut = VenteViewSet.as_view({"patch": "update_statut"})
vente_mes_ventes = VenteViewSet.as_view({"get": "mes_ventes"})

urlpatterns = [
    path("ventes/", vente_list, name="vente-list"),
    path("ventes/mes-ventes/", vente_mes_ventes, name="vente-mes-ventes"),
    path("ventes/<int:pk>/", vente_detail, name="vente-detail"),
    path("ventes/<int:pk>/statut/", vente_statut, name="vente-statut"),
]
