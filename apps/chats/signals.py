# Django
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.base import ModelBase

# Project
from chats.models import Message


@receiver(
    signal=post_save,
    sender=Message
)
def post_save_message(
    sender: ModelBase,
    instance: Message,
    created: bool,
    **kwargs: dict
) -> None:
    """Triggers when the Message is created."""
    if created:
        instance.send_telegram_message()
