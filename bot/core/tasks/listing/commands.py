import datetime

from core import timeutils
from core.common import BotCtx, TelegramChatCtx, TelegramMessageCtx, TelegramUserCtx
from core.i10n import tasks_listing as i10n
from core.i10n.utils import get_first_day_of_the_week
from core.tasks.listing.listing_monthly import render_monthly_navigation_form
from core.tasks.listing.listing_sequential import render_sequential_tasks_navigation
from core.tasks.listing.listing_weekly import render_weekly_tasks_navigation


async def list_inbox_tasks_sequentially(ray: int, ctx: BotCtx, input: TelegramMessageCtx):
    chat = TelegramChatCtx.from_message_context(input)
    user = TelegramUserCtx.from_chat_context(chat)
    now = await timeutils.now_according_to_users_timezone(user)
    await render_sequential_tasks_navigation(ray, ctx, chat, after=None, before=None, now=now, inbox=True)


async def list_all_tasks_sequentially(ray: int, ctx: BotCtx, input: TelegramMessageCtx):
    chat = TelegramChatCtx.from_message_context(input)
    user = TelegramUserCtx.from_chat_context(chat)
    now = await timeutils.now_according_to_users_timezone(user)
    await render_sequential_tasks_navigation(ray, ctx, chat, after=None, before=None, now=now, all_tasks_listing=True)


async def list_today_tasks_sequentially(ray: int, ctx: BotCtx, input: TelegramMessageCtx):
    chat = TelegramChatCtx.from_message_context(input)
    user = TelegramUserCtx.from_chat_context(chat)
    now = await timeutils.now_according_to_users_timezone(user)
    after = now.replace(hour=0, minute=0, second=0, microsecond=0)
    before = now.replace(hour=23, minute=59, second=59, microsecond=999)
    await render_sequential_tasks_navigation(ray, ctx, chat, after, before, now)


async def list_tommorow_tasks_sequentially(ray: int, ctx: BotCtx, input: TelegramMessageCtx):
    chat = TelegramChatCtx.from_message_context(input)
    user = TelegramUserCtx.from_chat_context(chat)
    now = await timeutils.now_according_to_users_timezone(user)
    tomorrow = now + datetime.timedelta(days=1)
    after = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    before = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999)
    await render_sequential_tasks_navigation(ray, ctx, chat, after, before, now)



async def list_week_tasks(ray: int, ctx: BotCtx, input: TelegramMessageCtx):
    """
    Renders tasks navigation list for current week, starting from current day.
    """

    chat = TelegramChatCtx.from_message_context(input)
    user = TelegramUserCtx.from_chat_context(chat)
    now = await timeutils.now_according_to_users_timezone(user)
    await render_weekly_tasks_navigation(ray, ctx, chat, now, now)


async def list_next_week_tasks(ray: int, ctx: BotCtx, input: TelegramMessageCtx):
    """
    Renders tasks navigation list for the next week,
    starting from the FIRST DAY of the next week.
    """

    chat = TelegramChatCtx.from_message_context(input)
    user = TelegramUserCtx.from_chat_context(chat)
    now = today = await timeutils.now_according_to_users_timezone(user)

    # Calculate how many days to add to get to the next Monday.
    # TODO: Test this logic!
    #       Separated test case is needed to be added in Notion!
    days_to_add = (7 - today.weekday()) % 7
    if days_to_add == 0:
        days_to_add = 7  # If today is Monday, we still want the next Monday.
    target_date = today + datetime.timedelta(days=days_to_add)

    # LOCALIZATION: Determining first day of the week for the user.
    first_weekday = get_first_day_of_the_week(TelegramUserCtx.from_message_context(input))
    # index 6 == SUN
    if first_weekday == i10n.days_short()[6]:
        target_date = target_date - datetime.timedelta(days=1)

    await render_weekly_tasks_navigation(ray, ctx, chat, target_date, now)


async def list_workweek_tasks(ray: int, ctx: BotCtx, input: TelegramMessageCtx):
    """
    Renders tasks navigation list for the current workweek,
    starting from today or from the first day of the workweek if today is a weekend.
    """

    # TODO: Test this logic!
    #       Separated test case is needed to be added in Notion!

    chat = TelegramChatCtx.from_message_context(input)
    user = TelegramUserCtx.from_chat_context(chat)
    now = today = await timeutils.now_according_to_users_timezone(user)
    today_week_day_number = today.isocalendar()[2]

    if today_week_day_number > 5:
        # Today is the weekend.
        # Target date must be shifted to the first day of the next workweek.
        target_date = today + datetime.timedelta(days=8 - today_week_day_number)
    else:
        # Today is a workday.
        # No need to shift the target date to the first day of the week.
        # It is better to show tasks to the user starting from today.
        target_date = today

    await render_weekly_tasks_navigation(ray, ctx, chat, target_date, now)


async def list_month_tasks(ray: int, ctx: BotCtx, input: TelegramMessageCtx):
    """
    Renders tasks navigation list for current month, starting from current day.
    """

    chat = TelegramChatCtx.from_message_context(input)
    user = TelegramUserCtx.from_chat_context(chat)
    now = await timeutils.now_according_to_users_timezone(user)
    await render_monthly_navigation_form(ray, ctx, chat, now, now)


async def list_next_month_tasks(ray: int, ctx: BotCtx, input: TelegramMessageCtx):
    """
    Renders tasks navigation list for the next month,
    starting from the FIRST DAY of the next month.
    """

    chat = TelegramChatCtx.from_message_context(input)
    user = TelegramUserCtx.from_chat_context(chat)
    now = today = await timeutils.now_according_to_users_timezone(user)
    next_month = today + datetime.timedelta(days=30)
    target_date = datetime.datetime(next_month.year, next_month.month, 1, next_month.hour ,next_month.minute, next_month.second)
    await render_monthly_navigation_form(ray, ctx, chat, target_date, now)
