"""
Reusable permission classes for role-based access control.
"""
from rest_framework.permissions import BasePermission


class IsPharmacist(BasePermission):
    """Allow access only to users with the 'pharmacist' role."""

    message = "Accès réservé aux pharmaciens."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "pharmacist"
        )


class IsClient(BasePermission):
    """Allow access only to users with the 'client' role."""

    message = "Accès réservé aux clients."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "client"
        )


class IsPharmacistOrReadOnly(BasePermission):
    """
    Pharmacists have full access.
    Authenticated clients have read-only access.
    """

    message = "Les modifications sont réservées aux pharmaciens."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return request.user.role == "pharmacist"
    
