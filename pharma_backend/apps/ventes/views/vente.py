"""
ViewSet for Vente CRUD + status management.
"""
import logging

from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.core.pagination import StandardPagination
from apps.core.permissions import IsPharmacist
from apps.ventes.views.filters import VenteFilter
from apps.ventes.serializers.vente import (
    VenteCreateSerializer,
    VenteListSerializer,
    VenteSerializer,
    VenteStatutUpdateSerializer,
)
from apps.ventes.services import VenteService

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(
        summary="Lister les ventes",
        tags=["Ventes"],
        parameters=[
            OpenApiParameter("statut", str, description="Filtrer par statut"),
            OpenApiParameter("date_debut", str, description="Date début (YYYY-MM-DD)"),
            OpenApiParameter("date_fin", str, description="Date fin (YYYY-MM-DD)"),
        ],
    ),
    create=extend_schema(
        summary="Créer une vente",
        tags=["Ventes"],
        description=(
            "Creates a sale with automatic stock deduction. "
            "Provide a list of `{medicament, quantite}` objects in `lignes`."
        ),
    ),
    retrieve=extend_schema(summary="Détail d'une vente", tags=["Ventes"]),
    destroy=extend_schema(summary="Annuler une vente", tags=["Ventes"]),
)
class VenteViewSet(ViewSet):
    """
    ViewSet for sale management.

    - Pharmacists: full access (list all, create, update status, cancel).
    - Clients: create sales + view own sales only.
    """

    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = VenteService()

    # GET /ventes/
    # ------------------------------------------------------------------
    def list(self, request):
        queryset = self.service.list_ventes(request.user)

        # Apply filters
        filterset = VenteFilter(request.GET, queryset=queryset)
        queryset = filterset.qs

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            return paginator.get_paginated_response(
                VenteListSerializer(page, many=True).data
            )
        return Response(
            {"success": True, "results": VenteListSerializer(queryset, many=True).data}
        )

    # POST /ventes/
    # ------------------------------------------------------------------
    def create(self, request):
        serializer = VenteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vente = self.service.create_vente(
            lignes_data=serializer.validated_data["lignes"],
            user=request.user,
            notes=serializer.validated_data.get("notes"),
        )
        return Response(
            {"success": True, "data": VenteSerializer(vente).data},
            status=status.HTTP_201_CREATED,
        )

    # GET /ventes/{id}/
    # ------------------------------------------------------------------
    def retrieve(self, request, pk=None):
        vente = self.service.get_vente(int(pk), request.user)
        return Response({"success": True, "data": VenteSerializer(vente).data})

    # DELETE /ventes/{id}/   → cancel (pharmacist only)
    # ------------------------------------------------------------------
    def destroy(self, request, pk=None):
        self._require_pharmacist(request)
        vente = self.service.update_statut(
            int(pk), new_statut="annulee", user=request.user
        )
        return Response({"success": True, "data": VenteSerializer(vente).data})

    # PATCH /ventes/{id}/statut/
    # ------------------------------------------------------------------
    @extend_schema(
        request=VenteStatutUpdateSerializer,
        responses={200: VenteSerializer},
        summary="Changer le statut d'une vente",
        tags=["Ventes"],
    )
    @action(
        detail=True,
        methods=["patch"],
        url_path="statut",
        permission_classes=[IsPharmacist],
    )
    def update_statut(self, request, pk=None):
        serializer = VenteStatutUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vente = self.service.update_statut(
            int(pk),
            new_statut=serializer.validated_data["statut"],
            user=request.user,
        )
        return Response({"success": True, "data": VenteSerializer(vente).data})

    # GET /ventes/mes-ventes/   — client shortcut
    # ------------------------------------------------------------------
    @extend_schema(
        summary="Mes ventes (client)",
        tags=["Ventes"],
        responses={200: VenteListSerializer(many=True)},
    )
    @action(detail=False, methods=["get"], url_path="mes-ventes")
    def mes_ventes(self, request):
        from apps.ventes.repositories import VenteRepository
        queryset = VenteRepository.get_by_user(request.user.pk)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            return paginator.get_paginated_response(
                VenteListSerializer(page, many=True).data
            )
        return Response(
            {"success": True, "results": VenteListSerializer(queryset, many=True).data}
        )

    # ------------------------------------------------------------------
    def _require_pharmacist(self, request):
        perm = IsPharmacist()
        if not perm.has_permission(request, self):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(perm.message)
