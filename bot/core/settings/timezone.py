import datetime

import aiohttp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from yarl import URL

from core import log
from core import users
from core.common import BotCtx, TelegramUserCtx
from core.i10n import tasks_listing as i10n
from core.i10n.tasks_listing__en import days_short as days_short_en
from core.i10n import payments as i10n_payments
import settings


async def get_timezone_shift(user: TelegramUserCtx) -> int:
    async with aiohttp.ClientSession() as session:
        headers = await users.get_user_api_key_by_chat_id(session, user)
        url = URL(settings.API_BASE_URL).join(URL("user/settings/"))
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            return data.get("timezone_shift")


async def create_or_update_timezone_shift(user: TelegramUserCtx, timezone_shift_hours: int):
    # TODO: Allow session to be reused. Currently, it is created and destroyed for each request.
    async with aiohttp.ClientSession() as session:
        headers = await users.get_user_api_key_by_chat_id(session, user)
        url = URL(settings.API_BASE_URL).join(URL("user/settings/"))
        data = {"timezone_shift": timezone_shift_hours}
        async with session.post(url, json=data, headers=headers) as response:
            if response.content_type == "application/json":
                data = await response.json()
                return data
            else:
                raise ValueError("Unexpected response content type: {}".format(response.content_type))


async def send_timezone_selector(ctx: BotCtx, ray: int, query):
    await ctx.bot.edit_message_text(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        text=i10n.timezone_prompt(),
        reply_markup=await send_timezone_keyboard("settings_timezone_"),
    )


async def send_timezone_keyboard(callback_query: str):
    keyboard = []
    rows = []
    utc_now = datetime.datetime.utcnow()
    # buttons = []
    for offset in range(-12, 13):
        # Calculate time in the current UTC timezone
        offset_time = utc_now + datetime.timedelta(hours=offset)
        # Format time as 24-hour format and include day
        formatted_time = offset_time.strftime("%H:%M") + " " + offset_time.strftime("%a %d")

        # Create a button with the formatted time and offset
        # button_text = f"{formatted_time} (UTC{'' if offset >= 0 else '-'}{abs(offset)})"
        time, _, date = formatted_time.split(" ")
        try:
            day_index = days_short_en().index(_)
            new_day = i10n.days_short()[day_index]
        except ValueError:
            error_message = "Day not found in list"
            log.error(error_message)
        new_formatted_time = " ".join([time, new_day, date])

        button_text = f"{new_formatted_time}"
        button = InlineKeyboardButton(text=button_text, callback_data=f"{callback_query}{offset}")
        rows.append(button)
        if len(rows) == 3:
            keyboard.append(rows)
            rows = []
        if len(keyboard) == 8:
            keyboard.append(rows)
    if callback_query != "settings_timezone_tutorial_":
        keyboard.append([InlineKeyboardButton(text=i10n_payments.back(), callback_data="back_to_settings")])

    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return reply_markup
