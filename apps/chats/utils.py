# Python
from typing import Any

# Django
from asgiref.sync import async_to_sync

# Third party
import telegram
from django.conf import settings


@async_to_sync
async def send_telegram_bot_message(
    msg_content: str,
    chat_id: int,
    user_first_name: str,
    *args: tuple[Any],
    **kwargs: dict[Any, Any]
) -> None:
    """Send message to user via telegram bot."""
    bot: telegram.Bot = telegram.Bot(token=settings.BOT_TOKEN)
    msg: str = f"{user_first_name}, я получил от тебя сообщение:\n{msg_content}"  # noqa
    await bot.send_message(chat_id=chat_id, text=msg)
