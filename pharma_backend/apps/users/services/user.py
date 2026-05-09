"""
Service layer for User management.
"""
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

from apps.users.models import User
from apps.users.repositories.user import UserRepository


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def list_users(self):
        return self.repo.get_all()

    def get_user(self, pk: int) -> User:
        user = self.repo.get_by_id(pk)
        if not user:
            raise NotFound(f"Utilisateur {pk} introuvable.")
        return user

    def change_password(self, user: User, old_password: str, new_password: str) -> None:
        if not user.check_password(old_password):
            raise ValidationError({"old_password": "Mot de passe actuel incorrect."})
        user.set_password(new_password)
        user.save()

    def deactivate_user(self, pk: int, requester: User) -> User:
        if not requester.is_pharmacist:
            raise PermissionDenied("Seul un pharmacien peut désactiver un compte.")
        user = self.get_user(pk)
        user.is_active = False
        user.save()
        return user
