"""
Repository layer for Categorie — all DB queries live here.
"""
from typing import Optional

from django.db.models import QuerySet

from apps.categories.models import Categorie


class CategorieRepository:
    """Encapsulates all database access for the Categorie model."""

    @staticmethod
    def get_all() -> QuerySet:
        """Return all categories ordered by name."""
        return Categorie.objects.all()

    @staticmethod
    def get_by_id(pk: int) -> Optional[Categorie]:
        """Return a single category or None."""
        return Categorie.objects.filter(pk=pk).first()

    @staticmethod
    def create(nom: str, description: Optional[str] = None) -> Categorie:
        """Persist a new category."""
        return Categorie.objects.create(nom=nom, description=description)

    @staticmethod
    def update(instance: Categorie, **fields) -> Categorie:
        """Update allowed fields and save."""
        for attr, value in fields.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @staticmethod
    def delete(instance: Categorie) -> None:
        """Hard-delete a category."""
        instance.delete()

    @staticmethod
    def exists_with_name(nom: str, exclude_pk: Optional[int] = None) -> bool:
        """Check uniqueness (case-insensitive)."""
        qs = Categorie.objects.filter(nom__iexact=nom)
        if exclude_pk:
            qs = qs.exclude(pk=exclude_pk)
        return qs.exists()
