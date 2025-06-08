from aiogram import types
from core.messages.history import fetch

from core.messages.submission import send_markdown2, update_markdown2
from core.common import BotCtx, TelegramChatCtx
from core.messages.types import MESSAGE_TYPE_TASKS_LISTING
from core.tasks.listing.history import delete_listing_messages_from_user_chat
from datetime import datetime, timedelta, timezone


async def send_or_update_tasks_listing(
    rai: int,
    ctx: BotCtx,
    chat: TelegramChatCtx,
    message: str,
    keyboard: types.InlineKeyboardMarkup,
):
    # Fetch the last message in the chat.
    # If the last message is a listing message and was sent less than 20 minutes ago, update it.
    # Otherwise, delete all other listing messages and send a new one.
    response = await fetch(rai, chat_id=chat.user_id, limit=1)
    messages = response.get("results", [])

    if messages:
        last_message = messages[0]

        # Check if the last message is a listing message.
        if last_message.get("type") == MESSAGE_TYPE_TASKS_LISTING:
            message_time = datetime.fromisoformat(last_message.get("created_at"))
            # If the message was sent less than 20 minutes ago, update it
            if datetime.now(timezone.utc) - message_time < timedelta(minutes=1):
                await update_markdown2(
                    rai,
                    ctx,
                    chat.user_id,
                    last_message.get("message_id"),
                    MESSAGE_TYPE_TASKS_LISTING,
                    message,
                    keyboard,
                )

                # Delete all other messages of the same type, if any
                await delete_listing_messages_from_user_chat(
                    rai, ctx, chat.user_id, except_message_id=last_message.get("message_id")
                )
                return

    # If the last message is not a listing message or was sent more than 20 minutes ago,
    # delete all other listing messages and send a new one
    await delete_listing_messages_from_user_chat(rai, ctx, chat.user_id)
    await send_markdown2(rai, ctx, chat.user_id, MESSAGE_TYPE_TASKS_LISTING, message, keyboard)
