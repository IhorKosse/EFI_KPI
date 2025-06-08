from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from core import log
from core.i10n import tasks_listing as i10n
from core.i10n import payments as i10n_payments
from core.common import BotCtx, TelegramMessageCtx, TelegramUserCtx
from core.settings.timezone import create_or_update_timezone_shift
from aiogram import enums

async def process_timezone_update(ctx: BotCtx, ray: int, query: types.CallbackQuery):
    try:
        if query.data:
            if type(query.message) is not types.Message:
                raise ValueError("Callback message is not a Message")

            user = TelegramUserCtx.from_message_context(TelegramMessageCtx(query.message))
            picked_timezone_shift = query.data.split("_")[3]
            await create_or_update_timezone_shift(user, int(picked_timezone_shift))
            await ctx.redis.delete(f"{query.from_user.id}_timezone_chosen")

            response_text = i10n.timezone_update_message(picked_timezone_shift)
            await ctx.bot.send_message(query.from_user.id, response_text)

            # Delete the message "Choose your time zone:" with buttons
            try:
                await ctx.bot.delete_message(query.message.chat.id, query.message.message_id)
            except Exception as e:
                log.warning(ray, f"Failed to delete message with timezone buttons: {e}")
                pass

            await ctx.bot.send_message(
                user.id,
                i10n_payments.free_trial_activated_message(),
                parse_mode=enums.ParseMode.MARKDOWN_V2,
                disable_web_page_preview=True,
            )

            # Send another message to the user with the task prompt and normal buttons
            task_prompt = i10n.task_start_prompt()
            tutorial_start_message = i10n.tutorial_start_message(task_prompt)
            await ctx.bot.send_message(user.id, tutorial_start_message, parse_mode=enums.ParseMode.MARKDOWN_V2, disable_web_page_preview=True)

        else:
            raise ValueError("Callback data is empty")

    except Exception as e:
        error_message = f"Processing of callback query failed with an exception: {e}"
        log.error(ray, error_message)

    finally:
        await query.answer()