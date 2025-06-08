import aiohttp
from core import log
from core.common import BotCtx
from core.messages.history import append_to_history, delete_from_history, edit_in_history
from aiogram.types import InlineKeyboardMarkup
from aiogram import enums

from core.tasks.listing.redis import redis_key_sequential_listing_load_more_message_content, redis_key_sequential_listing_load_more_message_id


async def send_markdown2(
    ray: int,
    ctx: BotCtx,
    user_id: int,
    message_type: str,
    content: str,
    reply_markup: InlineKeyboardMarkup | None = None,
    related_tasks_ids: list[int] | None = None,
    session: aiohttp.ClientSession | None = None,
):
    telegram_message = await ctx.bot.send_message(
        user_id, content, reply_markup=reply_markup, parse_mode=enums.ParseMode.MARKDOWN_V2
    )

    try:
        await append_to_history(
            ray, user_id, telegram_message.message_id, content, message_type, related_tasks_ids, session
        )
                        # Storing id of the message, that contain the "Load more" button.
                # The content of the message is laos stored in Redis, so it can be edited later,
                # (to cut the button, hwn more tasks has been loaded).
        await ctx.redis.setex(
            redis_key_sequential_listing_load_more_message_id(user_id), 60 * 30, telegram_message.message_id
            )
        await ctx.redis.setex(redis_key_sequential_listing_load_more_message_content(user_id), 60 * 30, content)
           


    except Exception as e:
        log.error(ray, f"Failed to append message to history. Error: {e}")

    return telegram_message


async def update_markdown2(
    ray: int,
    ctx: BotCtx,
    user_id: int,
    message_id: int,
    message_type: str,
    new_content: str,
    reply_markup: InlineKeyboardMarkup | None = None,
    related_tasks_ids: list[int] | None = None,
    session: aiohttp.ClientSession | None = None,
):
    telegram_message = await ctx.bot.edit_message_text(
        text=new_content,
        chat_id=user_id,
        message_id=message_id,
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.MARKDOWN_V2,
    )

    try:
        await edit_in_history(ray, user_id, message_id, new_content, message_type, related_tasks_ids, session=session)
    except Exception as e:
        log.error(ray, f"Failed to edit message in history. Error: {e}")

    return telegram_message


async def delete_message(ray: int, ctx: BotCtx, chat_id: int, message_id: int):
    try:
        await ctx.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        log.error(ray, f"Failed to delete message {message_id}. Error: {e}")

    try:
        await delete_from_history(ray, chat_id, message_id)
    except Exception as e:
        log.error(ray, f"Failed to delete message from history. Error: {e}")
