import asyncio

import aiohttp
from aiogram import enums
from httpx import HTTPStatusError
from openai import BadRequestError
from core.messages.history import append_to_history
from core.messages.types import MESSAGE_TYPE_TASKS_FROM_AI
from core.stringutils import format_text

import settings
from core import functions, log, runs, threads
from core.ai.tasks import enrich_ai_response_with_tasks_context
from core.common import BotCtx, TelegramMessageCtx, TelegramUserCtx
from core.timeutils import now_according_to_users_timezone


async def post_message_to_thread(
    ctx: BotCtx,
    ray: int,
    input: TelegramMessageCtx,
    thread_id: str,
    processing_key: str,
    recreate_a_run_on_failure=True,
    attempt=0,
):
    user = TelegramUserCtx.from_message_context(input)
    now = await now_according_to_users_timezone(user)
    content_with_timestamp = (
        f'<now "{now.strftime("%a")} {now.isoformat()}"/> ' + input._modified_text if input._modified_text else ""
    )
    log.info(ray, f"Incoming user message: {content_with_timestamp}")

    await clear_thread_up_to_six_messages(ctx, thread_id)

    await threads.append_user_thread_context(ctx.ai, thread_id, content_with_timestamp, recreate_a_run_on_failure)
    try:
        run = await ctx.ai.beta.threads.runs.create(assistant_id=settings.OPEN_AI_ASSISTANT_ID, thread_id=thread_id)
    except Exception as e:
        # Handle the exception as needed, for example, log the error and possibly retry or exit
        print(f"An error occurred while creating a run: {e}")
    # Depending on the nature of the error, you might want to retry or handle it differently
    # For example, if it's a temporary network error, you might want to retry after a short delay
    # If it's a more serious error, you might want to log it and stop the process or raise the exception
    await ctx.redis.setex(f"thread:{thread_id}:run_id", 300, run.id)
    while True:
        run_status = await runs.get_update_or_wait(ctx.ai, thread_id, run.id)
        if run_status.status == "requires_action":
            await functions.resolve_functions_input(
                ray,
                ctx.bot,
                ctx.ai,
                ctx.redis,
                user,
                thread_id,
                run.id,
                run_status.required_action,
            )
            continue

        if run_status.status == "completed":
            response = await ctx.ai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            messages = await ctx.ai.beta.threads.messages.list(thread_id=thread_id, limit=1)
            await ctx.redis.delete(processing_key)
            async with aiohttp.ClientSession() as session:
                for response in messages.data:
                    log.info(ray, f"AI Response: {response}")

                    ai_response = response.content[0].text.value
                    if ai_response:
                        tasks_enriched_objects = await enrich_ai_response_with_tasks_context(
                            ray, ai_response, now, session
                        )
                        for enriched_object in tasks_enriched_objects:
                            log.info(ray, f"Responding to user: {enriched_object['message']}")

                            sent_message = await ctx.bot.send_message(
                                input.message.chat.id,
                                format_text(enriched_object["message"]),
                                parse_mode=enums.ParseMode.MARKDOWN_V2,
                            )
                            if enriched_object["tasks_info"]:
                                try:
                                    await append_to_history(
                                        ray,
                                        enriched_object["tasks_info"]["chat_id"],
                                        sent_message.message_id,
                                        enriched_object["message"],
                                        MESSAGE_TYPE_TASKS_FROM_AI,
                                        [enriched_object["tasks_info"]["task_id"]],
                                        session=None,
                                    )
                                except Exception as e:
                                    log.error(ray, f"Failed to append message from ai to history. Error:{e}")

                        # Create a summary of the AI's responses
                        # BUG Megalodon
                        # response_summary = "".join(obj["message"] for obj in tasks_enriched_objects)
                        # await threads.append_ai_thread_context(
                        #     ctx.ai, thread_id, response_summary, recreate_a_run_on_failure
                        # )

            return

        if run_status.status == "failed":
            if attempt < 3:
                # Try one more time.
                await post_message_to_thread(
                    ctx,
                    ray,
                    input,
                    thread_id,
                    processing_key,
                    recreate_a_run_on_failure,
                    attempt=attempt + 1,
                )
            else:
                raise RuntimeError(f"unexpected thread run status: {run_status.status}")

        raise RuntimeError(f"unexpected status: {run_status.status}")


async def clear_thread_up_to_six_messages(ctx: BotCtx, thread_id: str):
    thread_messages = ctx.ai.beta.threads.messages.list(thread_id)
    pages = []
    async for page in thread_messages:
        pages.append(page)

    if len(pages) >= 6:
        # Delete all pages except the first 6
        for page in pages[4:]:
            message_id = page.id
            await ctx.ai.beta.threads.messages.delete(
                message_id=message_id,
                thread_id=thread_id,
            )


async def get_task_status(ctx: BotCtx, thread_id: str, run_id: str):
    try:
        run_status = await ctx.ai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        return run_status.status
    except HTTPStatusError as e:
        if e.response.status_code == 404:
            log.info(f"Run not found in thread {thread_id} for run {run_id}")
            return "run_not_exist"
        else:
            log.error(f"HTTP error retrieving task status in thread {thread_id} for run {run_id}: {e}")
            return "error"
    except Exception:
        # log.error(f"Unexpected error retrieving task status in thread {thread_id} for run {run_id}: {e}")
        return "completed"


async def get_thread_id_by_user_id(ctx: BotCtx, user_id: int):
    """
    Retrieves the thread ID associated with a user from Redis cache.
    If no thread ID is found, a new thread is created using the OpenAI API,
    and any existing threads for the user are cleared to maintain efficiency on the OpenAI's side.

    The new thread is created with a lifespan determined by settings.BOT_THREAD_CONTEXT_TIMEOUT_SECONDS,
    after which it is considered stale and a new thread will be created upon the next request.
    """

    return await __get_or_create_thread_id(ctx, user_id, "default")


async def get_index_thread_id_by_user_id(ctx: BotCtx, user_id: int):
    """
    Retrieves the index thread ID associated with a user from Redis cache.
    If no thread ID is found, a new thread is created using the OpenAI API,
    and any existing threads for the user are cleared to maintain efficiency on the OpenAI's side.

    The new thread is created with a lifespan determined by settings.BOT_THREAD_CONTEXT_TIMEOUT_SECONDS,
    after which it is considered stale and a new thread will be created upon the next request.
    """

    return await __get_or_create_thread_id(ctx, user_id, "index")


async def append_user_thread_context(ctx: BotCtx, thread_id, text, cancel_previous_run: bool = False, attempt: int = 0):
    """
    Appends user's context to the thread for a given thread ID.

    :param ai: The AsyncOpenAI client instance to interact with the OpenAI API.
    :param thread_id: The thread ID to which to append the text.
    :param text: The text to append to the thread context.
    """
    try:
        await ctx.beta.threads.messages.create(thread_id=thread_id, role="user", content=text)

    except BadRequestError as e:
        if not cancel_previous_run:
            raise e

        # Error message contain ID of a run, that is already created.
        # This run must be cancelled (concurred access is not available).
        for word in e.message.split(" "):
            if word.startswith("run_"):
                try:
                    if attempt < 3:
                        run_id = word
                        await ctx.beta.threads.runs.cancel(thread_id=thread_id, run_id=run_id)
                        return await append_user_thread_context(
                            ctx,
                            thread_id,
                            text,
                            cancel_previous_run=cancel_previous_run,
                            attempt=attempt + 1,
                        )

                except BadRequestError as e:
                    if "Cannot cancel run with status 'cancelling'." in e.message:
                        if attempt < 3:
                            await asyncio.sleep(3)  # Wait some time while thread will be cancelled and try again.
                            return await append_user_thread_context(
                                ctx,
                                thread_id,
                                text,
                                cancel_previous_run=cancel_previous_run,
                                attempt=attempt + 1,
                            )
                        else:
                            raise e


async def append_ai_thread_context(ctx: BotCtx, thread_id, text, cancel_previous_run: bool = False, attempt: int = 0):
    """
    Appends AI's context to the thread for a given thread ID.

    :param ai: The AsyncOpenAI client instance to interact with the OpenAI API.
    :param thread_id: The thread ID to which to append the text.
    :param text: The text to append to the thread context.
    """
    try:
        # WARN!
        # OpenAI api does not support sending messages as assistant.
        # So we mark the message as user's message, but prepend it with a special text,
        # so the assistant will be capable to deal with it on a second run.
        await ctx.beta.threads.messages.create(thread_id=thread_id, role="user", content="<by assystant> " + text)

    except BadRequestError as e:
        if not cancel_previous_run:
            raise e

        # Error message contain ID of a run, that is already created.
        # This run must be cancelled (concurred access is not available).
        for word in e.message.split(" "):
            if word.startswith("run_"):
                try:
                    if attempt < 3:
                        run_id = word
                        await ctx.beta.threads.runs.cancel(thread_id=thread_id, run_id=run_id)
                        return append_ai_thread_context(
                            ctx,
                            thread_id,
                            text,
                            cancel_previous_run=cancel_previous_run,
                            attempt=attempt + 1,
                        )

                except BadRequestError as e:
                    if "Cannot cancel run with status 'cancelling'." in e.message:
                        if attempt < 3:
                            await asyncio.sleep(3)  # Wait some time while thread will be cancelled and try again.
                            return await append_ai_thread_context(
                                ctx,
                                thread_id,
                                text,
                                cancel_previous_run=cancel_previous_run,
                                attempt=attempt + 1,
                            )
                        else:
                            raise e


async def __get_or_create_thread_id(ctx: BotCtx, user_id: int, type="default"):
    if type not in ["default", "index"]:
        raise Exception("Invalid thread type, possible options are 'default' and 'index'")

    thread_id = await __get_thread_id_from_redis(ctx.redis, user_id, type)
    if thread_id:
        return thread_id

    thread = await ctx.ai.beta.threads.create()
    try:
        await __clear_threads_cache_on_open_ai_side(ctx, user_id, type)
    except Exception:
        pass
    await __assign_thread_to_user(ctx.redis, thread.id, user_id, type)
    return thread.id


async def __get_thread_id_from_redis(ctx: BotCtx, user_id, type: str):
    """
    Attempts to retrieve the current thread ID for a given user from Redis.

    If a thread ID exists in Redis under the key "user:{user_id}_current_thread",
    it is returned after decoding from bytes to a UTF-8 string. If no thread ID
    is found, None is returned, indicating that a new thread should be created.

    :param rc: Redis client instance to interact with the Redis cache.
    :param user_id: The user ID for which to retrieve the thread ID.
    :paream type: The type of thread to retrieve. Defaults to "default".
        Possible options are "default" and "index".

    :return: The thread ID as a string if found, otherwise None.
    """
    key = __compose_threads_namespace_key_prefix(user_id, type) + ".current_thread"

    thread_id = await ctx.get(key)
    if thread_id:
        await ctx.expire(key, settings.BOT_THREAD_CONTEXT_TIMEOUT_SECONDS)
        return thread_id.decode("utf-8")

    # TODO: Maybe populate a thread with messages from the chat history (stored in our DB).
    return None


async def __assign_thread_to_user(ctx: BotCtx, thread_id, user_id, type: str = "default"):
    key_prefix = __compose_threads_namespace_key_prefix(user_id, type)
    await ctx.setex(
        f"{key_prefix}.current_thread",
        settings.BOT_THREAD_CONTEXT_TIMEOUT_SECONDS,
        thread_id,
    )
    await ctx.lpush(f"{key_prefix}.threads", thread_id)


async def __clear_threads_cache_on_open_ai_side(ctx: BotCtx, user_id, type: str = "default"):
    """
    Clears all thread IDs associated with a user from the OpenAI cache and Redis.

    This function retrieves a list of thread IDs from Redis, deletes each thread using the OpenAI API,
    and then clears the Redis cache for the user's threads. This ensures that there are no stale threads
    left on the OpenAI side and that the user starts with a fresh thread upon the next interaction.

    :param ai: The AsyncOpenAI client instance to interact with the OpenAI API.
    :param rc: The Redis client instance to interact with the Redis cache.
    :param user_id: The user ID for which to clear the threads.
    :paream type: The type of thread to retrieve. Defaults to "default".
        Possible options are "default" and "index".
    """

    key_prefix = __compose_threads_namespace_key_prefix(user_id, type)
    thread_ids = await ctx.redis.lrange(f"{key_prefix}.threads", 0, -1)
    for thread_id in thread_ids:
        await ctx.ai.beta.threads.delete(thread_id=thread_id.decode("utf-8"))

    await ctx.redis.delete(f"{key_prefix}.threads")


def __compose_threads_namespace_key_prefix(user_id, type: str = "default"):
    return f"user:{user_id}.threads.{type}"
