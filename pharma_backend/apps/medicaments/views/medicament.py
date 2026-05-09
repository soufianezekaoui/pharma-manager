"""
ViewSet for Medicament CRUD + special actions.
"""
import logging

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.core.pagination import StandardPagination
from apps.core.permissions import IsPharmacist, IsPharmacistOrReadOnly
from apps.medicaments.views.filters import MedicamentFilter
from apps.medicaments.serializers.medicament import (
    MedicamentSerializer,
    StockUpdateSerializer,
)
from apps.medicaments.services.medicament import MedicamentService

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(
        summary="Lister les médicaments",
        tags=["Médicaments"],
        parameters=[
            OpenApiParameter("search", str, description="Recherche sur nom ou DCI"),
            OpenApiParameter("categorie", int, description="Filtrer par catégorie"),
            OpenApiParameter("est_actif", bool, description="Filtrer par statut actif"),
            OpenApiParameter("stock_bas", bool, description="Afficher uniquement le stock bas"),
        ],
    ),
    create=extend_schema(summary="Créer un médicament", tags=["Médicaments"]),
    retrieve=extend_schema(summary="Détail d'un médicament", tags=["Médicaments"]),
    update=extend_schema(summary="Modifier un médicament (PUT)", tags=["Médicaments"]),
    partial_update=extend_schema(summary="Modifier partiellement (PATCH)", tags=["Médicaments"]),
    destroy=extend_schema(summary="Désactiver un médicament (soft delete)", tags=["Médicaments"]),
)
class MedicamentViewSet(ViewSet):
    """
    CRUD + stock management for medications.

    - Pharmacists: full access.
    - Clients: read-only (list, retrieve).
    """

    permission_classes = [IsPharmacistOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MedicamentFilter
    search_fields = ["nom", "dci"]
    ordering_fields = ["nom", "prix_vente", "stock_actuel", "date_expiration"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = MedicamentService()

    # GET /medicaments/
    # ------------------------------------------------------------------
    def list(self, request):
        active_only = request.query_params.get("est_actif", "true").lower() != "false"
        queryset = self.service.list_medicaments(active_only=active_only)

        # Apply filters manually (ViewSet doesn't auto-apply filter_backends)
        filterset = MedicamentFilter(request.GET, queryset=queryset)
        queryset = filterset.qs

        # Search
        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(nom__icontains=search) | queryset.filter(
                dci__icontains=search
            )

        # Ordering
        ordering = request.query_params.get("ordering", "nom")
        if ordering.lstrip("-") in self.ordering_fields:
            queryset = queryset.order_by(ordering)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            return paginator.get_paginated_response(
                MedicamentSerializer(page, many=True).data
            )
        return Response(
            {"success": True, "results": MedicamentSerializer(queryset, many=True).data}
        )

    # POST /medicaments/
    # ------------------------------------------------------------------
    def create(self, request):
        self._require_pharmacist(request)
        serializer = MedicamentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        medicament = self.service.create_medicament(serializer.validated_data)
        return Response(
            {"success": True, "data": MedicamentSerializer(medicament).data},
            status=status.HTTP_201_CREATED,
        )

    # GET /medicaments/{id}/
    # ------------------------------------------------------------------
    def retrieve(self, request, pk=None):
        medicament = self.service.get_medicament(int(pk))
        return Response({"success": True, "data": MedicamentSerializer(medicament).data})

    # PUT /medicaments/{id}/
    # ------------------------------------------------------------------
    def update(self, request, pk=None):
        self._require_pharmacist(request)
        serializer = MedicamentSerializer(
            self.service.get_medicament(int(pk)), data=request.data
        )
        serializer.is_valid(raise_exception=True)
        updated = self.service.update_medicament(int(pk), serializer.validated_data)
        return Response({"success": True, "data": MedicamentSerializer(updated).data})

    # PATCH /medicaments/{id}/
    # ------------------------------------------------------------------
    def partial_update(self, request, pk=None):
        self._require_pharmacist(request)
        serializer = MedicamentSerializer(
            self.service.get_medicament(int(pk)), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        updated = self.service.update_medicament(int(pk), serializer.validated_data)
        return Response({"success": True, "data": MedicamentSerializer(updated).data})

    # DELETE /medicaments/{id}/   → soft delete
    # ------------------------------------------------------------------
    def destroy(self, request, pk=None):
        self._require_pharmacist(request)
        self.service.soft_delete_medicament(int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)

    # POST /medicaments/{id}/restock/
    # ------------------------------------------------------------------
    @extend_schema(
        request=StockUpdateSerializer,
        responses={200: MedicamentSerializer},
        summary="Réapprovisionner le stock",
        tags=["Médicaments"],
    )
    @action(detail=True, methods=["post"], url_path="restock",
            permission_classes=[IsPharmacist])
    def restock(self, request, pk=None):
        serializer = StockUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated = self.service.restock(int(pk), serializer.validated_data["quantite"])
        return Response({"success": True, "data": MedicamentSerializer(updated).data})

    # GET /medicaments/alertes-stock/
    # ------------------------------------------------------------------
    @extend_schema(
        summary="Médicaments en stock bas",
        tags=["Médicaments"],
        responses={200: MedicamentSerializer(many=True)},
    )
    @action(detail=False, methods=["get"], url_path="alertes-stock",
            permission_classes=[IsPharmacist])
    def alertes_stock(self, request):
        qs = self.service.get_low_stock_alerts()
        return Response(
            {"success": True, "count": qs.count(),
             "results": MedicamentSerializer(qs, many=True).data}
        )

    # GET /medicaments/expires/
    # ------------------------------------------------------------------
    @extend_schema(
        summary="Médicaments expirés",
        tags=["Médicaments"],
        responses={200: MedicamentSerializer(many=True)},
    )
    @action(detail=False, methods=["get"], url_path="expires",
            permission_classes=[IsPharmacist])
    def expires(self, request):
        qs = self.service.get_expired_medications()
        return Response(
            {"success": True, "count": qs.count(),
             "results": MedicamentSerializer(qs, many=True).data}
        )

    # ------------------------------------------------------------------
    def _require_pharmacist(self, request):
        perm = IsPharmacist()
        if not perm.has_permission(request, self):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(perm.message)
