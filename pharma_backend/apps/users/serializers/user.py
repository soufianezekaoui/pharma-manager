"""
Serializers for User registration, profile and listing.
"""
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.users.models.user import User, UserRole


class RegisterSerializer(serializers.ModelSerializer):
    """Handles new user registration with password confirmation."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label="Confirmer le mot de passe",
        style={"input_type": "password"},
    )
    role = serializers.ChoiceField(
        choices=UserRole.choices,
        default=UserRole.CLIENT,
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "password2", "role"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password2"):
            raise serializers.ValidationError(
                {"password2": "Les mots de passe ne correspondent pas."}
            )
        validate_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data.get("role", UserRole.CLIENT),
        )


class UserSerializer(serializers.ModelSerializer):
    """Read-only user profile serializer."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "is_active", "date_joined"]
        read_only_fields = ["id", "date_joined"]


class UserUpdateSerializer(serializers.ModelSerializer):
    """Allow pharmacists or the user themselves to update profile."""

    class Meta:
        model = User
        fields = ["email", "role", "is_active"]

    def validate_role(self, value):
        # Only pharmacists can promote other users
        request = self.context.get("request")
        if request and not request.user.is_pharmacist and value == UserRole.PHARMACIST:
            raise serializers.ValidationError(
                "Seul un pharmacien peut attribuer le rôle pharmacien."
            )
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """Allow authenticated users to change their own password."""

    old_password = serializers.CharField(required=True, style={"input_type": "password"})
    new_password = serializers.CharField(required=True, style={"input_type": "password"})
    new_password2 = serializers.CharField(required=True, style={"input_type": "password"})

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError(
                {"new_password2": "Les nouveaux mots de passe ne correspondent pas."}
            )
        validate_password(attrs["new_password"])
        return attrs
    
