# Django
from django.contrib.admin import (
    ModelAdmin,
    register,
)

# Project
from chats.models import Message


@register(Message)
class MessageAdmin(ModelAdmin):
    list_display: tuple[str] = (
        "id",
        "owner",
    )
