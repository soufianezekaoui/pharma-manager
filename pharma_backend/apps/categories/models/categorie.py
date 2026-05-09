"""
Categorie model — maps to the existing 'categories_categorie' table.
"""
from django.db import models
 
class Categorie(models.Model):
    """
    Represents a medication category (e.g. Antibiotiques, Analgésiques).
 
    The table is pre-existing in PostgreSQL; no migration will create it.
    """
 
    nom = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nom de la catégorie",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
    )
 
    class Meta:
        db_table = "categories_categorie"
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["nom"]
 
    def __str__(self) -> str:
        return self.nom
 