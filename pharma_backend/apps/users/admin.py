"""Admin registration for User."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "email", "role", "is_active", "date_joined"]
    list_filter = ["role", "is_active"]
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Rôle & Accès", {"fields": ("role", "is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("username", "email", "password1", "password2", "role")}),
    )
    search_fields = ["username", "email"]
    ordering = ["username"]
