from datetime import datetime, timedelta
from typing import Dict
from core.stringutils import escape_markdown_v2
from core.timeutils import now_according_to_users_timezone
import settings
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from core import log
from core.common import BotCtx, TelegramMessageCtx, TelegramUserCtx
from core.i10n import tasks_listing as i10n
from core.i10n import payments as i10n_payments
from core.i10n import support as i10n_support
from core.i10n import telegraph as i10n_telegraph
from core.payments import get_last_payment, get_last_payment_amount
from core.subscriptions import (
    cancel_subscription,
    delete_subscription_details_menu,
    get_adjusted_cancellation_date,
    get_stripe_portal_link,
    get_user_requests,
    get_user_subscription_status,
    retrieve_status_stripe,
)
from core.settings.redis import (
    redis_key_settings_message_id,
    redis_key_subscription_details_id,
)
from core.settings.timezone import get_timezone_shift
from aiogram import enums, types

__internal_cache__settings_initialized: Dict[int, bool] = {}
__internal_reminders_cache: Dict[int, str] = {}

async def settings_has_been_initialized(ray: int, user: TelegramUserCtx) -> bool:
    if user.id in __internal_cache__settings_initialized:
        return True

    try:
        # TODO: [Eugene Kusiak] Pls, fix error:
        # ERROR:root:[rai=1550038873]: Failed to check if settings have been initialized for user 61834914: 0, message='Attempt to decode JSON with unexpected mimetype: text/html; charset=utf-8', url=URL('http://127.0.0.1:8000/v1/user/settings/')
        timezone_shift = await get_timezone_shift(user)
        if timezone_shift is not None:
            __internal_cache__settings_initialized[user.id] = True
            return True

    except Exception as e:
        log.error(ray, f"Failed to check if settings have been initialized for user {user.id}: {e}")

        # If the error is not related to the connection to the back-end, then it's a critical error.
        # It should be raised to the upper level.
        if "connection" in str(e):
            raise e
        else:
            return False


# LOCALIZATION
async def create_settings_menu_keyboard(user: TelegramUserCtx) -> InlineKeyboardMarkup:
    keyboard = []
    row = []
    row_support = []
    row_telegraph = []
    row_subscription = []  # New row for the subscribe button
    row_reminder = []  # New row for the subscribe button

    timezone_shift = await get_timezone_shift(user)
    utc_now = datetime.utcnow()

    # Calculate time in the specified UTC offset

    if user.id in __internal_reminders_cache:
        key =  __internal_reminders_cache[user.id]
    else:
        key = i10n.auto_reminders_on()
        __internal_reminders_cache[user.id] = key

    
    button_reminder = InlineKeyboardButton(text=(i10n.auto_reminders() + " " + key), callback_data="change_reminder")
    row_reminder.append(button_reminder)
    keyboard.append(row_reminder)

    offset_time = utc_now + timedelta(hours=timezone_shift)

    button = InlineKeyboardButton(text=(i10n.current_time(offset_time)), callback_data="change_timezone")
    row.append(button)
    keyboard.append(row)

    button_support = InlineKeyboardButton(text=i10n_support.write_to_support(), callback_data="support")
    row_support.append(button_support)
    keyboard.append(row_support)

    button_telegraph = InlineKeyboardButton(text=i10n_telegraph.telegraph(), callback_data="telegraph")
    row_telegraph.append(button_telegraph)
    keyboard.append(row_telegraph)

    # Add the subscribe button

    button_subscription = InlineKeyboardButton(text=i10n_payments.subscription(), callback_data="subscription_settings")
    row_subscription.append(button_subscription)
    keyboard.append(row_subscription)

    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return reply_markup


async def delete_settings_message_if_exists(ctx: BotCtx, ray: int, user: TelegramUserCtx):
    settings_message_id = await ctx.redis.get(redis_key_settings_message_id(user.id))

    if settings_message_id:
        try:
            await ctx.bot.delete_message(chat_id=user.id, message_id=settings_message_id)
        finally:
            await ctx.redis.delete(redis_key_settings_message_id(user.id))


async def get_subscription_end_date(user: TelegramUserCtx) -> str:
    last_payment = await get_last_payment(user)
    end_date_str = last_payment["subscription_end_date"].replace("Z", "+00:00")
    end_date = datetime.fromisoformat(end_date_str)
    formatted_end_date = end_date.strftime("%Y-%m-%d")
    return formatted_end_date


async def get_payment_date(user: TelegramUserCtx) -> str:
    last_payment = await get_last_payment(user)
    payment_date_str = last_payment["payment_date"].replace("Z", "+00:00")
    payment_date = datetime.fromisoformat(payment_date_str)
    formatted_payment_date = payment_date.strftime("%Y-%m-%d")
    return formatted_payment_date


async def send_support_info(ctx: BotCtx, input: TelegramMessageCtx):
    chat_id = input.message.from_user.id
    text = i10n_support.link_to_support(settings.LINK_TO_SUPPORT)
    await ctx.bot.send_message(chat_id, text)


async def send_telegraph_link(ctx: BotCtx, input: TelegramMessageCtx):
    chat_id = input.message.from_user.id
    text = i10n_telegraph.telegraph_link()
    await ctx.bot.send_message(chat_id, text)


async def send_subscription_menu(ctx: BotCtx, user: TelegramUserCtx):
    subscription_end_date_str = await get_subscription_end_date(user)
    subscription_end_date = datetime.fromisoformat(
        subscription_end_date_str
    )  # Convert to datetime # Escape after conversion
    user_requests_data = await get_user_requests(user)
    user_requests_count = user_requests_data.get("requests", 0)
    subscription_status = await get_user_subscription_status(user)
    now = await now_according_to_users_timezone(user)

    if subscription_status == "trial":
        if subscription_end_date > now:
            # Send the second message with trial activated message
            subscription_end_date = escape_markdown_v2(subscription_end_date_str)
            trial_activated_text = i10n_payments.trial_activated_message(
                settings.TRIAL_MESSAGE_LIMIT, user_requests_count, subscription_end_date
            )
        else:
            # Send the second message with trial ended message
            subscription_end_date = escape_markdown_v2(subscription_end_date_str)
            trial_activated_text = i10n_payments.trial_ended_message(
                settings.TRIAL_MESSAGE_LIMIT, user_requests_count, subscription_end_date
            )

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=i10n_payments.create_subscription(), callback_data="go_to_subscription_creation"
                    ),
                ],
            ]
        )
        sent_message = await ctx.bot.send_message(
            user.id,
            trial_activated_text,
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True,
        )

    elif subscription_status == "active":
        start_date = await get_payment_date(user)
        start_date = escape_markdown_v2(start_date)
        subscription_end_date = escape_markdown_v2(subscription_end_date_str)
        # Send the second message with subscription active message and three buttons
        cost_of_subscription = await get_last_payment_amount(user)
        if float(cost_of_subscription) == settings.SUBSCRIPTION_PRICES["yearly"]:
            all_messages = settings.YEARLY_MESSAGE_LIMIT
            plan_price = settings.SUBSCRIPTION_PRICES_MARKDOWN["yearly"]
        elif float(cost_of_subscription) == settings.SUBSCRIPTION_PRICES["monthly"]:
            all_messages = settings.MONTHLY_MESSAGE_LIMIT
            plan_price = settings.SUBSCRIPTION_PRICES_MARKDOWN["monthly"]
        else:
            all_messages = settings.MONTHLY_MESSAGE_LIMIT
            plan_price = settings.SUBSCRIPTION_PRICES_MARKDOWN["monthly"]
        # Delete else: all_messages = settings.MONTHLY_MESSAGE_LIMIT
        subscription_active_text = i10n_payments.subscription_active_message(
            start_date,
            plan_price,
            subscription_end_date,
            all_messages,
            user_requests_count,
        )
        url_portal = await get_stripe_portal_link(user)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=i10n_payments.subscription_management(),
                        callback_data="subscription_management",
                        url=url_portal,
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=i10n_payments.view_payments(), callback_data="view_payments", url=url_portal
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=i10n_payments.cancel_subscription(), callback_data="go_to_cancel_subscription"
                    )
                ],
            ]
        )
        sent_message = await ctx.bot.send_message(
            user.id,
            subscription_active_text,
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True,
        )

    elif subscription_status == "cancelled":
        stripe_status = await retrieve_status_stripe(user)

        if stripe_status == "active":
            # Send the second message with subscription cancelled message and two buttons
            cancellation_date = escape_markdown_v2(await get_adjusted_cancellation_date(user))
            cost_of_subscription = await get_last_payment_amount(user)
            if float(cost_of_subscription) == settings.SUBSCRIPTION_PRICES["yearly"]:
                all_messages = settings.YEARLY_MESSAGE_LIMIT
                plan_price = settings.SUBSCRIPTION_PRICES_MARKDOWN["yearly"]
            elif float(cost_of_subscription) == settings.SUBSCRIPTION_PRICES["monthly"]:
                all_messages = settings.MONTHLY_MESSAGE_LIMIT
                plan_price = settings.SUBSCRIPTION_PRICES_MARKDOWN["monthly"]
            else:
                all_messages = settings.MONTHLY_MESSAGE_LIMIT
                plan_price = settings.SUBSCRIPTION_PRICES_MARKDOWN["monthly"]
            subscription_cancelled_text = i10n_payments.subscription_cancelled_message(cancellation_date, plan_price)
            url_portal = await get_stripe_portal_link(user)
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=i10n_payments.resume_subscription(),
                            callback_data="resume_subscription",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text=i10n_payments.view_payments(), callback_data="view_payments", url=url_portal
                        )
                    ],
                ]
            )
        elif stripe_status == "canceled":
            # Send the second message with subscription cancelled message and two buttons
            cancellation_date = escape_markdown_v2(await get_adjusted_cancellation_date(user))
            url_portal = await get_stripe_portal_link(user)
            subscription_cancelled_text = i10n_payments.subscription_cancelled_message(
                cancellation_date, settings.SUBSCRIPTION_PRICES["monthly"]
            )
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=i10n_payments.create_subscription(), callback_data="go_to_subscription_creation"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text=i10n_payments.view_payments(), callback_data="view_payments", url=url_portal
                        )
                    ],
                ]
            )
        sent_message = await ctx.bot.send_message(
            user.id, subscription_cancelled_text, reply_markup=keyboard, parse_mode=enums.ParseMode.MARKDOWN_V2
        )

    elif subscription_status == "incomplete":
        payment_failed_text = i10n_payments.payment_failed_retry()
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=i10n_payments.retry_payment_button(), callback_data="retry_subscription_payment"
                    )
                ]
            ]
        )
        sent_message = await ctx.bot.send_message(
            user.id, payment_failed_text, reply_markup=keyboard, parse_mode=enums.ParseMode.MARKDOWN_V2
        )

    await ctx.redis.setex(redis_key_subscription_details_id(user.id), timedelta(minutes=30), sent_message.message_id)


async def handle_cancel_subscription(ctx: BotCtx, user: TelegramUserCtx):
    message_id = await ctx.redis.get(redis_key_subscription_details_id(user.id))
    if not message_id:
        return
    now = await now_according_to_users_timezone(user)
    date_to_use_requests = now + timedelta(days=30)
    formatted_adjusted_date = date_to_use_requests.strftime("%Y-%m-%d")
    user_requests_data = await get_user_requests(user)
    user_requests_count = user_requests_data.get("requests", 0)
    subscription_end_date = escape_markdown_v2(formatted_adjusted_date)
    cancel_text = i10n_payments.subscription_will_be_cancelled_message(user_requests_count, subscription_end_date)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i10n_payments.i_like_efi(), callback_data="i_like_efi")],
            [
                InlineKeyboardButton(
                    text=i10n_payments.confirmation_of_cancel_subscription(),
                    callback_data="confirm_cancel_subscription",
                )
            ],
        ]
    )
    await ctx.bot.edit_message_text(
        chat_id=user.id,
        message_id=int(message_id),  # Convert message_id to integer
        text=cancel_text,
        reply_markup=keyboard,
        parse_mode=enums.ParseMode.MARKDOWN_V2,
    )


async def handle_i_like_efi(ctx: BotCtx, user: TelegramUserCtx):
    message_id = await ctx.redis.get(redis_key_subscription_details_id(user.id))
    if not message_id:
        return

    # Send the "i_like_efi" message
    await ctx.bot.send_message(user.id, i10n_payments.mutual_love())

    # Delete the original message
    await ctx.bot.delete_message(user.id, int(message_id))
    await ctx.redis.delete(redis_key_subscription_details_id(user.id))


async def handle_confirm_cancel_subscription(ctx: BotCtx, user: TelegramUserCtx):
    await delete_subscription_details_menu(ctx, user)

    # Perform the cancellation
    await cancel_subscription(ctx, user)
