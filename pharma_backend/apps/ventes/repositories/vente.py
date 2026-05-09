"""
Repository for Vente and LigneVente — DB queries only.
"""
from typing import Optional

from django.db.models import QuerySet

from apps.ventes.models.vent import LigneVente, Vente


class VenteRepository:
    """Encapsulates all database access for Vente and LigneVente."""

    @staticmethod
    def get_all() -> QuerySet:
        return Vente.objects.select_related("created_by").prefetch_related(
            "lignes__medicament"
        )

    @staticmethod
    def get_by_id(pk: int) -> Optional[Vente]:
        return (
            Vente.objects.select_related("created_by")
            .prefetch_related("lignes__medicament")
            .filter(pk=pk)
            .first()
        )

    @staticmethod
    def get_by_user(user_id: int) -> QuerySet:
        return (
            Vente.objects.select_related("created_by")
            .prefetch_related("lignes__medicament")
            .filter(created_by_id=user_id)
        )

    @staticmethod
    def create_vente(reference: str, notes: Optional[str], user) -> Vente:
        return Vente.objects.create(
            reference=reference,
            notes=notes,
            created_by=user,
        )

    @staticmethod
    def create_ligne(vente: Vente, medicament, quantite: int, prix_unitaire) -> LigneVente:
        return LigneVente.objects.create(
            vente=vente,
            medicament=medicament,
            quantite=quantite,
            prix_unitaire=prix_unitaire,
        )

    @staticmethod
    def update_statut(instance: Vente, statut: str) -> Vente:
        instance.statut = statut
        instance.save(update_fields=["statut"])
        return instance
