"""Admin registration for Medicament."""
from django.contrib import admin
from apps.medicaments.models import Medicament


@admin.register(Medicament)
class MedicamentAdmin(admin.ModelAdmin):
    list_display = ["nom", "dci", "categorie", "stock_actuel", "stock_minimum", "prix_vente", "est_actif"]
    list_filter = ["est_actif", "ordonnance_requise", "categorie"]
    search_fields = ["nom", "dci"]
    ordering = ["nom"]
