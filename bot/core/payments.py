from datetime import datetime
from yarl import URL
import aiohttp
from aiogram import types
import settings
from core import users
from core.common import BotCtx, TelegramUserCtx
from core.redis import (
    redis_key_payments_optional,
)
from core.timeutils import now_according_to_users_timezone


async def check_subscription_end_date(message: types.Message, user: TelegramUserCtx):
    last_payment = await get_last_payment(user)
    user_current_time = await now_according_to_users_timezone(user)
    if last_payment and last_payment["subscription_end_date"]:
        subscription_end_date = datetime.strptime(last_payment["subscription_end_date"], "%Y-%m-%dT%H:%M:%SZ")
        if subscription_end_date <= user_current_time:
            return True
    return False


async def delete_optional(ctx: BotCtx, user: TelegramUserCtx):
    option_id = await ctx.redis.get(redis_key_payments_optional(user.id))
    if option_id:
        try:
            await ctx.bot.delete_message(user.id, option_id)
        finally:
            await ctx.redis.delete(redis_key_payments_optional(user.id))


async def get_last_payment(user: TelegramUserCtx):
    async with aiohttp.ClientSession() as session:
        headers = await users.get_user_api_key_by_chat_id(session, user)

        async with session.get(URL(settings.PAYMENTS_API_URL).join(URL("last-payment/")), headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                response_text = await response.text()
                raise RuntimeError(f"HTTP API Backend raised error: {response.status} - {response_text}")


async def get_last_payment_amount(user: TelegramUserCtx):
    last_payment = await get_last_payment(user)
    if last_payment and "amount" in last_payment:
        return last_payment["amount"]
    return None
