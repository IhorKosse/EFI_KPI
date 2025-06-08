import datetime

from aiogram import types


from core.common import BotCtx, TelegramChatCtx, TelegramMessageCtx, TelegramUserCtx
from core.tasks.listing.listing_monthly import render_monthly_navigation_form
from core.tasks.listing.listing_sequential import render_sequential_tasks_navigation
from core.tasks.listing.listing_weekly import render_weekly_tasks_navigation
from core.timeutils import now_according_to_users_timezone


async def process_tasks_sequential_listing(ctx: BotCtx, ray: int, callback: types.CallbackQuery):
    try:
        if callback.data:
            if type(callback.message) is not types.Message:
                raise ValueError("Callback message is not a Message")

            action = callback.data.replace("tls__", "")
            all_tasks_listing = False
            inbox = False
            if "next__" or "next__all__" or "next__inbox__" in action:
                if "next__inbox__" in action:
                    action = action.replace("next__inbox__", "")
                    inbox=True
                elif "next__all__" in action:
                    action = action.replace("next__all__", "")
                    all_tasks_listing = True
                elif "next__" in action:
                    action = action.replace("next__", "")
                raw_after, raw_before = action.split("__")
                if raw_after == "NONE":
                    after = None
                else:
                    after = datetime.datetime.fromisoformat(raw_after)

                if raw_before == "NONE":
                    before = None
                else:
                    before = datetime.datetime.fromisoformat(raw_before)
                chat = TelegramChatCtx.from_message_context(TelegramMessageCtx(callback.message))
                user = TelegramUserCtx.from_message_context(TelegramMessageCtx(callback.message))
                await render_sequential_tasks_navigation(
                    ray,
                    ctx,
                    chat,
                    after,
                    before,
                    await now_according_to_users_timezone(user),
                    continue_previous_listing=True,
                    all_tasks_listing=all_tasks_listing,
                    inbox=inbox
                )
        else:
            raise ValueError("Callback data is empty")

    finally:
        await callback.answer()


async def process_tasks_weekly_listing(ctx: BotCtx, ray: int, callback: types.CallbackQuery):
    try:
        if callback.data:
            if type(callback.message) is not types.Message:
                raise ValueError("Callback message is not a Message")

            action = callback.data.replace("tlw_", "")
            if "_pw_" in action:
                action = action.replace("_pw_", "")
                anchor_day = datetime.datetime.fromisoformat(action)
                target_day = anchor_day - datetime.timedelta(days=7)

            elif "_nw_" in action:
                action = action.replace("_nw_", "")
                anchor_day = datetime.datetime.fromisoformat(action)
                target_day = anchor_day + datetime.timedelta(days=1)

            else:
                target_day = datetime.datetime.fromisoformat(action)

            message_ctx = TelegramMessageCtx(callback.message)
            user = TelegramUserCtx.from_message_context(message_ctx)
            chat = TelegramChatCtx.from_message_context(message_ctx)
            now = await now_according_to_users_timezone(user)
            await render_weekly_tasks_navigation(ray, ctx, chat, target_day, now)

        else:
            raise ValueError("Callback data is empty")

    finally:
        await callback.answer()


async def process_tasks_monthly_listing(ctx: BotCtx, ray: int, callback: types.CallbackQuery):
    try:
        if callback.data:
            if type(callback.message) is not types.Message:
                raise ValueError("Callback message is not a Message")

            chat = TelegramChatCtx.from_message_context(TelegramMessageCtx(callback.message))
            user = TelegramUserCtx.from_chat_context(chat)
            action = callback.data.replace("tlm_", "")
            if "_pm_" in action:
                action = action.replace("_pm_", "")
                anchor_day = datetime.datetime.fromisoformat(action)
                target_day = anchor_day - datetime.timedelta(days=anchor_day.day + 1)
                target_day = target_day.replace(day=1)

            elif "_nm_" in action:
                action = action.replace("_nm_", "")
                anchor_day = datetime.datetime.fromisoformat(action)

                # Increment month and correctly handle year change
                if anchor_day.month == 12:
                    target_day = datetime.datetime(anchor_day.year + 1, 1, 1)
                else:
                    target_day = datetime.datetime(anchor_day.year, anchor_day.month + 1, 1)

            elif "_today" in action:
                target_day = await now_according_to_users_timezone(user)

            else:
                target_day = datetime.datetime.fromisoformat(action)

            now = await now_according_to_users_timezone(user)
            await render_monthly_navigation_form(ray, ctx, chat, target_day, now)

        else:
            raise ValueError("Callback data is empty")

    finally:
        await callback.answer()
