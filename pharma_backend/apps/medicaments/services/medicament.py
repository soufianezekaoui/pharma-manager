"""
Service layer for Medicament — all business logic lives here.
"""
import logging
from typing import Optional

from django.db.models import QuerySet
from django.utils import timezone
from rest_framework.exceptions import NotFound, ValidationError

from apps.medicaments.models import Medicament
from apps.medicaments.repositories.medicament import MedicamentRepository

logger = logging.getLogger(__name__)


class MedicamentService:
    """Business logic for medication management."""

    def __init__(self):
        self.repo = MedicamentRepository()

    # Queries
    # ------------------------------------------------------------------
    def list_medicaments(self, active_only: bool = False) -> QuerySet:
        if active_only:
            return self.repo.get_active()
        return self.repo.get_all()

    def get_medicament(self, pk: int) -> Medicament:
        instance = self.repo.get_by_id(pk)
        if not instance:
            raise NotFound(f"Médicament avec l'id {pk} introuvable.")
        return instance

    def get_low_stock_alerts(self) -> QuerySet:
        return self.repo.get_low_stock()

    def get_expired_medications(self) -> QuerySet:
        return self.repo.get_expired()

    # Mutations
    # ------------------------------------------------------------------
    def create_medicament(self, validated_data: dict) -> Medicament:
        """Create a new medication after all business rules pass."""
        self._validate_prices(
            prix_achat=validated_data.get("prix_achat", 0),
            prix_vente=validated_data.get("prix_vente", 0),
        )
        return self.repo.create(**validated_data)

    def update_medicament(self, pk: int, validated_data: dict) -> Medicament:
        """Update an existing medication."""
        instance = self.get_medicament(pk)
        prix_achat = validated_data.get("prix_achat", instance.prix_achat)
        prix_vente = validated_data.get("prix_vente", instance.prix_vente)
        self._validate_prices(prix_achat, prix_vente)
        return self.repo.update(instance, **validated_data)

    def soft_delete_medicament(self, pk: int) -> Medicament:
        """Deactivate (soft-delete) a medication."""
        instance = self.get_medicament(pk)
        return self.repo.soft_delete(instance)

    def restock(self, pk: int, quantite: int) -> Medicament:
        """Add stock units to a medication."""
        if quantite <= 0:
            raise ValidationError({"quantite": "La quantité doit être strictement positive."})
        instance = self.get_medicament(pk)
        updated = self.repo.adjust_stock(instance, delta=quantite)
        logger.info("Medicament %s restocked by %d units. New stock: %d", pk, quantite, updated.stock_actuel)
        return updated

    # Stock validation used by VenteService
    # ------------------------------------------------------------------
    def validate_for_sale(self, medicament: Medicament, quantite: int) -> None:
        """
        Raise ValidationError if the medication cannot be sold.
        Checks: active status, expiration, and available stock.
        """
        if not medicament.est_actif:
            raise ValidationError(
                f"Le médicament '{medicament.nom}' est désactivé et ne peut pas être vendu."
            )
        if medicament.is_expired:
            raise ValidationError(
                f"Le médicament '{medicament.nom}' est expiré (exp: {medicament.date_expiration})."
            )
        if medicament.stock_actuel < quantite:
            raise ValidationError(
                f"Stock insuffisant pour '{medicament.nom}'. "
                f"Disponible: {medicament.stock_actuel}, demandé: {quantite}."
            )

    def deduct_stock(self, medicament: Medicament, quantite: int) -> Medicament:
        """Decrease stock after a confirmed sale."""
        updated = self.repo.adjust_stock(medicament, delta=-quantite)
        if updated.is_low_stock:
            logger.warning(
                "LOW STOCK ALERT — Medicament '%s' (id=%d): stock=%d, minimum=%d",
                updated.nom,
                updated.pk,
                updated.stock_actuel,
                updated.stock_minimum,
            )
        return updated

    # Private helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _validate_prices(prix_achat, prix_vente) -> None:
        if float(prix_vente) < float(prix_achat):
            raise ValidationError(
                {"prix_vente": "Le prix de vente doit être >= au prix d'achat."}
            )
