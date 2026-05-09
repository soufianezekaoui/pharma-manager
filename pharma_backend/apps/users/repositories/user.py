"""
Repository for User — DB queries only.
"""
from typing import Optional

from django.db.models import QuerySet

from apps.users.models import User


class UserRepository:
    @staticmethod
    def get_all() -> QuerySet:
        return User.objects.all()

    @staticmethod
    def get_by_id(pk: int) -> Optional[User]:
        return User.objects.filter(pk=pk).first()

    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        return User.objects.filter(username=username).first()

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        return User.objects.filter(email=email).first()
