from core.common import BotCtx
from core.messages.history import fetch
from core.messages.submission import delete_message
from core.messages.types import MESSAGE_TYPE_TASKS_LISTING


async def delete_listing_messages_from_user_chat(
    ray: int, ctx: BotCtx, chat_id: int, except_message_id: int | None = None
):
    response = await fetch(ray, chat_id=chat_id, message_type=MESSAGE_TYPE_TASKS_LISTING, limit=10)
    messages = response.get("results", [])
    for message in messages:
        if except_message_id and message.get("message_id") == except_message_id:
            continue

        await delete_message(ray, ctx, chat_id, message.get("message_id"))
