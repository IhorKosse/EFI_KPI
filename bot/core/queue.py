import asyncio
from datetime import datetime

from core.common import BotCtx, TelegramMessageCtx
from core.i10n import queue as i10n
from core.i10n import tasks_listing as i10n_listing
from core.threads import get_task_status, post_message_to_thread


async def collect_and_process_messages(
    ctx: BotCtx, ray: int, input: TelegramMessageCtx, thread_id: str, additional_task_context: str | None
):
    user_id = input.message.from_user.id
    queue_key = f"user:{user_id}:queue"
    processing_key = f"user:{user_id}:processing"
    last_message_time_key = f"user:{user_id}:last_message_time"

    try:
        if input._modified_text == "" and await ctx.redis.llen(queue_key) == 0:
            await update_status_message(ctx, user_id, queue_key, processing_key)
            return

        # Save the current time as the time of the last message
        await ctx.redis.set(last_message_time_key, int(datetime.now().timestamp()))

        # Check if there are messages in processing
        if await ctx.redis.llen(processing_key) > 0:
            # If there are, add to the queue
            message_text_to_queue = input.message.text if input.message.text is not None else ""
            # If there was a response to this message, then the context is added along with the message to the queue
            if additional_task_context:
                message_text_to_queue = f"{message_text_to_queue} {additional_task_context}"
            await ctx.redis.rpush(queue_key, message_text_to_queue)
            await update_status_message(ctx, user_id, queue_key, processing_key)
        elif await ctx.redis.llen(processing_key) == 0 and await ctx.redis.llen(queue_key) > 0:
            if input._modified_text == "":
                await check_and_transfer_messages(ctx, user_id, queue_key, processing_key, ray, input, thread_id)
            else:
                message_text_to_queue = input.message.text if input.message.text is not None else ""
                if additional_task_context:
                    message_text_to_queue = f"{message_text_to_queue} {additional_task_context}"
                await ctx.redis.rpush(queue_key, message_text_to_queue)
                await check_and_transfer_messages(ctx, user_id, queue_key, processing_key, ray, input, thread_id)
        else:
            await ctx.redis.rpush(processing_key, input.message.text if input.message.text is not None else "")
            await update_status_message(ctx, user_id, queue_key, processing_key)
            messages = await ctx.redis.lrange(processing_key, 0, 1 - 1)
            combined_message = "".join(message.decode("utf-8") for message in messages)
            if additional_task_context:
                combined_message = f"{combined_message} {additional_task_context}"
            input.update_message_text(combined_message)
            await post_message_to_thread(ctx, ray, input, thread_id, processing_key)
            input.update_message_text("")
            await collect_and_process_messages(ctx, ray, input, thread_id, additional_task_context=None)
    except Exception as e:
        print(f"Error is a {e}")
        await ctx.redis.delete(processing_key)
        await ctx.redis.delete(queue_key)
        await ctx.redis.delete(f"user:{user_id}.threads.default.current_thread")
        await update_status_message(ctx, user_id, queue_key, processing_key)
        failed_message_text = i10n_listing.smth_wrong()
        await ctx.bot.send_message(user_id, failed_message_text)

        # try:

        # except:


async def check_and_transfer_messages(ctx, user_id, queue_key, processing_key, ray, input, thread_id):
    last_message_time_key = f"user:{user_id}:last_message_time"
    while True:
        await asyncio.sleep(0.6)
        last_message_time = await ctx.redis.get(last_message_time_key)
        if last_message_time is not None:
            last_message_time = int(last_message_time)
            current_time = int(datetime.now().timestamp())
            if current_time - last_message_time >= 7:
                if await check_process_of_previous_tasks(ctx, thread_id):
                    messages_count = await ctx.redis.llen(queue_key)
                    if messages_count > 0:
                        for _ in range(messages_count):
                            message = await ctx.redis.lpop(queue_key)
                            if message:
                                await ctx.redis.rpush(processing_key, message)
                        await update_status_message(ctx, user_id, queue_key, processing_key)
                        messages = await ctx.redis.lrange(processing_key, -messages_count, -1)
                        combined_message = "\n".join(message.decode("utf-8") for message in messages)
                        input.update_message_text(combined_message)
                        await post_message_to_thread(ctx, ray, input, thread_id, processing_key)
                        await update_status_message(ctx, user_id, queue_key, processing_key)
                    # Important: Exit the loop after successful processing
                    break
                else:
                    # If previous tasks are not yet completed, continue waiting
                    continue
            else:
                # If 10 seconds have not passed yet, continue the loop
                continue
        else:
            # If unable to get the time of the last message, exit the loop
            break
    await ensure_queue_is_empty(ctx, user_id, queue_key, processing_key, ray, input, thread_id)


async def update_status_message(ctx, user_id, queue_key, processing_key):
    status_message_key = f"user:{user_id}:status_message_id"

    # Get current queue lengths
    current_queue_length = await ctx.redis.llen(queue_key)
    current_processing_length = await ctx.redis.llen(processing_key)

    # If both queues are empty, delete the status message and return
    if current_queue_length == 0 and current_processing_length == 0:
        previous_status_message_id = await ctx.redis.get(status_message_key)
        if previous_status_message_id:
            try:
                await ctx.bot.delete_message(chat_id=user_id, message_id=int(previous_status_message_id))
                print("Previous status message deleted because both queues are empty.")
            except Exception as e:
                print(f"Failed to delete previous status message: {e}")
        await ctx.redis.delete(status_message_key)
        return

    # Formulate and send a new status message
    status_message_text = i10n.status_message(int(current_processing_length), int(current_queue_length))
    previous_status_message_id = await ctx.redis.get(status_message_key)
    if previous_status_message_id:
        try:
            await ctx.bot.delete_message(chat_id=user_id, message_id=int(previous_status_message_id))
        except Exception as e:
            print(f"Failed to delete previous status message: {e}")
    status_message = await ctx.bot.send_message(user_id, status_message_text)
    await ctx.redis.set(status_message_key, status_message.message_id)


async def check_process_of_previous_tasks(ctx, thread_id):
    timeout = 3  # Timeout in seconds
    start_time = datetime.now()

    while (datetime.now() - start_time).total_seconds() < timeout:
        current_run_id = await ctx.redis.get(f"thread:{thread_id}:run_id")
        last_completed_run_id = await ctx.redis.get(f"thread:{thread_id}:last_completed_run_id")

        if current_run_id is None or current_run_id == last_completed_run_id:
            # Task completed, delete keys
            await ctx.redis.delete(f"thread:{thread_id}:run_id")
            await ctx.redis.delete(f"thread:{thread_id}:last_completed_run_id")
            return True  # Task completed

        # If run_id has changed, check the task status
        status = await get_task_status(ctx, thread_id, current_run_id.decode("utf-8") if current_run_id else "")
        if status in ["run_not_exist", "completed"]:
            await ctx.redis.set(f"thread:{thread_id}:last_completed_run_id", current_run_id)
            # After updating last_completed_run_id, delete old keys
            await ctx.redis.delete(f"thread:{thread_id}:run_id")
            await ctx.redis.delete(f"thread:{thread_id}:last_completed_run_id")
            return True

        await asyncio.sleep(2)  # Short pause before the next check

    # If the function doesn't finish within the timeout, assume the task is not completed
    print("Timeout reached, the task may still be processing.")
    return False


async def ensure_queue_is_empty(ctx, user_id, queue_key, processing_key, ray, input, thread_id):
    queue_length = await ctx.redis.llen(queue_key)
    if queue_length > 0:
        print(f"Queue is not empty after processing. {queue_length} messages left. Initiating reprocessing...")
        await check_and_transfer_messages(ctx, user_id, queue_key, processing_key, ray, input, thread_id)
