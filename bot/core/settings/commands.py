import datetime

from core.common import BotCtx, TelegramMessageCtx, TelegramUserCtx
from core.i10n import tasks_listing as i10n
from core.settings.common import create_settings_menu_keyboard
from core.settings.redis import redis_key_settings_message_id


async def handle_settings_command(ray: int, ctx: BotCtx, input: TelegramMessageCtx):
    # Check if the user has a settings message ID stored in Redis
    user = TelegramUserCtx.from_message_context(input)

    settings_message_id = await ctx.redis.get(redis_key_settings_message_id(user.id))
    if settings_message_id:
        # If the settings message ID exists, try to update the message with the reply markup
        try:
            await ctx.bot.edit_message_reply_markup(
                chat_id=user.id,
                message_id=settings_message_id,
                reply_markup=await create_settings_menu_keyboard(user),
            )
        except Exception:
            # If the message is not modified, ignore the error
            pass
    else:
        # If the settings message ID doesn't exist, create a new message and store its ID in Redis
        reply_markup = await create_settings_menu_keyboard(user)

        text = i10n.settings_menu_text()
        sent_message = await ctx.bot.send_message(chat_id=user.id, text=text, reply_markup=reply_markup)

        await ctx.redis.setex(
            redis_key_settings_message_id(user.id), datetime.timedelta(minutes=30), sent_message.message_id
        )
