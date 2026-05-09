"""
Service layer for Categorie — business logic lives here.
"""
from typing import Optional

from django.db.models import QuerySet
from rest_framework.exceptions import NotFound, ValidationError

from apps.categories.models import Categorie
from apps.categories.repositories import CategorieRepository


class CategorieService:
    """Business logic for category management."""

    def __init__(self):
        self.repo = CategorieRepository()

    def list_categories(self) -> QuerySet:
        """Return all categories."""
        return self.repo.get_all()

    def get_category(self, pk: int) -> Categorie:
        """Return a category or raise 404."""
        instance = self.repo.get_by_id(pk)
        if not instance:
            raise NotFound(f"Catégorie avec l'id {pk} introuvable.")
        return instance

    def create_category(self, nom: str, description: Optional[str] = None) -> Categorie:
        """Create a new category after uniqueness check."""
        if self.repo.exists_with_name(nom):
            raise ValidationError({"nom": "Une catégorie avec ce nom existe déjà."})
        return self.repo.create(nom=nom.strip(), description=description)

    def update_category(
        self,
        pk: int,
        nom: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Categorie:
        """Update an existing category."""
        instance = self.get_category(pk)
        updates = {}
        if nom is not None:
            if self.repo.exists_with_name(nom, exclude_pk=pk):
                raise ValidationError({"nom": "Une catégorie avec ce nom existe déjà."})
            updates["nom"] = nom.strip()
        if description is not None:
            updates["description"] = description
        return self.repo.update(instance, **updates)

    def delete_category(self, pk: int) -> None:
        """Delete a category if it has no linked medications."""
        instance = self.get_category(pk)
        if instance.medicament_set.exists():
            raise ValidationError(
                "Impossible de supprimer une catégorie contenant des médicaments."
            )
        self.repo.delete(instance)
