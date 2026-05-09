"""
Serializers for Vente and LigneVente resources.
"""
from rest_framework import serializers

from apps.medicaments.serializers import MedicamentMinimalSerializer
from apps.users.serializers import UserSerializer
from apps.ventes.models import LigneVente, Vente, VenteStatut


# LigneVente
# ---------------------------------------------------------------------------
class LigneVenteCreateSerializer(serializers.Serializer):
    """Used only on Vente creation — accepts medicament id + quantite."""

    medicament = serializers.IntegerField(min_value=1)
    quantite = serializers.IntegerField(min_value=1)


class LigneVenteSerializer(serializers.ModelSerializer):
    """Full read serializer for a LigneVente line item."""

    medicament_detail = MedicamentMinimalSerializer(source="medicament", read_only=True)

    class Meta:
        model = LigneVente
        fields = [
            "id",
            "medicament",
            "medicament_detail",
            "quantite",
            "prix_unitaire",
            "sous_total",
        ]
        read_only_fields = ["id", "prix_unitaire", "sous_total", "medicament_detail"]


# Vente
# ---------------------------------------------------------------------------
class VenteCreateSerializer(serializers.Serializer):
    """
    Input serializer for creating a new Vente with its lines.

    Expected payload:
    {
        "notes": "optional note",
        "lignes": [
            {"medicament": 1, "quantite": 3},
            {"medicament": 4, "quantite": 1}
        ]
    }
    """

    notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    lignes = LigneVenteCreateSerializer(many=True, min_length=1)

    def validate_lignes(self, value):
        # Prevent duplicate medicament entries in the same sale
        med_ids = [item["medicament"] for item in value]
        if len(med_ids) != len(set(med_ids)):
            raise serializers.ValidationError(
                "Un médicament ne peut apparaître qu'une seule fois par vente."
            )
        return value


class VenteSerializer(serializers.ModelSerializer):
    """Full read serializer for Vente — includes nested lines and creator."""

    lignes = LigneVenteSerializer(many=True, read_only=True)
    created_by_detail = UserSerializer(source="created_by", read_only=True)
    statut_display = serializers.CharField(source="get_statut_display", read_only=True)

    class Meta:
        model = Vente
        fields = [
            "id",
            "reference",
            "date_vente",
            "total_ttc",
            "statut",
            "statut_display",
            "notes",
            "created_by",
            "created_by_detail",
            "lignes",
        ]
        read_only_fields = [
            "id", "reference", "date_vente", "total_ttc",
            "created_by", "created_by_detail", "statut_display",
        ]


class VenteListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views — no nested lines."""

    statut_display = serializers.CharField(source="get_statut_display", read_only=True)
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )

    class Meta:
        model = Vente
        fields = [
            "id",
            "reference",
            "date_vente",
            "total_ttc",
            "statut",
            "statut_display",
            "created_by_username",
        ]


class VenteStatutUpdateSerializer(serializers.Serializer):
    """Used for PATCH /ventes/{id}/statut/ — change status only."""

    statut = serializers.ChoiceField(choices=VenteStatut.choices)

