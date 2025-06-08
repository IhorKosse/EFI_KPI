from datetime import datetime, timedelta

from aiogram import types

from core.api.tasks import get_tasks
from core.common import BotCtx, TelegramChatCtx, TelegramUserCtx
from core.responses import name_of_day
from core.tasks.listing.common import send_or_update_tasks_listing
from core.tasks.listing.formatting import (
    weekly_listing_header_markdown,
    weekly_listing_tasks_markdown,
)


async def render_weekly_tasks_navigation(
    rai: int, ctx: BotCtx, chat: TelegramChatCtx, target_day: datetime, now: datetime
):
    user = TelegramUserCtx.from_chat_context(chat)
    message = await __compose_tasks_of_day_message(target_day, now, user)
    keyboard = __compose_weekly_listing_keyboard(target_day)
    await send_or_update_tasks_listing(rai, ctx, chat, message, keyboard)


def __compose_weekly_listing_keyboard(
    day: datetime,
) -> types.InlineKeyboardMarkup:
    day_per_row = 3

    # TODO: Support changing first day of the week depending on locale.
    first_day_of_the_week = day - timedelta(days=day.weekday())
    last_day_of_the_week = first_day_of_the_week + timedelta(days=6)

    navigation = [
        # [
        #     "✏️ Редагувати (показати по-задачно)"
        # ],
        [
            [
                __format_day_navigation_button_according_to_target_day(
                    day, first_day_of_the_week + timedelta(days=i + day_per_row * 0)
                ),
                f"tlw_{(first_day_of_the_week + timedelta(days=i + day_per_row * 0)).isoformat()}",
            ]
            for i in range(day_per_row)
        ],
        [
            [
                __format_day_navigation_button_according_to_target_day(
                    day, first_day_of_the_week + timedelta(days=i + day_per_row * 1)
                ),
                f"tlw_{(first_day_of_the_week + timedelta(days=i + day_per_row * 1)).isoformat()}",
            ]
            for i in range(day_per_row)
        ],
        [
            [
                __format_day_navigation_button_according_to_target_day(day, last_day_of_the_week),
                f"tlw_{last_day_of_the_week.isoformat()}",
            ],
            ["<< 🗓", f"tlw__pw_{first_day_of_the_week.isoformat()}"],
            ["🗓 >>", f"tlw__nw_{last_day_of_the_week.isoformat()}"],
        ],
    ]

    buttons = []
    for row in navigation:
        buttons_row = []
        for navigation_btn in row:
            buttons_row.append(types.InlineKeyboardButton(text=navigation_btn[0], callback_data=navigation_btn[1]))
        buttons.append(buttons_row)

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def __compose_tasks_of_day_message(day: datetime, now: datetime, user: TelegramUserCtx) -> str:
    after = day.replace(hour=0, minute=0, second=0)
    before = day.replace(hour=23, minute=59, second=59)
    tasks = await get_tasks(user, inbox=False, after=after, before=before, limit=100)

    header = weekly_listing_header_markdown(day, now, len(tasks))
    tasks_content = weekly_listing_tasks_markdown(day, tasks, now)
    return f"{header}{tasks_content}"


def __format_day_navigation_button_according_to_target_day(target_day: datetime, day: datetime) -> str:
    # LOCALIZATION
    day_name = name_of_day(day.weekday(), short=True)
    button_title = f"{day_name}"

    total_tasks_count = 0
    if total_tasks_count > 0:
        button_title += f" — {total_tasks_count}"

    if day.date() < target_day.date():
        return f"{button_title}"
    elif day.date() == target_day.date():
        return f"🟢 {button_title}"
    else:
        return f"{button_title}"
