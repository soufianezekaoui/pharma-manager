"""Admin registration for Categorie."""
from django.contrib import admin
from apps.categories.models import Categorie


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ["nom", "description"]
    search_fields = ["nom"]
