import asyncio
import settings
from core.common import BotCtx, TelegramMessageCtx
from core.i10n import limit as i10n


# Quota Scheme Description:
# This function implements a message quota system for users. Each message sent by a user is tracked with a unique Redis key
# that includes the user ID and message ID, and has a time-to-live (TTL) corresponding to the quota time window (e.g., 1 hour).
# The length of each message is stored, and the total length of all messages within the TTL window is calculated.
# If the total length exceeds the predefined character limit, a limit message is sent to the user with the remaining time
# until the quota resets. This limit message is updated if the user attempts to send more messages during the limit period.
# Once the TTL expires, a message is sent to the user indicating that they can send messages again, and the limit message is deleted.
async def send_permission_message(ctx, user_id, limit_message_id_key, ttl, task_created_key):
    # Wait for TTL to expire before sending message about permission to write again
    await asyncio.sleep(ttl)
    await ctx.bot.send_message(chat_id=user_id, text=i10n.permission_to_write_again())
    # Delete the limit message if it exists
    limit_message_id = await ctx.redis.get(limit_message_id_key)
    if limit_message_id:
        try:
            await ctx.bot.delete_message(chat_id=user_id, message_id=int(limit_message_id))
        except Exception as e:
            print(f"Failed to delete limit message: {e}")
    # Delete key containing the ID of the limit exceeded message
    await ctx.redis.delete(limit_message_id_key)
    # Delete the task created flag
    await ctx.redis.delete(task_created_key)


async def characters_limit(ctx: BotCtx, input: TelegramMessageCtx):
    user_id = input.message.from_user.id
    message_length = len(input.message.text)
    message_key = f"users:input_quota:{user_id}:{input.message.message_id}"
    limit = settings.INPUT_QUOTA['max_characters_per_quota_window']  # Character limit
    ttl = settings.INPUT_QUOTA['quota_window_seconds']  # Time-to-live for the key (1 hour)
    limit_reached_key = f"users:input_quota:{user_id}:limit_reached"
    limit_message_id_key = f"users:input_quota:{user_id}:limit_message_id"

    # Set message length as the value for this message key with TTL
    await ctx.redis.setex(message_key, ttl, message_length)

    # Get keys pattern for all user messages
    keys_pattern = f"users:input_quota:{user_id}:*"
    user_message_keys = await ctx.redis.keys(keys_pattern)

    # Sum up lengths of all messages that haven't expired yet
    total_length = 0
    max_ttl = 0
    for key in user_message_keys:
        # Decode the key from bytes to str before retrieving the length
        key = key.decode("utf-8")
        # Ensure the key follows the expected pattern
        if key.startswith(f"users:input_quota:{user_id}:"):
            length = await ctx.redis.get(key)
            if length:
                total_length += int(length)
                key_ttl = await ctx.redis.ttl(key)
                if key_ttl > max_ttl:
                    max_ttl = key_ttl

    # Check if total length exceeds the set limit
    if total_length > limit:
        old_limit_message_id = await ctx.redis.get(limit_message_id_key)
        if old_limit_message_id:
            try:
                await ctx.bot.delete_message(chat_id=user_id, message_id=int(old_limit_message_id))
            except Exception as e:
                print(f"Failed to delete old limit message: {e}")

        # Use max_ttl to determine time until limit expires
        expires_in = max_ttl
        minutes, seconds = divmod(expires_in, 60)
        minutes = int(minutes)
        seconds = int(seconds)
        # Send new limit exceeded message
        sent_message = await ctx.bot.send_message(chat_id=user_id, text=i10n.raise_limit(minutes, seconds))
        # Save the ID of the new limit exceeded message
        await ctx.redis.set(limit_message_id_key, str(sent_message.message_id))

        if not await ctx.redis.get(limit_reached_key):
            await ctx.redis.set(limit_reached_key, "1")
            await ctx.redis.expire(limit_reached_key, ttl)
            # Wait for TTL to expire before sending message about permission to write again
            task_created_key = f"users:input_quota:{user_id}:task_created"
            if not await ctx.redis.get(task_created_key):
                await ctx.redis.set(task_created_key, "1")
                await ctx.redis.expire(task_created_key, ttl)
                # Create a task to send permission message after TTL expires
                asyncio.create_task(
                    send_permission_message(ctx, user_id, limit_message_id_key, expires_in, task_created_key)
                )
        return False
    return True
