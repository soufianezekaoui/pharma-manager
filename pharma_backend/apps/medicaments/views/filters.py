"""
django-filter FilterSet for Medicament.
"""
import django_filters

from apps.medicaments.models import Medicament


class MedicamentFilter(django_filters.FilterSet):
    """
    Query params supported:
      ?categorie=<id>
      ?est_actif=true|false
      ?ordonnance_requise=true|false
      ?prix_vente_min=<float>
      ?prix_vente_max=<float>
      ?expire_avant=<YYYY-MM-DD>
    """

    categorie = django_filters.NumberFilter(field_name="categorie__id")
    est_actif = django_filters.BooleanFilter(field_name="est_actif")
    ordonnance_requise = django_filters.BooleanFilter(field_name="ordonnance_requise")
    prix_vente_min = django_filters.NumberFilter(field_name="prix_vente", lookup_expr="gte")
    prix_vente_max = django_filters.NumberFilter(field_name="prix_vente", lookup_expr="lte")
    expire_avant = django_filters.DateFilter(field_name="date_expiration", lookup_expr="lte")
    stock_bas = django_filters.BooleanFilter(method="filter_stock_bas", label="Stock bas uniquement")

    class Meta:
        model = Medicament
        fields = [
            "categorie",
            "est_actif",
            "ordonnance_requise",
            "prix_vente_min",
            "prix_vente_max",
            "expire_avant",
            "stock_bas",
        ]

    def filter_stock_bas(self, queryset, name, value):
        if value:
            from django.db.models import F
            return queryset.filter(stock_actuel__lte=F("stock_minimum"))
        return queryset
