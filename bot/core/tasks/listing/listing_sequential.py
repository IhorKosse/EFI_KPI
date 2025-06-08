from datetime import datetime

from aiogram import enums, types

from core.api.tasks import get_tasks
from core.common import BotCtx, TelegramChatCtx, TelegramUserCtx
from core.i10n import tasks_listing as i10n
from core.messages.submission import send_markdown2
from core.messages.types import MESSAGE_TYPE_TASKS_LISTING_SEQUENTIAL
from core.tasks.listing.formatting import (
    sequential_listing_dates_splitter_header,
    to_message,
)
from core.tasks.listing.history import delete_listing_messages_from_user_chat
from core.tasks.listing.redis import (
    redis_key_sequential_listing_last_header_date,
    redis_key_sequential_listing_load_more_message_content,
    redis_key_sequential_listing_load_more_message_id,
    redis_key_sequential_listing_offset,
)
from settings_dev import BOT_TASKS_LISTING_LIMIT_PER_PAGE


# TODO: Support ordering by date, priority, etc.
# TODO: Make AI capable of using this sorting and ordering.
async def render_sequential_tasks_navigation(
    ray: int,
    ctx: BotCtx,
    chat: TelegramChatCtx,
    after: datetime | None,
    before: datetime | None,
    now: datetime,
    inbox: bool = False,
    continue_previous_listing: bool = False,
    all_tasks_listing: bool = False
):
    # Drop other listing messages from the chat.
    await delete_listing_messages_from_user_chat(ray, ctx, chat.user_id)

    offset = 0
    if not continue_previous_listing:
        # Refresh internal listing parameters.
        await ctx.redis.delete(redis_key_sequential_listing_offset(chat.user_id))
        await ctx.redis.delete(redis_key_sequential_listing_last_header_date(chat.user_id))

    else:
        load_more_msg_id = await ctx.redis.get(redis_key_sequential_listing_load_more_message_id(chat.user_id))
        if load_more_msg_id:
            message_content = await ctx.redis.get(redis_key_sequential_listing_load_more_message_content(chat.user_id))
            if message_content:
                await ctx.bot.edit_message_text(
                    chat_id=chat.user_id,
                    message_id=load_more_msg_id.decode("utf-8"),
                    text=message_content.decode("utf-8"),
                    parse_mode=enums.ParseMode.MARKDOWN_V2,
                )

        offset_raw = await ctx.redis.get(redis_key_sequential_listing_offset(chat.user_id))
        offset = int(offset_raw.decode("utf-8")) if offset_raw else 0

    last_header_date_printed = await ctx.redis.get(redis_key_sequential_listing_last_header_date(chat.user_id))
    if last_header_date_printed:
        last_header_date_printed = datetime.fromisoformat(last_header_date_printed.decode("utf-8")).date()

    limit = BOT_TASKS_LISTING_LIMIT_PER_PAGE
    # limit = 1     # Dev usage only

    user = TelegramUserCtx.from_chat_context(chat)
    before = before.replace(hour=23, minute=59, second=59) if before else None
    tasks = await get_tasks(user, after=after, before=before, limit=limit, offset=offset, inbox=inbox, listing_sequential=True)
    if not tasks:
        response = i10n.no_tasks_in_inbox() if inbox else i10n.no_tasks()
        await send_markdown2(ray, ctx, chat.user_id, "regular", response)
        return

    tasks_count = len(tasks)


    tasks_sent = False
    for i, task in enumerate(tasks):
        
        #TODO: Eugene Kusiak Fix Or Drop
        if all_tasks_listing is True:
            if before is None:
                task_deadline = None
                if "deadline_date" in task and task["deadline_date"] is not None:
                    task_deadline = datetime.strptime(task["deadline_date"], "%Y-%m-%d")

                if "deadline_datetime" in task and task["deadline_datetime"] is not None:
                    task_deadline = datetime.strptime(task["deadline_datetime"], "%Y-%m-%dT%H:%M:%S%z")
                    task_deadline = task_deadline.date()

                

            # If task has a deadline and it's the first task of the day — show the date message first.
            # That will help user to navigate through the tasks.
            if task_deadline:
                try:
                    task_deadline = task_deadline.date()
                except:
                    pass
                if not last_header_date_printed or last_header_date_printed < task_deadline:
                    header_message = sequential_listing_dates_splitter_header(task_deadline)
                    last_header_date_printed = task_deadline
                    await send_markdown2(ray, ctx, chat.user_id, "regular", header_message)
                    await ctx.redis.setex(
                        redis_key_sequential_listing_last_header_date(user.id),
                        60 * 30,
                        last_header_date_printed.isoformat(),
                    )

        if task.get("status") == "closed":
            continue

        # LOCALIZATION
        message = await to_message(task, now)
        last_iteration = i == tasks_count - 1
        keyboard = None
        if last_iteration:
            if tasks.more_available is True:
                after_date_anchor = "NONE"
                if after:
                    after_date_anchor = after.date().isoformat()

                before_date_anchor = "NONE"
                if before:
                    before_date_anchor = before.date().isoformat()

                # attach inline keyboard keyboard to the message to load more
                if inbox is True:
                    keyboard = types.InlineKeyboardMarkup(
                        # LOCALIZATION
                        inline_keyboard=[
                            [
                                types.InlineKeyboardButton(
                                    text=i10n.load_more_tasks(),
                                    callback_data=f"tls__next__inbox__{after_date_anchor}__{before_date_anchor}",
                                )
                            ]
                        ]
                    )
                elif all_tasks_listing is True:
                    keyboard = types.InlineKeyboardMarkup(
                        # LOCALIZATION
                        inline_keyboard=[
                            [
                                types.InlineKeyboardButton(
                                    text=i10n.load_more_tasks(),
                                    callback_data=f"tls__next__all__{after_date_anchor}__{before_date_anchor}",
                                )
                            ]
                        ]
                    )
                else:
                    keyboard = types.InlineKeyboardMarkup(
                        # LOCALIZATION
                        inline_keyboard=[
                            [
                                types.InlineKeyboardButton(
                                    text=i10n.load_more_tasks(),
                                    callback_data=f"tls__next__{after_date_anchor}__{before_date_anchor}",
                                )
                            ]
                        ]
                    )

                await send_markdown2(
                    ray,
                    ctx,
                    chat.user_id,
                    MESSAGE_TYPE_TASKS_LISTING_SEQUENTIAL,
                    message,
                    keyboard,
                    related_tasks_ids=[task.get("id")],
                )

            else:
                await send_markdown2(
                    ray,
                    ctx,
                    chat.user_id,
                    MESSAGE_TYPE_TASKS_LISTING_SEQUENTIAL,
                    message,
                    keyboard,
                    related_tasks_ids=[task.get("id")],
                )

        else:
            await send_markdown2(
                ray,
                ctx,
                chat.user_id,
                MESSAGE_TYPE_TASKS_LISTING_SEQUENTIAL,
                message,
                keyboard,
                related_tasks_ids=[task.get("id")],
            )
        tasks_sent = True  # Set the flag to True since a task is sent


    if not tasks_sent:  # Check if no tasks were sent after the loop
        response = i10n.no_tasks_in_inbox() if inbox else i10n.no_tasks()
        await send_markdown2(ray, ctx, chat.user_id, "regular", response)


    offset += limit
    await ctx.redis.setex(redis_key_sequential_listing_offset(user.id), 60 * 30, offset)
