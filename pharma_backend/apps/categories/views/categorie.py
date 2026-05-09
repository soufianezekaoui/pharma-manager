from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.categories.models import Categorie
from apps.categories.serializers.categorie import CategorieSerializer
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    """
    Custom pagination class for consistent pagination settings.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@extend_schema_view(
    list=extend_schema(
        summary="Retrieve a list of categories",
        description="Returns a paginated list of all categories with optional filtering and search."
    ),
    retrieve=extend_schema(
        summary="Retrieve a single category",
        description="Returns details of a specific category by ID."
    ),
    create=extend_schema(
        summary="Create a new category",
        description="Creates a new category with the provided data."
    ),
    update=extend_schema(
        summary="Update an existing category",
        description="Updates the details of an existing category by ID."
    ),
    partial_update=extend_schema(
        summary="Partially update a category",
        description="Partially updates the details of an existing category by ID."
    ),
    destroy=extend_schema(
        summary="Delete a category",
        description="Deletes a specific category by ID."
    ),
)

class CategorieViewSet(ModelViewSet):
    """
    ViewSet for managing categories in the pharmacy management system.

    Provides CRUD operations, filtering, search, and pagination.
    """
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'description']
    ordering_fields = ['created_at', 'nom']
    ordering = ['-created_at']

    def create(self, request, *args, **kwargs):
        """
        Handle the creation of a new category with proper status codes.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """
        Handle the deletion of a category with proper status codes.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
