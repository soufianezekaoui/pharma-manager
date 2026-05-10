"""
Categorie model for medication classification.
"""
from django.db import models


class Categorie(models.Model):
    """
    Represents a medication category (e.g. Antibiotiques, Analgésiques).

    Attributes:
        nom (str): Unique category name.
        description (str): Optional long description.
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
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["nom"]

    def __str__(self) -> str:
        return self.nom
