"""
User management ViewSet (pharmacist-facing admin operations).
"""
import logging

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.core.pagination import StandardPagination
from apps.core.permissions import IsPharmacist
from apps.users.serializers.user import (
    ChangePasswordSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from apps.users.services import UserService

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(summary="Lister les utilisateurs", tags=["Utilisateurs"]),
    retrieve=extend_schema(summary="Détail utilisateur", tags=["Utilisateurs"]),
    partial_update=extend_schema(summary="Modifier un utilisateur", tags=["Utilisateurs"]),
    destroy=extend_schema(summary="Désactiver un utilisateur", tags=["Utilisateurs"]),
)
class UserViewSet(ViewSet):
    """
    ViewSet for user management — pharmacist only.
    Clients can only view their own profile via /auth/me/.
    """

    permission_classes = [IsPharmacist]
    pagination_class = StandardPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UserService()

    def list(self, request):
        queryset = self.service.list_users()

        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(username__icontains=search)

        role = request.query_params.get("role")
        if role:
            queryset = queryset.filter(role=role)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            return paginator.get_paginated_response(UserSerializer(page, many=True).data)
        return Response({"success": True, "results": UserSerializer(queryset, many=True).data})

    def retrieve(self, request, pk=None):
        user = self.service.get_user(int(pk))
        return Response({"success": True, "data": UserSerializer(user).data})

    def partial_update(self, request, pk=None):
        user = self.service.get_user(int(pk))
        serializer = UserUpdateSerializer(user, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "data": UserSerializer(user).data})

    def destroy(self, request, pk=None):
        user = self.service.deactivate_user(int(pk), requester=request.user)
        return Response({"success": True, "data": UserSerializer(user).data})

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: None},
        summary="Changer son mot de passe",
        tags=["Utilisateurs"],
    )
    @action(detail=False, methods=["post"], url_path="change-password",
            permission_classes=[])  # authenticated users only
    def change_password(self, request):
        from rest_framework.permissions import IsAuthenticated
        if not IsAuthenticated().has_permission(request, self):
            from rest_framework.exceptions import NotAuthenticated
            raise NotAuthenticated()

        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.change_password(
            user=request.user,
            old_password=serializer.validated_data["old_password"],
            new_password=serializer.validated_data["new_password"],
        )
        return Response({"success": True, "message": "Mot de passe modifié avec succès."})
    
