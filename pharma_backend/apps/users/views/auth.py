"""
Authentication views: register, login, token refresh, logout, me.
"""
import logging

from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.serializers.user import RegisterSerializer, UserSerializer

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    """
    POST /auth/register/
    Create a new user account (no authentication required).
    """

    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses={201: UserSerializer},
        summary="Créer un compte utilisateur",
        tags=["Authentification"],
        examples=[
            OpenApiExample(
                "Exemple",
                value={
                    "username": "jean.dupont",
                    "email": "jean@pharma.ma",
                    "password": "SecurePass123!",
                    "password2": "SecurePass123!",
                    "role": "client",
                },
                request_only=True,
            )
        ],
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = _generate_tokens(user)
        return Response(
            {
                "success": True,
                "message": "Compte créé avec succès.",
                "user": UserSerializer(user).data,
                **tokens,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    """
    POST /auth/login/
    Return access + refresh JWT tokens.
    """

    permission_classes = [AllowAny]

    @extend_schema(
        summary="Se connecter",
        tags=["Authentification"],
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            response.data = {
                "success": True,
                "message": "Connexion réussie.",
                **response.data,
            }
        return response


class LogoutView(APIView):
    """
    POST /auth/logout/
    Blacklist the refresh token.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Se déconnecter",
        tags=["Authentification"],
        request={"application/json": {"type": "object", "properties": {"refresh": {"type": "string"}}}},
        responses={200: None},
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"success": False, "message": "Token de rafraîchissement requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as exc:
            return Response(
                {"success": False, "message": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"success": True, "message": "Déconnexion réussie."})


class MeView(APIView):
    """
    GET /auth/me/
    Return the current authenticated user's profile.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Profil courant",
        tags=["Authentification"],
        responses={200: UserSerializer},
    )
    def get(self, request):
        return Response(
            {"success": True, "data": UserSerializer(request.user).data}
        )


def _generate_tokens(user) -> dict:
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
