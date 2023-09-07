# Django
from django.db.models import (
    TextField,
    ForeignKey,
    CASCADE,
)

# Project
from abstracts.models import AbstractDateTime
from auths.models import CustomUser
from chats.utils import send_telegram_bot_message


class Message(AbstractDateTime):
    """Message database entity."""

    text: TextField = TextField(
        verbose_name="Тело сообщения (текст)"
    )
    owner: CustomUser = ForeignKey(
        to=CustomUser,
        on_delete=CASCADE,
        related_name="messages",
        verbose_name="Кто написал"
    )

    class Meta:
        """Customization of the Message model class."""

        verbose_name: str = "Сообщение"
        verbose_name_plural: str = "Сообщения"
        ordering: tuple[str] = ("-datetime_updated",)

    def __str__(self) -> str:
        """Override default classes' instance view."""
        return f"{self.text[:50]}..."

    def send_telegram_message(self) -> None:
        """Send message to the telegram chat."""
        if self.owner.telegram_id:
            send_telegram_bot_message(
                msg_content=self.text,
                chat_id=self.owner.telegram_id,
                user_first_name=self.owner.first_name
            )
