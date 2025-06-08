from typing import Dict

import aiohttp
from yarl import URL

import settings
from core.common import TelegramUserCtx


# Internal cache for storing API keys for users.
# Stores headers as dict to avoid unnecessary copy operations on each access.
__internal_instance_api_keys_cache: Dict[int, dict] = {}


async def get_user_api_key_header_by_chat_id(
    user: TelegramUserCtx, session: aiohttp.ClientSession | None = None
) -> dict:
    """
    Retrieves and caches internally the API key header for a given user's chat ID.
    Safe to call multiple times for the same user, as the API key is cached internally.

    Args:
        session: The aiohttp ClientSession object for making HTTP requests.
        user: The TelegramUserCtx object representing the user.

    Returns:
        A dictionary containing the API key header.

    Raises:
        Exception: If the API key retrieval fails or the response is invalid.
    """

    api_key_header = __internal_instance_api_keys_cache.get(user.id)
    if api_key_header:
        return api_key_header

    # No cached API key found, fetch it from the back-end.
    # If no session — create it and use same method again.
    if not session:
        async with aiohttp.ClientSession() as session:
            return await get_user_api_key_header_by_chat_id(user, session)

    base_url = URL(settings.INTERNAL_API_URL_PREFIX)
    url = base_url / "users/api-key/"
    params = {
        "chat_id": user.id,
    }
    url = url.with_query(params)
    headers = {"X-API-Key": settings.SUPERUSER_API_KEY}

    async with session.get(url, headers=headers) as resp:
        if resp.status != 200:
            raise Exception(f"Failed to get api key for chat_id {user.id}. Status code: {resp.status}")

        data = await resp.json()
        key = data.get("key")
        if not key:
            raise Exception(f"Failed to get api key for chat_id {user.id}. Response: {await resp.text()}")

        # Store the key in the cache before returning it
        header = {"X-API-KEY": key}
        __internal_instance_api_keys_cache[user.id] = header
        return header
