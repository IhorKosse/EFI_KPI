from typing import Dict
from core.common import TelegramUserCtx
import settings
from yarl import URL


__internal_instance_cache: Dict[int, str] = {}


# WARNING: DEPRECATED!
# Please, use the new function get_user_api_key_by_chat_id from core.api.headers instead.
# There are some important optimizations and improvements in the new function.
async def get_user_api_key_by_chat_id(session, user: TelegramUserCtx) -> dict:
    if user.id in __internal_instance_cache:
        return {"X-API-KEY": __internal_instance_cache[user.id]}

    # No cached API key found, fetch it from the back-end.
    base_url = URL(settings.INTERNAL_API_URL_PREFIX)
    url = base_url / "users/api-key/"
    params = {
        "chat_id": user.id
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
        __internal_instance_cache[user.id] = key
        return {"X-API-KEY": key}
