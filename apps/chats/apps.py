# Django
from django.apps import AppConfig


class ChatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chats'
    verbose_name: str = "Чаты, сообщения"

    def ready(self) -> None:
        import chats.signals  # noqa
