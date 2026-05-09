"""
Repository for Medicament — all DB queries isolated here.
"""
from typing import Optional

from django.db.models import QuerySet

from apps.medicaments.models import Medicament


class MedicamentRepository:
    """Encapsulates all database access for the Medicament model."""

    @staticmethod
    def get_all() -> QuerySet:
        return Medicament.objects.select_related("categorie").all()

    @staticmethod
    def get_active() -> QuerySet:
        return Medicament.objects.select_related("categorie").filter(est_actif=True)

    @staticmethod
    def get_by_id(pk: int) -> Optional[Medicament]:
        return Medicament.objects.select_related("categorie").filter(pk=pk).first()

    @staticmethod
    def get_low_stock() -> QuerySet:
        """Return active medications whose stock is at or below minimum."""
        from django.db.models import F
        return (
            Medicament.objects.select_related("categorie")
            .filter(est_actif=True, stock_actuel__lte=F("stock_minimum"))
        )

    @staticmethod
    def get_expired() -> QuerySet:
        """Return active medications that have expired."""
        from django.utils import timezone
        return (
            Medicament.objects.select_related("categorie")
            .filter(est_actif=True, date_expiration__lt=timezone.now().date())
        )

    @staticmethod
    def create(**fields) -> Medicament:
        return Medicament.objects.create(**fields)

    @staticmethod
    def update(instance: Medicament, **fields) -> Medicament:
        for attr, value in fields.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @staticmethod
    def soft_delete(instance: Medicament) -> Medicament:
        instance.est_actif = False
        instance.save(update_fields=["est_actif"])
        return instance

    @staticmethod
    def adjust_stock(instance: Medicament, delta: int) -> Medicament:
        """Increment (positive) or decrement (negative) stock atomically."""
        from django.db.models import F
        Medicament.objects.filter(pk=instance.pk).update(
            stock_actuel=F("stock_actuel") + delta
        )
        instance.refresh_from_db()
        return instance
