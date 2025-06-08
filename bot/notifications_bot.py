import asyncio
import datetime
import json
from openai import AsyncOpenAI
from redis import asyncio as redis
from core import log, threads
from core.common import BotCtx, TelegramUserCtx
from core.messages.history import append_to_history
from core.messages.types import MESSAGE_TYPE_NOTIFICATION
from core.subscriptions import create_checkout_session
from core.timeutils import now_according_to_users_timezone
from core.i10n import notifications as i10n
from core.i10n import tasks_listing as i10n_listing
from core.i10n import payments as i10n_payments
from core.i10n.tasks_listing__en import months_short as months_short_en
import settings
import logging
import aiohttp
from aiogram import Bot, enums
from yarl import URL
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ctx: BotCtx


class TaskProcessingError(Exception):
    def init(self, task_id, message, drop_from_index=False):
        self.task_id = task_id
        self.message = message
        self.drop_from_index = drop_from_index
        super().__init__(self.message)

    def drop_from_index(self):
        return self.drop_from_index

    def task_id(self):
        return self.task_id


async def __drop_next_notification_in_index(rc: redis.Redis, index_key: str) -> None:
    """
    Removes the next notification from the sorted set at the specified index key.

    Args:
        rc (aioredis.Redis): The Redis client.
        index_key (str): The key of the sorted set.
    """
    await rc.zremrangebyrank(index_key, 0, 0)


async def __get_next_notification_or_block(rc: redis.Redis, index_key: str) -> list:
    """
    Get the next notification from the specified index in Redis or sleep until
    the next notification is due.

    Args:
        rc (aioredis.Redis): The Redis client.
        index_key (str): The key of the index in Redis.

    Returns:
        list: The next notification from the index.
    """
    while True:
        notification = await rc.zrange(index_key, 0, 0)
        if not notification:
            await asyncio.sleep(30)  # Sleep for 30 seconds if no element fetched
            continue

        return notification


async def __fetch_task(session, task_id: str) -> dict:
    """
    Fetches the details of a task from the backend server.
    Validation the task for required fields.

    Args:
        session (aiohttp.ClientSession): The client session to use for the HTTP request.
        task_id (str): The ID of the task to fetch.

    Returns:
        dict: The details of the task.

    Raises:
        TaskProcessingError: If there is an error while fetching or processing the task.
    """
    task_url = URL(settings.INTERNAL_API_URL_PREFIX).join(URL(f"tasks/{task_id}/"))
    async with session.get(task_url) as response:
        if response.status == 404:
            raise TaskProcessingError(
                task_id,
                f"There is no task with ID = {task_id} in the database, notification is going to be dropped from index",
                True,
            )

        if response.status != 200:
            raise TaskProcessingError(
                task_id,
                f"Failed to fetch task {task_id}: "
                f"response status — {response.status}, "
                f"response text — {await response.text()}",
                False,
            )  # Note: no need to drop notification from index, the real reason of problem is unknown.

        try:
            task = await response.json()
            if "id" not in task:
                raise KeyError('required field "id" is missing in task data')

            if "name" not in task:
                raise KeyError('required field "name" is missing in task data')

            if "owner" not in task:
                raise KeyError('required field "owner" is missing in task data')

            if "chat_id" not in task["owner"]:
                raise KeyError('required field "chat_id" is missing in task data')

            if task["status"] == "closed":

                raise KeyError('Task is already closed')
            
            if task["status"] == "deleted":
                raise KeyError('Task is already closed')

        except Exception:
            raise TaskProcessingError(
                task_id,
                f"Failed to parse task {task_id}, JSON: {response.text()}. Notification is going to be dropped from index",
                True,
            )

        return task


async def __enrich_ai_thread_context_with_notification(ctx: BotCtx, task: dict) -> None:
    """
    Enriches the AI thread context with the notification details.
    This is required for AI to be able to continue the conversation and react on user's further input.

    Args:
        ai (AsyncOpenAI): The AI instance.
        rc (redis.Redis): The Redis client instance.
        task (dict): The task containing the notification details.

    Returns:
        None
    """
    new_context = f"{task['name']} <task_id={task['id']}>"  # Note: task_id is required for AI to be able to fetch task details from DB.
    chat_id = task["owner"]["chat_id"]
    thread_id = await threads.get_thread_id_by_user_id(ctx, chat_id)
    await threads.append_user_thread_context(ctx.ai, thread_id, new_context, cancel_previous_run=True)


async def __send_notification_to_the_user_through_bot(bot: Bot, task: dict, now: datetime) -> None:
    """
    Sends a notification to the user through a bot.

    Args:
        bot (Bot): The bot object used to send the message.
        task (dict): The task dictionary containing information about the task.

    Returns:
        None
    """

    message_markdown = f"*{task['name']}*"
    start = task.get("start_datetime")
    if start:
        start_format = "%Y-%m-%dT%H:%M:%SZ"
        parsed_start = datetime.datetime.strptime(start, start_format)
        formatted_start = parsed_start.strftime("%b %d %Y, %H:%M")

        time_left = parsed_start - now

        # ToDo: add proper time left formatting
        if parsed_start < now:
            message_markdown += f"\n\n⏳ {formatted_start}"

        else:
            if not isinstance(time_left, datetime.timedelta):
                time_left = datetime.timedelta(seconds=int(time_left))

            days, remainder = divmod(time_left.total_seconds(), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, _ = divmod(remainder, 60)

            # Format time_left_human_readable based on days, hours, and minutes
            if days:
                time_left_human_readable = i10n.days(hours, days)
            elif hours:
                time_left_human_readable = i10n.hours(hours)
            elif minutes:
                time_left_human_readable = i10n.minutes(minutes)
            else:
                time_left_human_readable = i10n.right_now()


            en_months_short = months_short_en()
            months_short = i10n_listing.months_short()
            for i, month in enumerate(en_months_short):
                if month in formatted_start:
                    formatted_start = formatted_start.replace(month, months_short[i])

            # Escape Markdown V2 special characters in the message
            message_markdown = (
                f"*{task['name'].replace('-', '\\-')}*\n\n⏳ {time_left_human_readable}, {formatted_start}"
            )

    chat_id = task["owner"]["chat_id"]
    queue_key = f"user:{chat_id}:queue"
    processing_key = f"user:{chat_id}:processing"
    is_not_queue_empty = await ctx.redis.exists(queue_key)
    is_not_processing_empty = await ctx.redis.exists(processing_key)

    while is_not_queue_empty >= 1 or is_not_processing_empty >= 1:
        # If either queue or processing is not empty, wait before sending the notification
        await asyncio.sleep(5)
        is_not_queue_empty = await ctx.redis.exists(queue_key)
        is_not_processing_empty = await ctx.redis.exists(processing_key)

    # Once both queue and processing are empty, proceed with sending the notification
    related_task_id = [task["id"]]
    try:
        message = await bot.send_message(chat_id, message_markdown, parse_mode=enums.ParseMode.MARKDOWN_V2)
    except Exception as e:
        print(e)
    message_id = message.message_id
    message_text = message.text
    ray = log.new_ray()
    await append_to_history(ray, chat_id, message_id, message_text, MESSAGE_TYPE_NOTIFICATION, related_task_id)


async def __sleep_until_notification_start(
    rc: redis.Redis, index_key: str, notification_key: str, now: datetime
) -> None:
    """
    Sleeps until the notification start is reached.

    Args:
        rc (redis.Redis): The Redis client.
        index_key (str): The key of the Redis sorted set containing the notification timestamps.
        notification_key (str): The key of the specific notification in the sorted set.
    """
    timestamp = await rc.zscore(index_key, notification_key)
    timestamp = timestamp - 3600 - 3600
    now = now.timestamp()
    await __drop_next_notification_in_index(ctx.redis, index_key)
    if now < timestamp:
        await asyncio.sleep(timestamp - now)


async def setup() -> BotCtx:
    ai = AsyncOpenAI(api_key=settings.OPEN_AI_API_KEY)
    rc = await redis.from_url(settings.REDIS_CONNECTION_STRING)
    bot = Bot(settings.TELEGRAM_BOT_TOKEN, parse_mode=None)

    return BotCtx(bot, rc, ai)


async def process_notification(bot, notification, session, index_key):
    try:
        # Interpret the notification as JSON
        notification_data = json.loads(notification.decode("utf-8"))
        task_id = notification_data.get("task_id")
        chat_id = notification_data.get("chat_id")
        payment_status = notification_data.get("payment_status")

        if task_id:
            # Process task notification using existing logic
            logging.info(f"Processing task {task_id}...")
            task = await __fetch_task(session, task_id)
            chat_id = task["owner"]["chat_id"]
            user = TelegramUserCtx(id=chat_id)
            now = await now_according_to_users_timezone(user)
            await __sleep_until_notification_start(ctx.redis, index_key, notification, now)
            now = await now_according_to_users_timezone(user)
            await __enrich_ai_thread_context_with_notification(ctx, task)
            try:
                task = await __fetch_task(session, task_id)
                await __send_notification_to_the_user_through_bot(ctx.bot, task, now)
            except Exception as e:
                logging.error(f"Failed to send notification to the user: {e}")
                # Optionally, handle the failure e.g., by retrying or logging
        elif chat_id and payment_status:
            # Process payment status update notification
            await send_payment_status_message(bot, chat_id, payment_status)
            await __drop_next_notification_in_index(ctx.redis, index_key)
        else:
            raise ValueError("Notification JSON does not contain 'task_id' or both 'chat_id' and 'payment_status'.")

    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode notification as JSON: {e}")
        # Handle the case where the notification is not in JSON format
    except Exception as e:
        logging.error(f"Failed to process notification: {e}")
        # Handle other exceptions as needed


async def send_payment_status_message(bot, chat_id, payment_status):
    # Implement the logic for sending a message to the user based on payment_status
    if payment_status == "success":
        message_text = i10n_payments.subscription_successful()
        await bot.send_message(chat_id, message_text)
    elif payment_status == "failed":
        monthly_price_id = settings.ONE_MONTH_PRICE_ID
        yearly_price_id = settings.ONE_YEAR_PRICE_ID
        user = TelegramUserCtx(id=chat_id)
        monthly_checkout_url = await create_checkout_session(ctx, user, monthly_price_id)
        yearly_checkout_url = await create_checkout_session(ctx, user, yearly_price_id)

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=i10n_payments.subscription_price_400_month(), url=monthly_checkout_url)],
                [InlineKeyboardButton(text=i10n_payments.subscription_price_4800_year(), url=yearly_checkout_url)],
            ]
        )
        await bot.send_message(chat_id, i10n_payments.payment_unsuccessful(), reply_markup=keyboard)


async def main():
    global ctx
    ctx = await setup()
    index_key = settings.NOTIFICATIONS["INDEX"]["redis_key"]

    logging.info("Notifications bot started")
    logging.basicConfig(level=logging.DEBUG)

    async with aiohttp.ClientSession() as session:
        while True:
            notifications = await __get_next_notification_or_block(ctx.redis, index_key)
            for notification in notifications:
                # Create a separate task for each notification
                asyncio.create_task(process_notification(ctx.bot, notification, session, index_key))
            await asyncio.sleep(30)  # Sleep for 30 seconds before checking for new notifications again


asyncio.run(main())
