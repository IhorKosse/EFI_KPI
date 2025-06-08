from aiogram.types import CallbackQuery, InaccessibleMessage

from core import log
from core.i10n import tasks_listing as i10n
from core.common import BotCtx, TelegramMessageCtx, TelegramUserCtx
from core.settings.common import create_settings_menu_keyboard
from core.settings.timezone import create_or_update_timezone_shift

from core.settings.common import __internal_reminders_cache, create_settings_menu_keyboard


async def settings_menu(ctx: BotCtx, ray: int, query: CallbackQuery):
    if not query.message or type(query.message) is InaccessibleMessage:
        raise ValueError("Callback message is empty or inaccessible")

    user = TelegramUserCtx.from_message_context(TelegramMessageCtx(query.message)) # type: ignore  # query.message is already checked to not to be InaccessibleMessage, but mypy doesn't understand it.
    reply_markup = await create_settings_menu_keyboard(user)
   
    text = i10n.settings_menu_text()
    await ctx.bot.edit_message_text(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        text=text,
        reply_markup=reply_markup,
    )


async def handle_callback_timezone(ctx: BotCtx, ray: int, query: CallbackQuery):
    try:
        if not query.data:
            raise ValueError("Callback data is empty")
        
        if not query.message or type(query.message) is InaccessibleMessage:
            raise ValueError("Callback message is empty or inaccessible")

        picked_timezone_shift_hours = int(query.data.split("_")[2])
        user = TelegramUserCtx.from_message_context(TelegramMessageCtx(query.message)) # type: ignore  # query.message is already checked to not to be InaccessibleMessage, but mypy doesn't understand it.
        await create_or_update_timezone_shift(user, picked_timezone_shift_hours)

        response_text = i10n.settings_timezone_update_message(picked_timezone_shift_hours)
        await query.answer(response_text)
        await settings_menu(ctx,ray, query)

    except Exception as e:
        # `finally` section is not used here 
        # because the try..catch section responds with CUSTOM notification in query.answer()
        await query.answer()

        error_message = f"Processing of callback query failed with an exception: {e}"
        log.error(ray, error_message)
        raise e


async def handle_change_reminder(ctx: BotCtx, ray: int, query: CallbackQuery):
    user_id = query.from_user.id
    current_setting = __internal_reminders_cache.get(user_id, i10n.auto_reminders_on())

    # Define the order of reminder settings
    reminder_options = [
        i10n.auto_reminders_on(),
        i10n.auto_reminders_off(),
        i10n.auto_reminders_15(),
        i10n.auto_reminders_30(),
        i10n.auto_reminders_60(),
    ]

    # Find the next reminder setting
    next_index = (reminder_options.index(current_setting) + 1) % len(reminder_options)
    next_setting = reminder_options[next_index]

    # Update the reminder setting in the cache
    __internal_reminders_cache[user_id] = next_setting

    # Update the settings menu to reflect the new reminder setting
    reply_markup = await create_settings_menu_keyboard(TelegramUserCtx(id=user_id))
    await ctx.bot.edit_message_reply_markup(chat_id=user_id, message_id=query.message.message_id, reply_markup=reply_markup)

    await query.answer()