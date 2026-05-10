"""
Medicament model for pharmacy inventory management.
"""
from django.db import models
from django.utils import timezone

from apps.categories.models import Categorie


class Medicament(models.Model):
    """
    Represents a medication in the pharmacy inventory.

    Attributes:
        nom (str): Brand name of the medication.
        dci (str): International Common Denomination.
        categorie (Categorie): FK to medication category.
        forme (str): Galenic form (tablet, syrup, etc.).
        dosage (str): Dosage description (e.g. 500mg).
        prix_achat (Decimal): Purchase price in MAD.
        prix_vente (Decimal): Sale price in MAD.
        stock_actuel (int): Current stock quantity.
        stock_minimum (int): Minimum threshold for alerts.
        date_expiration (date): Expiry date.
        ordonnance_requise (bool): Whether prescription is required.
        est_actif (bool): Soft delete flag — False means archived.
        date_creation (datetime): Auto-set creation timestamp.
    """

    nom = models.CharField(max_length=150, verbose_name="Nom commercial")
    dci = models.CharField(
        max_length=150, blank=True, null=True,
        verbose_name="Dénomination Commune Internationale",
    )
    forme = models.CharField(
        max_length=50, blank=True, null=True,
        verbose_name="Forme galénique",
        help_text="Ex: comprimé, sirop, injection",
    )
    dosage = models.CharField(max_length=20, blank=True, null=True, verbose_name="Dosage")
    prix_achat = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Prix d'achat (MAD)"
    )
    prix_vente = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Prix de vente (MAD)"
    )
    stock_actuel = models.IntegerField(default=0, verbose_name="Stock actuel")
    stock_minimum = models.IntegerField(default=0, verbose_name="Stock minimum")
    date_expiration = models.DateField(
        blank=True, null=True, verbose_name="Date d'expiration"
    )
    ordonnance_requise = models.BooleanField(
        default=False, verbose_name="Ordonnance requise"
    )
    est_actif = models.BooleanField(default=True, verbose_name="Actif")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="medicaments",
        verbose_name="Catégorie",
    )

    class Meta:
        verbose_name = "Médicament"
        verbose_name_plural = "Médicaments"
        ordering = ["nom"]

    def __str__(self) -> str:
        return f"{self.nom} ({self.dosage or '-'})"

    @property
    def is_low_stock(self) -> bool:
        """True when current stock falls at or below the minimum threshold."""
        return self.stock_actuel <= self.stock_minimum

    @property
    def is_expired(self) -> bool:
        """True when expiration date has passed."""
        if not self.date_expiration:
            return False
        return self.date_expiration < timezone.now().date()
