"""
ViewSet for Categorie CRUD operations.
"""
import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.categories.serializers import CategorieSerializer
from apps.categories.services import CategorieService
from apps.core.pagination import StandardPagination
from apps.core.permissions import IsPharmacist, IsPharmacistOrReadOnly

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(
        summary="Lister toutes les catégories",
        tags=["Catégories"],
    ),
    create=extend_schema(
        summary="Créer une catégorie",
        tags=["Catégories"],
    ),
    retrieve=extend_schema(
        summary="Détail d'une catégorie",
        tags=["Catégories"],
    ),
    update=extend_schema(
        summary="Mettre à jour une catégorie (PUT)",
        tags=["Catégories"],
    ),
    partial_update=extend_schema(
        summary="Mettre à jour partiellement une catégorie (PATCH)",
        tags=["Catégories"],
    ),
    destroy=extend_schema(
        summary="Supprimer une catégorie",
        tags=["Catégories"],
        responses={204: OpenApiResponse(description="Supprimé avec succès.")},
    ),
)
class CategorieViewSet(ViewSet):
    """
    ViewSet exposing CRUD operations for medication categories.

    - Pharmacists: full access (CRUD).
    - Clients: read-only (list, retrieve).
    """

    permission_classes = [IsPharmacistOrReadOnly]
    pagination_class = StandardPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CategorieService()

    # GET /categories/
    # ------------------------------------------------------------------
    def list(self, request):
        queryset = self.service.list_categories()

        # Manual search
        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(nom__icontains=search)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = CategorieSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = CategorieSerializer(queryset, many=True)
        return Response({"success": True, "results": serializer.data})

    # POST /categories/
    # ------------------------------------------------------------------
    def create(self, request):
        self.check_permissions(request)  # enforce pharmacist-only for writes
        serializer = CategorieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data
        categorie = self.service.create_category(
            nom=validated["nom"],
            description=validated.get("description"),
        )
        out = CategorieSerializer(categorie)
        return Response(
            {"success": True, "data": out.data},
            status=status.HTTP_201_CREATED,
        )

    # GET /categories/{id}/
    # ------------------------------------------------------------------
    def retrieve(self, request, pk=None):
        categorie = self.service.get_category(int(pk))
        serializer = CategorieSerializer(categorie)
        return Response({"success": True, "data": serializer.data})

    # PUT /categories/{id}/
    # ------------------------------------------------------------------
    def update(self, request, pk=None):
        self._require_pharmacist(request)
        categorie = self.service.get_category(int(pk))
        serializer = CategorieSerializer(categorie, data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data
        updated = self.service.update_category(
            pk=int(pk),
            nom=validated.get("nom"),
            description=validated.get("description"),
        )
        return Response({"success": True, "data": CategorieSerializer(updated).data})

    # PATCH /categories/{id}/
    # ------------------------------------------------------------------
    def partial_update(self, request, pk=None):
        self._require_pharmacist(request)
        categorie = self.service.get_category(int(pk))
        serializer = CategorieSerializer(categorie, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data
        updated = self.service.update_category(
            pk=int(pk),
            nom=validated.get("nom"),
            description=validated.get("description"),
        )
        return Response({"success": True, "data": CategorieSerializer(updated).data})

    # DELETE /categories/{id}/
    # ------------------------------------------------------------------
    def destroy(self, request, pk=None):
        self._require_pharmacist(request)
        self.service.delete_category(int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Helpers
    # ------------------------------------------------------------------
    def _require_pharmacist(self, request):
        perm = IsPharmacist()
        if not perm.has_permission(request, self):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(perm.message)
        