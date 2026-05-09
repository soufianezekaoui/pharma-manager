from rest_framework import serializers
from apps.categories.models import Categorie

class CategorieSerializer(serializers.ModelSerializer):
    """
    Serializer for the Categorie model.

    Provides validation and serialization for the Categorie model fields.
    """

    class Meta:
        model = Categorie
        fields = ['id', 'nom', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_nom(self, value):
        """
        Validate the 'nom' field to ensure it is not empty and meets requirements.
        """
        if not value.strip():
            raise serializers.ValidationError("The category name cannot be empty.")
        if len(value) > 255:
            raise serializers.ValidationError("The category name must not exceed 255 characters.")
        return value
    
