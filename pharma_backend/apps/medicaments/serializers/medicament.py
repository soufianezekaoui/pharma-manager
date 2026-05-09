"""
Serializers for the Medicament resource.
"""
from django.utils import timezone
from rest_framework import serializers

from apps.categories.serializers.categorie import CategorieMinimalSerializer
from apps.medicaments.models import Medicament


class MedicamentSerializer(serializers.ModelSerializer):
    """Full serializer for read operations — includes computed fields."""

    categorie_detail = CategorieMinimalSerializer(source="categorie", read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = Medicament
        fields = [
            "id",
            "nom",
            "dci",
            "forme",
            "dosage",
            "prix_achat",
            "prix_vente",
            "stock_actuel",
            "stock_minimum",
            "date_expiration",
            "ordonnance_requise",
            "est_actif",
            "date_creation",
            "categorie",
            "categorie_detail",
            "is_low_stock",
            "is_expired",
        ]
        read_only_fields = ["id", "date_creation", "categorie_detail", "is_low_stock", "is_expired"]

    def validate_prix_achat(self, value):
        if value < 0:
            raise serializers.ValidationError("Le prix d'achat ne peut pas être négatif.")
        return value

    def validate_prix_vente(self, value):
        if value < 0:
            raise serializers.ValidationError("Le prix de vente ne peut pas être négatif.")
        return value

    def validate_stock_actuel(self, value):
        if value < 0:
            raise serializers.ValidationError("Le stock actuel ne peut pas être négatif.")
        return value

    def validate_stock_minimum(self, value):
        if value < 0:
            raise serializers.ValidationError("Le stock minimum ne peut pas être négatif.")
        return value

    def validate_date_expiration(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError(
                "La date d'expiration ne peut pas être dans le passé lors de la création."
            )
        return value

    def validate(self, attrs):
        prix_achat = attrs.get("prix_achat", getattr(self.instance, "prix_achat", 0))
        prix_vente = attrs.get("prix_vente", getattr(self.instance, "prix_vente", 0))
        if prix_vente < prix_achat:
            raise serializers.ValidationError(
                {"prix_vente": "Le prix de vente doit être supérieur ou égal au prix d'achat."}
            )
        return attrs


class MedicamentMinimalSerializer(serializers.ModelSerializer):
    """Lightweight — used inside LigneVente."""

    class Meta:
        model = Medicament
        fields = ["id", "nom", "dosage", "prix_vente"]
        read_only_fields = fields


class StockUpdateSerializer(serializers.Serializer):
    """Dedicated serializer for stock adjustment endpoint."""

    quantite = serializers.IntegerField(min_value=1, help_text="Quantity to add to current stock.")
