"""
django-filter FilterSet for Vente.
"""
import django_filters

from apps.ventes.models import Vente, VenteStatut


class VenteFilter(django_filters.FilterSet):
    """
    Supported query params:
      ?statut=confirmee|en_attente|annulee
      ?date_debut=YYYY-MM-DD
      ?date_fin=YYYY-MM-DD
      ?created_by=<user_id>
    """

    statut = django_filters.ChoiceFilter(choices=VenteStatut.choices)
    date_debut = django_filters.DateFilter(field_name="date_vente", lookup_expr="date__gte")
    date_fin = django_filters.DateFilter(field_name="date_vente", lookup_expr="date__lte")
    created_by = django_filters.NumberFilter(field_name="created_by__id")

    class Meta:
        model = Vente
        fields = ["statut", "date_debut", "date_fin", "created_by"]
