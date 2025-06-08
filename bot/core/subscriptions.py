from datetime import datetime, timedelta
import aiohttp
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from core.payments import get_last_payment, get_last_payment_amount
from core.settings.redis import redis_key_subscription_details_id
from core.stringutils import escape_markdown_v2
import settings
from core import users, log
from core.common import BotCtx, TelegramUserCtx
from core.i10n import payments as i10n_payments
from core.i10n import tasks_listing as i10n_listing
from core.timeutils import now_according_to_users_timezone
from aiogram import enums


async def get_user_requests(user: TelegramUserCtx):
    async with aiohttp.ClientSession() as session:
        headers = await users.get_user_api_key_by_chat_id(session, user)
        url = settings.PAYMENTS_API_URL + "requests/"
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                response_text = await response.text()
                raise RuntimeError(f"Failed to get user requests: {response.status} - {response_text}")


async def check_user_requests_limit(ctx: BotCtx, user: TelegramUserCtx):
    user_requests_data = await get_user_requests(user)
    user_requests_count = user_requests_data.get("requests", 0)
    subscription_status = await get_user_subscription_status(user)
    last_payment = await get_last_payment(user)
    subscription_end_date = datetime.strptime(last_payment["subscription_end_date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    offset_time = await now_according_to_users_timezone(user)
    if user_requests_count == 40:
        await ctx.bot.send_message(
            user.id, i10n_payments.remaining_messages_info(), parse_mode=enums.ParseMode.MARKDOWN_V2
        )
    if user_requests_count < 1:
        if subscription_status == "active":
            await replace_subscription(ctx, user, settings.ONE_MONTH_PRICE_ID)
        elif subscription_status == "trial":
            # Send free trial ended message with subscription button
            free_trial_ended_text = i10n_payments.free_trial_ended()
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=i10n_payments.create_subscription(), callback_data="go_to_subscription_creation"
                        )
                    ]
                ]
            )
            message = await ctx.bot.send_message(
                user.id,
                free_trial_ended_text,
                reply_markup=keyboard,
                disable_web_page_preview=True,
            )
            await ctx.redis.set(f"free_trial_message:{user.id}", message.message_id)
            return True
        elif subscription_status == "cancelled":
            cancellation_date = escape_markdown_v2(await get_adjusted_cancellation_date(user))
            cost_of_subscription = await get_last_payment_amount(user)
            if float(cost_of_subscription) == settings.SUBSCRIPTION_PRICES["yearly"]:
                plan_price = settings.SUBSCRIPTION_PRICES_MARKDOWN["yearly"]
            elif float(cost_of_subscription) == settings.SUBSCRIPTION_PRICES["monthly"]:
                plan_price = settings.SUBSCRIPTION_PRICES_MARKDOWN["monthly"]
            else:
                plan_price = settings.SUBSCRIPTION_PRICES_MARKDOWN["monthly"]
            subscription_cancelled_text = i10n_payments.subscription_cancelled_message(cancellation_date, plan_price)
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=i10n_payments.create_subscription(), callback_data="go_to_subscription_creation"
                        )
                    ]
                ]
            )
            message = await ctx.bot.send_message(
                user.id,
                subscription_cancelled_text,
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.MARKDOWN_V2,
                disable_web_page_preview=True,
            )
            await ctx.redis.set(f"cancelled_message:{user.id}", message.message_id)
            return True
        elif subscription_status == "incomplete":
            # Send payment failed message with retry button
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
            message = await ctx.bot.send_message(
                user.id, payment_failed_text, reply_markup=keyboard, parse_mode=enums.ParseMode.MARKDOWN_V2
            )
            await ctx.redis.set(f"payment_failed_message:{user.id}", message.message_id)
            return True
    elif subscription_end_date <= offset_time and subscription_status == "trial":
        free_trial_ended_text = i10n_payments.free_trial_ended()
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=i10n_payments.create_subscription(), callback_data="go_to_subscription_creation"
                    )
                ]
            ]
        )
        message = await ctx.bot.send_message(user.id, free_trial_ended_text, reply_markup=keyboard)
        await ctx.redis.set(f"free_trial_message:{user.id}", message.message_id)
        return True
    else:
        return False


async def get_user_subscription_status(user: TelegramUserCtx):
    async with aiohttp.ClientSession() as session:
        headers = await users.get_user_api_key_by_chat_id(session, user)
        url = settings.PAYMENTS_API_URL + "subscription-status/"

        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("status")
            else:
                response_text = await response.text()
                raise RuntimeError(f"Failed to get subscription status: {response.status} - {response_text}")


async def cancel_subscription(ctx: BotCtx, user: TelegramUserCtx):
    async with aiohttp.ClientSession() as session:
        headers = await users.get_user_api_key_by_chat_id(session, user)
        url = settings.PAYMENTS_API_URL + "subscription-status/"

        # Retrieve the subscription ID from your backend
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                subscription_id = data.get("subscription_id")
                if subscription_id:
                    try:
                        async with aiohttp.ClientSession() as session:
                            headers = await users.get_user_api_key_by_chat_id(session, user)
                            url = settings.PAYMENTS_API_URL + "cancel-subscription/"

                            async with session.post(url, headers=headers) as response:
                                if response.status == 200:
                                    success_message = i10n_payments.subscription_cancelled_message_heartbreak()
                                    await ctx.bot.send_message(user.id, success_message)
                                    return True
                                else:
                                    response_text = await response.text()
                                    print(f"Failed to cancel subscription: {response.status} - {response_text}")
                                    await ctx.bot.send_message(user.id, i10n_listing.smth_wrong())
                                    return False
                    except aiohttp.ClientError as e:
                        print(f"HTTP client error during subscription canceling: {e}")
                        await ctx.bot.send_message(user.id, i10n_listing.smth_wrong())
                        return False
                    except Exception as e:
                        print(f"Unexpected error during subscription canceling: {e}")
                        await ctx.bot.send_message(user.id, i10n_listing.smth_wrong())
                        return False
                else:
                    await ctx.bot.send_message(user.id, i10n_listing.smth_wrong())
                    return False
            else:
                await ctx.bot.send_message(user.id, i10n_listing.smth_wrong())
                return False


async def renew_cancelled_subscription(ctx: BotCtx, user: TelegramUserCtx):
    try:
        # Retrieve the last payment data using the existing function
        last_payment = await get_last_payment(user)
        # Get the current time according to the user's timezone
        user_current_time = await now_according_to_users_timezone(user)

        if last_payment and last_payment["subscription_end_date"]:
            last_payment_date = datetime.strptime(last_payment["subscription_end_date"], "%Y-%m-%dT%H:%M:%S.%fZ")

            # Retrieve the subscription status and ID
            async with aiohttp.ClientSession() as session:
                headers = await users.get_user_api_key_by_chat_id(session, user)
                subscription_status_response = await session.get(
                    settings.PAYMENTS_API_URL + "subscription-status/", headers=headers
                )
                if subscription_status_response.status == 200:
                    subscription_status_data = await subscription_status_response.json()
                    subscription_status = subscription_status_data.get("status")

                    if subscription_status == "cancelled" and last_payment_date > user_current_time:
                        try:
                            async with aiohttp.ClientSession() as session:
                                headers = await users.get_user_api_key_by_chat_id(session, user)
                                url = settings.PAYMENTS_API_URL + "reactivate-subscription/"

                                async with session.post(url, headers=headers) as response:
                                    if response.status == 200:
                                        success_message = i10n_payments.subscription_resumed()
                                        await delete_subscription_details_menu(ctx, user)
                                        await ctx.bot.send_message(user.id, success_message)
                                        return True
                                    else:
                                        response_text = await response.text()
                                        print(f"Failed to reactivate subscription: {response.status} - {response_text}")
                                        await delete_subscription_details_menu(ctx, user)
                                        await ctx.bot.send_message(
                                            user.id,
                                            i10n_payments.subscription_resumption_error(),
                                        )
                                        return False
                        except aiohttp.ClientError as e:
                            print(f"HTTP client error during subscription resumption: {e}")
                            await delete_subscription_details_menu(ctx, user)
                            await ctx.bot.send_message(user.id, i10n_payments.subscription_resumption_error())
                            return False
                        except Exception as e:
                            print(f"Unexpected error during subscription resumption: {e}")
                            await delete_subscription_details_menu(ctx, user)
                            await ctx.bot.send_message(user.id, i10n_payments.subscription_resumption_error())
                            return False
                    else:
                        # If the subscription status is not 'cancelled' or the last payment date has passed, send a link to create a new one
                        await delete_subscription_details_menu(ctx, user)
                        await send_subscription_info(ctx, user)
                        return True
                else:
                    error_message = i10n_listing.smth_wrong()
                    await ctx.bot.send_message(user.id, error_message)
                    return False
        else:
            error_message = i10n_payments.no_last_payment_info()
            await ctx.bot.send_message(user.id, error_message)
            return False
    except aiohttp.ClientError as e:
        print(f"HTTP client error during subscription renewal: {e}")
        await ctx.bot.send_message(user.id, i10n_listing.smth_wrong())
        return False
    except Exception as e:
        print(f"Unexpected error during subscription renewal: {e}")
        await ctx.bot.send_message(user.id, i10n_listing.smth_wrong())
        return False


async def get_stripe_portal_link(user: TelegramUserCtx) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            headers = await users.get_user_api_key_by_chat_id(session, user)
            customer_url = settings.PAYMENTS_API_URL + "customer/"

            async with session.get(customer_url, headers=headers) as response:
                if response.status == 200:
                    customer_data = await response.json()
                    customer_id = customer_data.get("customer")
                    if customer_id:
                        # Create a billing portal session via your API
                        portal_url = settings.PAYMENTS_API_URL + "create-billing-portal-session/"

                        async with session.get(portal_url, headers=headers) as portal_response:
                            if portal_response.status == 200:
                                portal_data = await portal_response.json()
                                return portal_data.get("url")
                            else:
                                portal_response_text = await portal_response.text()
                                print(
                                    f"Failed to create billing portal session: {portal_response.status} - {portal_response_text}"
                                )
                                return None
                    else:
                        print("Customer ID not found")
                        return None
                else:
                    response_text = await response.text()
                    print(f"Failed to retrieve customer data: {response.status} - {response_text}")
                    return None
    except aiohttp.ClientError as e:
        print(f"HTTP client error during Stripe portal link retrieval: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error during Stripe portal link retrieval: {e}")
        return None


async def send_subscription_info(ctx, user):
    try:
        # Delete the free trial ended message if it exists
        message_id = await ctx.redis.get(f"free_trial_message:{user.id}")
        message_id2 = await ctx.redis.get(f"cancelled_message:{user.id}")
        if message_id or message_id2:
            await ctx.bot.delete_message(user.id, int(message_id))
            await ctx.redis.delete(f"free_trial_message:{user.id}")
            await ctx.bot.delete_message(user.id, int(message_id2))
            await ctx.redis.delete(f"cancelled_message:{user.id}")

        # Send the first message with efi_features
        await ctx.bot.send_message(
            user.id,
            i10n_payments.efi_features(),
            parse_mode=enums.ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True,
        )

        # Create the keyboard with two buttons in two rows
        monthly_price_id = settings.ONE_MONTH_PRICE_ID
        yearly_price_id = settings.ONE_YEAR_PRICE_ID

        monthly_checkout_url = await create_checkout_session(ctx, user, monthly_price_id)
        yearly_checkout_url = await create_checkout_session(ctx, user, yearly_price_id)

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=i10n_payments.subscription_price_400_month(), url=monthly_checkout_url)],
                [InlineKeyboardButton(text=i10n_payments.subscription_price_4800_year(), url=yearly_checkout_url)],
            ]
        )

        # Send the second message with subscription_includes and the keyboard
        await ctx.bot.send_message(
            user.id,
            text=i10n_payments.subscription_includes(),
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True,
        )
    except Exception as e:
        print(f"Unexpected error during sending subscription info: {e}")
        await ctx.bot.send_message(user.id, i10n_listing.smth_wrong())


async def create_checkout_session(ctx, user, price_id):
    chat_id = user.id
    async with aiohttp.ClientSession() as session:
        json_data = {"chat_id": str(chat_id), "price_id": price_id, "localization": settings.LOCALIZATION}
        headers = {"Content-Type": "application/json"}
        async with session.post(
            settings.PAYMENTS_API_URL + "create-checkout-session",
            json=json_data,
            headers=headers,
        ) as response:
            if response.status == 200:
                response_data = await response.json()
                return response_data["url"]
            else:
                print(f"Failed to create checkout session: {response.status}")
                await ctx.bot.send_message(chat_id, i10n_listing.smth_wrong())


async def retrieve_status_stripe(user: TelegramUserCtx):
    async with aiohttp.ClientSession() as session:
        headers = await users.get_user_api_key_by_chat_id(session, user)
        url = settings.PAYMENTS_API_URL + "retrieve-status-stripe/"

        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data["status"]
            else:
                response_text = await response.text()
                raise RuntimeError(f"Failed to retrieve status from Stripe: {response.status} - {response_text}")


async def get_cancellation_date(user: TelegramUserCtx):
    async with aiohttp.ClientSession() as session:
        headers = await users.get_user_api_key_by_chat_id(session, user)
        url = settings.PAYMENTS_API_URL + "get-cancellation-date/"

        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                date = data.get("cancellation_date")
                return date

            else:
                response_text = await response.text()
                raise RuntimeError(f"Failed to get cancellation date: {response.status} - {response_text}")


async def get_adjusted_cancellation_date(user: TelegramUserCtx):
    cancellation_date_str = await get_cancellation_date(user)
    if cancellation_date_str:
        cancellation_date = datetime.fromisoformat(cancellation_date_str.replace("Z", "+00:00"))
        adjusted_date = cancellation_date - timedelta(days=30)
        formatted_adjusted_date = adjusted_date.strftime("%Y-%m-%d")
        return formatted_adjusted_date
    else:
        raise RuntimeError("Cancellation date not found")


async def delete_subscription_details_menu(ctx: BotCtx, user: TelegramUserCtx):
    details_message_id = await ctx.redis.get(redis_key_subscription_details_id(user.id))
    if details_message_id:
        try:
            await ctx.bot.delete_message(user.id, details_message_id)

        except:
            pass

        finally:
            await ctx.redis.delete(redis_key_subscription_details_id(user.id))


async def replace_subscription(ctx: BotCtx, user: TelegramUserCtx, price_id: str):
    async with aiohttp.ClientSession() as session:
        headers = await users.get_user_api_key_by_chat_id(session, user)
        json_data = {"chat_id": str(user.id), "plan_id": price_id}
        url = settings.PAYMENTS_API_URL + "replace-subscription/"

        async with session.post(url, json=json_data, headers=headers) as response:
            if response.status == 200:
                pass
            else:
                response_text = await response.text()
                error_message = f"Failed to replace subscription: {response.status} - {response_text}"
                raise RuntimeError(error_message)


async def update_remind_for_promo(user: TelegramUserCtx):
    async with aiohttp.ClientSession() as session:
        headers = await users.get_user_api_key_by_chat_id(session, user)
        url = settings.PAYMENTS_API_URL + "update-remind-for-promo/"

        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                response_text = await response.text()
                raise RuntimeError(f"Failed to update remind for promo: {response.status} - {response_text}")


async def add_user_requests(ctx: BotCtx, user: TelegramUserCtx, requests: int):
    async with aiohttp.ClientSession() as session:
        headers = await users.get_user_api_key_by_chat_id(session, user)
        payload = {"increment_amount": requests}
        url = settings.PAYMENTS_API_URL + "add-request/"

        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                await ctx.bot.send_message(
                    user.id,
                    i10n_payments.free_messages_credited(settings.ONE_TIME_FREE_REQUESTS),
                    parse_mode=enums.ParseMode.MARKDOWN_V2,
                )
                return await response.json()
            else:
                response_text = await response.text()
                raise RuntimeError(f"Failed to add user requests: {response.status} - {response_text}")


async def retry_subscription_payment(ray, user: TelegramUserCtx):
    async with aiohttp.ClientSession() as session:
        headers = await users.get_user_api_key_by_chat_id(session, user)
        url = settings.PAYMENTS_API_URL + "retry-subscription-payment/"

        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                pass
            else:
                response_text = await response.text()
                error_message = f"Failed to retry subscription payment: {response.status} - {response_text}"
                log.debug(ray, error_message)
