"""
Service layer for Vente — business logic and transactions.
"""
import logging
import uuid
from typing import List

from django.db import transaction
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

from apps.medicaments.repositories.medicament import MedicamentRepository
from apps.medicaments.services.medicament import MedicamentService
from apps.ventes.models.vent import Vente, VenteStatut
from apps.ventes.repositories.vente import VenteRepository

logger = logging.getLogger(__name__)

med_repo = MedicamentRepository()
med_service = MedicamentService()


class VenteService:
    """
    Orchestrates sale creation, status transitions and stock management.

    All multi-step operations are wrapped in atomic transactions so that
    partial failures never leave the database in an inconsistent state.
    """

    def __init__(self):
        self.repo = VenteRepository()

    # Queries
    # ------------------------------------------------------------------
    def list_ventes(self, user):
        """Pharmacists see all sales; clients see only their own."""
        if user.is_pharmacist:
            return self.repo.get_all()
        return self.repo.get_by_user(user.pk)

    def get_vente(self, pk: int, user) -> Vente:
        instance = self.repo.get_by_id(pk)
        if not instance:
            raise NotFound(f"Vente {pk} introuvable.")
        # Clients may only see their own sales
        if user.is_client and instance.created_by_id != user.pk:
            raise PermissionDenied("Vous n'avez pas accès à cette vente.")
        return instance

    # Create
    # ------------------------------------------------------------------
    @transaction.atomic
    def create_vente(self, lignes_data: List[dict], user, notes: str = None) -> Vente:
        """
        Create a Vente with its LigneVente items in one atomic transaction.

        Steps:
        1. Validate each medicament (active, not expired, enough stock).
        2. Create the Vente record.
        3. Create each LigneVente and deduct stock.
        4. Recalculate and save total_ttc.
        """
        reference = self._generate_reference()

        # --- Step 1: pre-validate all lines before any write ---
        resolved_lines = []
        for item in lignes_data:
            med = med_repo.get_by_id(item["medicament"])
            if not med:
                raise ValidationError(
                    {"medicament": f"Médicament id={item['medicament']} introuvable."}
                )
            med_service.validate_for_sale(med, item["quantite"])
            resolved_lines.append(
                {"medicament": med, "quantite": item["quantite"]}
            )

        # --- Step 2: create Vente ---
        vente = self.repo.create_vente(reference=reference, notes=notes, user=user)

        # --- Step 3: create lines + deduct stock ---
        for item in resolved_lines:
            med = item["medicament"]
            self.repo.create_ligne(
                vente=vente,
                medicament=med,
                quantite=item["quantite"],
                prix_unitaire=med.prix_vente,
            )
            med_service.deduct_stock(med, item["quantite"])

        # --- Step 4: compute total ---
        vente.recalculate_total()
        logger.info(
            "Vente créée: ref=%s, total=%.2f, user=%s",
            vente.reference, vente.total_ttc, user.username
        )
        return self.repo.get_by_id(vente.pk)  # re-fetch with prefetch

    # Status transitions
    # ------------------------------------------------------------------
    @transaction.atomic
    def update_statut(self, pk: int, new_statut: str, user) -> Vente:
        """
        Change the status of a Vente.

        Rules:
        - Confirmed sales cannot be cancelled (stock already consumed).
        - Cancelling an en_attente sale restores stock.
        - Only pharmacists can confirm or cancel sales.
        """
        vente = self.get_vente(pk, user)

        if vente.statut == new_statut:
            return vente

        if vente.statut == VenteStatut.ANNULEE:
            raise ValidationError("Une vente annulée ne peut pas changer de statut.")

        if new_statut == VenteStatut.ANNULEE:
            if vente.statut == VenteStatut.CONFIRMEE:
                raise ValidationError("Une vente confirmée ne peut pas être annulée.")
            self._restore_stock(vente)
            logger.info("Vente %s annulée — stock restauré.", vente.reference)

        self.repo.update_statut(vente, new_statut)
        vente.refresh_from_db()
        return vente

    # Private helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _generate_reference() -> str:
        return f"VNT-{uuid.uuid4().hex[:8].upper()}"

    @staticmethod
    def _restore_stock(vente: Vente) -> None:
        """Re-increment stock for every line in a cancelled sale."""
        for ligne in vente.lignes.select_related("medicament"):
            med_repo.adjust_stock(ligne.medicament, delta=ligne.quantite)
