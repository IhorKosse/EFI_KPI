import calendar
from datetime import datetime

from aiogram import types

from core.api.tasks import get_tasks
from core.common import BotCtx, TelegramChatCtx, TelegramUserCtx
from core.i10n.utils import short_days_titles
from core.tasks.listing.common import send_or_update_tasks_listing
from core.tasks.listing.formatting import (
    monthly_listing_header_markdown,
    monthly_listing_tasks_markdown,
)
from core.i10n import tasks_listing as i10n_listing

async def render_monthly_navigation_form(
    ray: int, ctx: BotCtx, chat: TelegramChatCtx, target_day: datetime, now: datetime
):
    user = TelegramUserCtx.from_chat_context(chat)
    message = await __compose_tasks_of_day_message(target_day, now, user)
    keyboard = __compose_monthly_listing_keyboard(target_day, user)

    await send_or_update_tasks_listing(ray, ctx, chat, message, keyboard)


def __compose_monthly_listing_keyboard(
    target_day: datetime, telegram_user: TelegramUserCtx
) -> types.InlineKeyboardMarkup:
    weeks = __generate_calendar(target_day.year, target_day.month)

    buttons = []
    buttons_row = []
    for day in short_days_titles(telegram_user):
        buttons_row.append(types.InlineKeyboardButton(text=day, callback_data=day[1]))
    buttons.append(buttons_row)

    for week in weeks:
        buttons_row = []
        for day in week:
            if day == target_day.date():
                buttons_row.append(types.InlineKeyboardButton(text="🟢", callback_data="tlm_" + day.isoformat()))
            else:
                buttons_row.append(
                    types.InlineKeyboardButton(text=day.strftime("%d"), callback_data="tlm_" + day.isoformat())
                )

        buttons.append(buttons_row)

    buttons.append(
        [
            types.InlineKeyboardButton(text="<<", callback_data="tlm__pm_" + target_day.isoformat()),
            # LOCALIZATION
            types.InlineKeyboardButton(text=i10n_listing.today(), callback_data="tlm__today"),
            types.InlineKeyboardButton(text=">>", callback_data="tlm__nm_" + target_day.isoformat()),
        ]
    )

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def __generate_calendar(year, month):
    # Create a calendar
    cal = calendar.Calendar()

    # Generate dates for the month
    month_dates = list(cal.itermonthdates(year, month))

    # Adjust start and end dates if they don't belong to the target month
    first_day_of_month_index = next(i for i, d in enumerate(month_dates) if d.month == month)
    first_day_of_month = month_dates[first_day_of_month_index - month_dates[first_day_of_month_index].weekday()]

    last_day_of_month_index = (
        len(month_dates) - next(i for i, d in enumerate(month_dates[::-1]) if d.month == month) - 1
    )
    last_day_of_month = month_dates[last_day_of_month_index + 6 - month_dates[last_day_of_month_index].weekday()]

    # Generate the list of strings for each day, grouped by week
    weeks = []
    week = []
    for day in month_dates:
        if first_day_of_month <= day <= last_day_of_month:
            week.append(day)
            if day.weekday() == 6:  # Sunday, end of the week
                weeks.append(week)
                week = []
    # Add the last week if it hasn't been added yet
    if week:
        weeks.append(week)

    return weeks


async def __compose_tasks_of_day_message(day: datetime, now: datetime, user: TelegramUserCtx) -> str:
    after = day.replace(hour=0, minute=0, second=0)
    before = day.replace(hour=23, minute=59, second=59)
    tasks = await get_tasks(user, inbox=False, after=after, before=before, limit=100)

    header = monthly_listing_header_markdown(day, now, len(tasks))
    tasks_content = monthly_listing_tasks_markdown(day, tasks, now)
    return f"{header}{tasks_content}"
