# Python
from typing import Any

# Rest Framework
from rest_framework.permissions import BasePermission
from rest_framework.request import Request as DRF_Request


class IsSuperUserRequestAdmin(BasePermission):
    """IsNonDeletedUser."""

    message: str = "Нелья создавать администратора, будучи самим не админом!"

    def has_permission(self, request: DRF_Request, view: Any) -> bool:
        """Handle request permissions."""
        is_superuser: bool = request.data.get("is_superuser", False)
        if is_superuser and not request.user.is_superuser:
            return False
        return True


class IsNonDeletedUser(BasePermission):
    """IsNonDeletedUser."""

    message: str = "Вы не можете запрашивать данные, пока ваш аккаунт удалён."

    def has_permission(self, request: DRF_Request, view: Any) -> bool:
        """Handle request permissions."""
        return bool(
            request.user and
            request.user.is_authenticated and
            not request.user.datetime_deleted
        )


class IsConnectedTelegram(BasePermission):
    """IsConnectedTelegram."""

    message: str = "Вам необходимо подключить телеграм для продолжения."

    def has_permission(self, request: DRF_Request, view: Any):
        return True if request.user.telegram_id else False
