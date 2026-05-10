"""
Custom User model with role-based access.
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserRole(models.TextChoices):
    PHARMACIST = "pharmacist", "Pharmacien"
    CLIENT = "client", "Client"


class UserManager(BaseUserManager):
    """Manager for the custom User model."""

    def create_user(self, username, email, password=None, role=UserRole.CLIENT, **extra):
        if not email:
            raise ValueError("L'adresse email est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra):
        extra.setdefault("role", UserRole.PHARMACIST)
        user = self.create_user(username, email, password, **extra)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Application user.

    Roles:
        - pharmacist: full management access.
        - client: read-only and own-sales access.
    """

    username = models.CharField(
        max_length=100, unique=True, verbose_name="Nom d'utilisateur",
    )
    email = models.EmailField(
        max_length=150, unique=True, verbose_name="Adresse email",
    )
    role = models.CharField(
        max_length=30, choices=UserRole.choices,
        default=UserRole.CLIENT, verbose_name="Rôle",
    )
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_staff = models.BooleanField(default=False, verbose_name="Staff")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ["username"]

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"

    @property
    def is_pharmacist(self) -> bool:
        return self.role == UserRole.PHARMACIST

    @property
    def is_client(self) -> bool:
        return self.role == UserRole.CLIENT
