from django.db import models
from apps.categories.models import Categorie

class Categorie(models.Model):
    """
    Represents a category in the pharmacy management system.

    Attributes:
        nom (str): The unique name of the category.
        description (str): An optional description of the category.
        created_at (datetime): The timestamp when the category was created.
    """
    nom = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Category Name",
        help_text="Enter the unique name of the category."
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Provide an optional description for the category."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="The timestamp when the category was created."
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['-created_at']
        db_table = 'categories_categorie'

    def __str__(self):
        """
        Returns a string representation of the category.
        """
        return self.nom
    
