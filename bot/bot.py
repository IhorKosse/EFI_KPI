import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F, types
from openai import AsyncOpenAI
from redis import asyncio as redis
from core.functions import decrement_user_requests
from core.settings.commands import handle_settings_command
from core.subscriptions import (
    add_user_requests,
    delete_subscription_details_menu,
    retry_subscription_payment,
    send_subscription_info,
    update_remind_for_promo,
    check_user_requests_limit,
    renew_cancelled_subscription,
)
from core.voice_process import convert_voice_to_text
import settings
from core import commands, log, threads
from core.characters_limit import characters_limit
from core.common import BotCtx, TelegramMessageCtx, TelegramUserCtx
from core.i10n import tasks_listing as i10n
from core.payments import (
    delete_optional,
)
from core.queue import collect_and_process_messages
from core.replies_filters.filters import apply_message_reply_filters, close_tasks_by_reaction, reopen_tasks_by_reaction
from core.settings import callbacks as settings_callbacks
from core.settings.callbacks import handle_change_reminder
from core.settings.common import (
    delete_settings_message_if_exists,
    handle_cancel_subscription,
    handle_confirm_cancel_subscription,
    handle_i_like_efi,
    send_subscription_menu,
    send_support_info,
    send_telegraph_link,
    settings_has_been_initialized,
)
from core.settings.timezone import send_timezone_selector
from core.tasks.listing import callbacks as listing_callbacks
from core.tutorial import callbacks as tutorial_callbacks

ctx: BotCtx
dp = Dispatcher()


@dp.callback_query(F.data.startswith("tls_"))  # tls -> tasks_listing_sequential
@dp.callback_query(F.data.startswith("tls_"))  # tls -> tasks_listing_sequential
async def process_tasks_sequential_listing(query: types.CallbackQuery):
    ray = log.new_ray()
    await listing_callbacks.process_tasks_sequential_listing(ctx, ray, query)


@dp.callback_query(F.data.startswith("tlw_"))  # tlw -> tasks_listing_weekly
@dp.callback_query(F.data.startswith("tlw_"))  # tlw -> tasks_listing_weekly
async def process_tasks_weekly_listing(query: types.CallbackQuery):
    ray = log.new_ray()
    await listing_callbacks.process_tasks_weekly_listing(ctx, ray, query)


@dp.callback_query(F.data.startswith("tlm_"))  # tlm -> tasks_listing_monthly
@dp.callback_query(F.data.startswith("tlm_"))  # tlm -> tasks_listing_monthly
async def process_tasks_monthly_listing(query: types.CallbackQuery):
    ray = log.new_ray()
    await listing_callbacks.process_tasks_monthly_listing(ctx, ray, query)


@dp.callback_query(lambda query: query.data == "change_reminder")
async def on_change_reminder_callback_query(query: types.CallbackQuery):
    ray = log.new_ray()
    await handle_change_reminder(ctx, ray, query)


@dp.callback_query(lambda query: query.data.startswith("settings_timezone_"))
async def process_settings_timezone_update(query: types.CallbackQuery):
    ray = log.new_ray()

    if not query.data:
        log.error(ray, "Callback data is empty")
        query.answer()
        return

    if query.data.startswith("settings_timezone_tutorial_"):
        await tutorial_callbacks.process_timezone_update(ctx, ray, query)
    else:
        await settings_callbacks.handle_callback_timezone(ctx, ray, query)


@dp.callback_query(lambda query: query.data.startswith("change_timezone"))
async def on_change_timezone_callback_query(query: types.CallbackQuery):
    ray = log.new_ray()
    await send_timezone_selector(ctx, ray, query)


@dp.callback_query(lambda query: query.data.startswith("support"))
async def handle_support(query: types.CallbackQuery):
    input = TelegramMessageCtx(query)
    user = TelegramUserCtx.from_message_context(TelegramMessageCtx(query))
    ray = log.new_ray()
    await send_support_info(ctx, input)
    await delete_settings_message_if_exists(ctx, ray, user)


@dp.callback_query(lambda query: query.data.startswith("telegraph"))
async def handle_telegraph(query: types.CallbackQuery):
    input = TelegramMessageCtx(query)
    user = TelegramUserCtx.from_message_context(TelegramMessageCtx(query))
    ray = log.new_ray()
    await send_telegraph_link(ctx, input)
    await delete_settings_message_if_exists(ctx, ray, user)


@dp.callback_query(lambda query: query.data.startswith("subscription_settings"))
async def send_subscription_details(query: types.CallbackQuery):
    user = TelegramUserCtx.from_message_context(TelegramMessageCtx(query))
    ray = log.new_ray()
    await delete_settings_message_if_exists(ctx, ray, user)
    await send_subscription_menu(ctx, user)


@dp.callback_query(lambda query: query.data.startswith("go_to_cancel_subscription"))
async def go_to_cancel_subscription(query: types.CallbackQuery):
    user = TelegramUserCtx.from_message_context(TelegramMessageCtx(query))
    await handle_cancel_subscription(ctx, user)


@dp.callback_query(lambda query: query.data.startswith("i_like_efi"))
async def i_like_efi(query: types.CallbackQuery):
    user = TelegramUserCtx.from_message_context(TelegramMessageCtx(query))
    await handle_i_like_efi(ctx, user)


@dp.callback_query(lambda query: query.data.startswith("confirm_cancel_subscription"))
async def confirm_cancel_subscription(query: types.CallbackQuery):
    user = TelegramUserCtx.from_message_context(TelegramMessageCtx(query))
    await handle_confirm_cancel_subscription(ctx, user)


@dp.callback_query(lambda query: query.data.startswith("resume_subscription"))
async def handle_renew_subscription(query: types.CallbackQuery):
    user = TelegramUserCtx.from_message_context(TelegramMessageCtx(query))
    await renew_cancelled_subscription(ctx, user)
    ray = log.new_ray()
    await delete_settings_message_if_exists(ctx, ray, user)


@dp.callback_query(lambda query: query.data.startswith("go_to_subscription_creation"))
async def handle_subscription_creation(query: types.CallbackQuery):
    user = TelegramUserCtx.from_message_context(TelegramMessageCtx(query))
    await send_subscription_info(ctx, user)


@dp.callback_query(lambda query: query.data.startswith("back_to_settings"))
async def handle_back_to_settings(query: types.CallbackQuery):
    input = TelegramMessageCtx(query)
    ray = log.new_ray()
    await handle_settings_command(ray, ctx, input)


@dp.callback_query(lambda query: query.data.startswith("do_not_remind_again"))
async def handle_do_not_remind_again(query: types.CallbackQuery):
    user = TelegramUserCtx.from_message_context(TelegramMessageCtx(query))
    await update_remind_for_promo(user)
    await query.message.delete()


@dp.callback_query(lambda query: query.data.startswith("show_available_options"))
async def handle_show_available_options(query: types.CallbackQuery):
    user = TelegramUserCtx.from_message_context(TelegramMessageCtx(query))
    await send_subscription_info(ctx, user)
    await query.message.delete()


@dp.callback_query(lambda query: query.data.startswith("get_messages_bonus"))
async def handle_get_messages_bonus(query: types.CallbackQuery):
    user = TelegramUserCtx.from_message_context(TelegramMessageCtx(query))
    await add_user_requests(ctx, user, settings.ONE_TIME_FREE_REQUESTS)
    await query.message.delete()


@dp.callback_query(lambda query: query.data.startswith("retry_subscription_payment"))
async def handle_retry_subscription_payment(query: types.CallbackQuery):
    user = TelegramUserCtx.from_message_context(TelegramMessageCtx(query))
    ray = log.new_ray()
    await retry_subscription_payment(ray, user)
    await query.message.delete()


@dp.message_reaction()
async def message_reaction_handler(reaction: types.reaction_type_emoji.ReactionTypeEmoji):
    ray = log.new_ray()
    message_id = reaction.message_id
    chat_id = reaction.chat.id
    user = TelegramUserCtx(reaction.user.id)
    if reaction.new_reaction:
        first_reaction = reaction.new_reaction[0]
        emoji = first_reaction.emoji
        if emoji in ("👍", "👌", "🤝"):
            await close_tasks_by_reaction(ray, message_id, chat_id, ctx, user, session=None)
    elif reaction.old_reaction:
        first_reaction = reaction.old_reaction[0]
        emoji = first_reaction.emoji
        if emoji in ("👍", "👌", "🤝"):
            await reopen_tasks_by_reaction(ray, message_id, chat_id, ctx, user, session=None)


@dp.message()
async def bot_message_handler(message: types.Message) -> None:
    input = TelegramMessageCtx(message)
    user = TelegramUserCtx.from_message_context(input)
    ray = log.new_ray()

    log.debug(ray, f"Incoming telegram bot message: {message}")

    # Check if user has initialized settings.
    # If not — no commands should be allowed except /start and /settings.
    if not await settings_has_been_initialized(ray, user):
        if message.text.lower() not in ("/start"):
            await message.answer(i10n.timezone_first())
            await message.delete()
            return

    # Close settings (delete message) if user has initialized them.
    # The message will be only deleted once due to internal cache.
    await delete_settings_message_if_exists(ctx, ray, user)

    #  Checking whether the user has sent a command, so that the user, even without a subscription, has the opportunity to use commands
    if message.text and not message.text.startswith(("/", "\\")):
        # LOCALIZATION
        if await check_user_requests_limit(ctx, user):
            return
    else:
        pass

        # TODO: [Ihor Kosse / REFACTORING REQUEST]
        # Please, keep this logic in the ned of processing the message.
        # The probability of the user sending a payment is very low,
        # so it is better to check it at the end of the message processing.
        pass
    if message.content_type not in ["text", "successful_payment", "voice"]:
        # Ignore...
        # ToDo: Add proper implementation for other message types.
        log.debug(ray, f"message is not a text: {message}")

        placeholder = i10n.non_text_message()
        await message.answer(placeholder)
        return
    if message.content_type == "voice":
        asyncio.create_task(ctx.bot.send_chat_action(message.chat.id, "typing"))
        thread_id = await threads.get_thread_id_by_user_id(ctx, user.id)
        text = await convert_voice_to_text(message, ctx)
        await collect_and_process_messages(ctx, ray, input, thread_id, additional_task_context=text)
        await decrement_user_requests(user)

    if not message.text:
        # Telegram bot for some reason sent an empty message.
        log.debug(ray, f"message is empty: {message}")
        return

    potential_command_candidate = message.text.lower()
    if potential_command_candidate.startswith("\\"):
        # Invalid slash command ocurred: command should start with a forward slash, not a backslash,
        # Invalid slash command ocurred: command should start with a forward slash, not a backslash,
        # but users can make mistakes, so we will fix it for them.
        potential_command_candidate = potential_command_candidate.replace("\\", "/")

    # Check if user has initialized settings.
    # If not — no commands should be allowed except /start and /settings.

    # Close settings (delete message) if user has initialized them.
    # The message will be only deleted once due to internal cache.
    await delete_settings_message_if_exists(ctx, ray, user)

    await delete_optional(ctx, user)

    await delete_subscription_details_menu(ctx, user)

    # Check if the message is a command.
    if potential_command_candidate.startswith("/"):
        command = potential_command_candidate
    if potential_command_candidate.startswith("/"):
        command = potential_command_candidate
        handler = commands.match(command)
        if handler:
            try:
                await handler(ray, ctx, input)

                # Delete the command message from the chat history to not to overload the chat.
                await message.delete()

                # After command has been executed — return from the handler.
                return

            except Exception as e:
                # Command handler has been found, but execution failed.
                # Command did not involved AI, so most probably the error is on our side.
                # No reason to ask the user to rephrase the input.
                error_message = f"Processing of user's commands failed with an exception: {e}"
                error_message = f"Processing of user's commands failed with an exception: {e}"
                log.error(ray, error_message)

                placeholder = i10n.smth_wrong()
                await message.answer(placeholder)

                # Still raise exception to log the error to the stderr.
                raise e

        else:
            placeholder = i10n.invalid_command()
            await message.answer(placeholder)
            return

    # The message is a plain text and not a command.
    # Potentially, it could be a reply to a message.
    if message.reply_to_message and message.reply_to_message.from_user.is_bot:
        status, reply, task_data = await apply_message_reply_filters(ctx, ray, input)
        if status:
            await message.answer(reply)
        else:
            additional_task_context = task_data
            thread_id = await threads.get_thread_id_by_user_id(ctx, user.id)
            if await characters_limit(ctx, input):
                await collect_and_process_messages(ctx, ray, input, thread_id, additional_task_context)
            pass

    # Involve AI to process the message.
    else:
        placeholder = i10n.working_one_moment()
        asyncio.create_task(ctx.bot.send_chat_action(message.chat.id, "typing"))

        try:
            # if message.text == i10n.close_tutorial():
            #     await close_tutorial(input)
            #     await ctx.bot.send_message(
            #         message.chat.id,
            #         i10n_payments.free_trial_activated_message(),
            #         parse_mode=enums.ParseMode.MARKDOWN_V2,
            #         disable_web_page_preview=True,
            #     )
            #     return

            thread_id = await threads.get_thread_id_by_user_id(ctx, user.id)
            if await characters_limit(ctx, input):
                await collect_and_process_messages(ctx, ray, input, thread_id, additional_task_context=None)
                await decrement_user_requests(user)
            # Check if the user's message matches the task prompt
            # if message.text == i10n.task_start_prompt():
            #     # Call the function to handle task completion
            #     await handle_task_completion(ctx, ray, user.id)

            # elif message.text == i10n.task_completion_prompt():
            #     # Call the function to handle task completion
            #     await handle_task_update(ctx, ray, user.id)

            # elif message.text == i10n.task_update_prompt():
            #     # Call the function to handle task completion
            #     await handle_task_close(ctx, ray, user.id)
            #     await ctx.bot.send_message(
            #         user.id,
            #         i10n_payments.free_trial_activated_message(),
            #         parse_mode=enums.ParseMode.MARKDOWN_V2,
            #         disable_web_page_preview=True,
            #     )

        except Exception as e:
            # Bot failed to process user's request with an error.
            # Log the error for further investigation.
            error_message = f"Processing of user's message failed with an exception: {e}"
            log.error(ray, error_message)

            # Ask user to rephrase the input.
            # 1. Placeholder message deletion could potentially raise an exception.
            # If, for example, the message has been deleted in `try`` block.
            #
            # 2, Message deletion could be async to speedup processing of a request a bit.

            i10n.oops()

            # Still raise exception to log the error in std err log.
            raise e


# pre checkout  (must be answered in 10 seconds)


async def main():
    global ctx
    ctx = await setup()
    await dp.start_polling(ctx.bot)


async def setup() -> BotCtx:
    ai = AsyncOpenAI(api_key=settings.OPEN_AI_API_KEY)
    rc = await redis.from_url(settings.REDIS_CONNECTION_STRING)
    bot = Bot(settings.TELEGRAM_BOT_TOKEN, parse_mode=None)

    return BotCtx(bot, rc, ai)


if __name__ == "__main__":
    if settings.DEBUG:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    else:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())
