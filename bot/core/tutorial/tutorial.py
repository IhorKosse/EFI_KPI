from aiogram import types
from aiogram.enums import ParseMode
from aiogram.types import KeyboardButton, Message, ReplyKeyboardRemove

from core import log
from core.common import BotCtx, TelegramMessageCtx
from core.i10n import tasks_listing as i10n
from core.settings.timezone import send_timezone_keyboard


async def handle_task_completion(ctx: BotCtx, ray: int, user_id: int):
    try:
        i10n.task_completion_prompt()
        # Send a message to the user to notify them about the task completion
        task_prompt = i10n.task_completion_prompt()
        close_tutorial = i10n.close_tutorial()
        reply_markup = ReplyKeyboardRemove(
            keyboard=[[KeyboardButton(text=task_prompt)], [KeyboardButton(text=close_tutorial)]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        await ctx.bot.send_message(
            user_id,
            i10n.task_completion_message(task_prompt),
            reply_markup=reply_markup,
        )
    except Exception as e:
        error_message = f"Processing of task completion failed with an exception: {e}"
        log.error(ray, error_message)
        raise e


async def handle_task_update(ctx: BotCtx, ray: int, user_id: int):
    try:
        # Send a message to the user to notify them about the task completion
        task_prompt = i10n.task_update_prompt()
        close_tutorial = i10n.close_tutorial()
        reply_markup = ReplyKeyboardRemove(
            keyboard=[[KeyboardButton(text=task_prompt)], [KeyboardButton(text=close_tutorial)]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        await ctx.bot.send_message(
            user_id,
            i10n.task_update_message(task_prompt),
            reply_markup=reply_markup,
        )

    except Exception as e:
        error_message = f"Processing of task completion failed with an exception: {e}"
        log.error(ray, error_message)
        raise e


async def handle_task_close(ctx: BotCtx, ray: int, user_id: int):
    try:
        # Send a message to the user to notify them about the task completion

        await ctx.bot.send_message(
            user_id,
            i10n.task_close_message(),
            reply_markup=types.ReplyKeyboardRemove(),
        )

    except Exception as e:
        error_message = f"Processing of task completion failed with an exception: {e}"
        log.error(ray, error_message)
        raise e


async def send_timezone(message: Message):
    reply_markup = await send_timezone_keyboard("settings_timezone_tutorial_")
    await message.answer(i10n.timezone_prompt(), reply_markup=reply_markup)


async def close_tutorial(input: TelegramMessageCtx):
    try:
        text = i10n.tutorial_complete_message()
        await input.message.answer(text, parse_mode=ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())
    except Exception:
        pass
    return
