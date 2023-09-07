# Python
from typing import (
    Sequence,
    Tuple,
    Union,
    Any,
    Optional,
)

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http.request import HttpRequest

# Project
from auths.models import CustomUser
from abstracts.filters import DeletedStateFilter
from abstracts.admin import AbstractAdminIsDeleted


@admin.register(CustomUser)
class CustomUserAdmin(AbstractAdminIsDeleted, UserAdmin):
    """CustomUser setting on Django admin site."""

    ordering: tuple[str] = ("-datetime_updated", "-id")
    list_display: tuple[str] = (
        "id",
        "login",
        "telegram_id",
        "first_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "get_is_deleted",
    )
    list_display_links: Sequence[str] = (
        "id",
        "telegram_id",
        "login",
    )
    readonly_fields: tuple[str] = (
        "get_is_deleted",
        "datetime_deleted",
        "datetime_created",
        "datetime_updated",
    )
    search_fields: Sequence[str] = (
        "id",
        "first_name",
        "login",
    )
    list_filter: tuple[str, Any] = (
        "is_active",
        "is_staff",
        "is_superuser",
        DeletedStateFilter,
    )
    fieldsets: tuple[tuple[Union[str, dict[str, Any]]]] = (
        (
            "Личная информация",
            {
                "fields": (
                    "login",
                    "first_name",
                    "telegram_id",
                )
            }
        ),
        (
            "Разрешения (Доступы)",
            {
                "fields": (
                    ("is_superuser", "is_staff",),
                    "is_active",
                    "user_permissions",
                )
            }
        ),
        (
            "Данные времени",
            {
                "fields": (
                    "datetime_created",
                    "datetime_updated",
                    "datetime_deleted",
                    "get_is_deleted",
                )
            }
        )
    )
    add_fieldsets: tuple[tuple] = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "login",
                    "first_name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    save_on_top: bool = True
    list_per_page: int = 20

    def get_is_deleted(self, obj: Optional[CustomUser] = None) -> str:
        """Get is deleted state of object."""
        return self.get_is_deleted_obj(obj=obj, obj_name="Пользователь")
    get_is_deleted.short_description = "Состояние"

    def get_readonly_fields(
        self,
        request: HttpRequest,
        obj: Optional[CustomUser] = None
    ) -> Tuple[str]:
        """Get readonly fields as obj is created."""
        if obj:
            return self.readonly_fields + (
                "login",
                "first_name",
                "is_active",
                "is_staff",
                "is_superuser",
            )
        return self.readonly_fields
