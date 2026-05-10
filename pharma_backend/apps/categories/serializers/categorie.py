"""
Serializers for the Categorie resource.
"""
from rest_framework import serializers

from apps.categories.models import Categorie


class CategorieSerializer(serializers.ModelSerializer):
    """Full serializer — used for list, retrieve, create and update."""

    medicaments_count = serializers.SerializerMethodField(
        help_text="Number of active medications in this category."
    )

    class Meta:
        model = Categorie
        fields = ["id", "nom", "description", "medicaments_count"]
        read_only_fields = ["id"]

    def get_medicaments_count(self, obj) -> int:
        """Return the number of active medications in this category."""
        return obj.medicaments.filter(est_actif=True).count()

    def validate_nom(self, value: str) -> str:
        """Ensure the name is unique (case-insensitive)."""
        value = value.strip()
        qs = Categorie.objects.filter(nom__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "Une catégorie avec ce nom existe déjà."
            )
        return value


class CategorieMinimalSerializer(serializers.ModelSerializer):
    """Lightweight serializer used when embedding in other resources."""

    class Meta:
        model = Categorie
        fields = ["id", "nom"]
        read_only_fields = ["id", "nom"]
