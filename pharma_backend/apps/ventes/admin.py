"""Admin registration for Vente and LigneVente."""
from django.contrib import admin
from apps.ventes.models import Vente, LigneVente


class LigneVenteInline(admin.TabularInline):
    model = LigneVente
    extra = 0
    readonly_fields = ["sous_total"]


@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    list_display = ["reference", "statut", "total_ttc", "created_by", "date_vente"]
    list_filter = ["statut"]
    inlines = [LigneVenteInline]
    readonly_fields = ["reference", "total_ttc", "date_vente"]
