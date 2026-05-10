"""
Vente and LigneVente models.
"""
import uuid

from django.conf import settings
from django.db import models


class VenteStatut(models.TextChoices):
    EN_ATTENTE = "en_attente", "En attente"
    CONFIRMEE = "confirmee", "Confirmée"
    ANNULEE = "annulee", "Annulée"


class Vente(models.Model):
    """
    Represents a pharmacy sale transaction.

    Business rules:
    - reference is auto-generated (UUID prefix) if not provided.
    - total_ttc is calculated automatically from LigneVente items.
    - Cancelling a sale restores stock.
    """

    reference = models.CharField(
        max_length=100, unique=True, verbose_name="Référence",
    )
    date_vente = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de vente",
    )
    total_ttc = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name="Total TTC (MAD)",
    )
    statut = models.CharField(
        max_length=30, choices=VenteStatut.choices,
        default=VenteStatut.EN_ATTENTE, verbose_name="Statut",
    )
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="ventes",
        verbose_name="Créé par",
    )

    class Meta:
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"
        ordering = ["-date_vente"]

    def __str__(self) -> str:
        return f"Vente {self.reference} — {self.statut}"

    def recalculate_total(self) -> None:
        """Recalculate total_ttc from all associated LigneVente rows."""
        from django.db.models import Sum
        result = self.lignes.aggregate(total=Sum("sous_total"))
        self.total_ttc = result["total"] or 0
        self.save(update_fields=["total_ttc"])


class LigneVente(models.Model):
    """
    A single line item within a Vente.

    sous_total is computed automatically: quantite × prix_unitaire.
    prix_unitaire is a snapshot of the price at time of sale.
    """

    vente = models.ForeignKey(
        Vente, on_delete=models.CASCADE,
        related_name="lignes", verbose_name="Vente",
    )
    medicament = models.ForeignKey(
        "medicaments.Medicament",
        on_delete=models.PROTECT,
        related_name="lignes_vente",
        verbose_name="Médicament",
    )
    quantite = models.IntegerField(verbose_name="Quantité")
    prix_unitaire = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name="Prix unitaire (MAD)",
    )
    sous_total = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name="Sous-total (MAD)",
    )

    class Meta:
        verbose_name = "Ligne de vente"
        verbose_name_plural = "Lignes de vente"
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.quantite}× {self.medicament.nom} = {self.sous_total} MAD"

    def save(self, *args, **kwargs):
        """Auto-compute sous_total before every save."""
        self.sous_total = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)
