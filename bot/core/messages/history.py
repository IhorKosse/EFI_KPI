import aiohttp
from core.messages.types import (
    MESSAGE_AI_RESPONSE,
    MESSAGE_REGULAR,
    MESSAGE_TYPE_TASKS_FROM_AI,
    MESSAGE_TYPE_TASKS_LISTING,
    MESSAGE_TYPE_TASKS_LISTING_SEQUENTIAL,
    MESSAGE_USER_REQUEST,
    MESSAGE_TYPE_NOTIFICATION,
)

from yarl import URL
import settings


async def fetch(
    ray: int,
    chat_id: int,
    message_type: str = "",
    limit: int = 20,
    message_id: int | None = None,
    session: aiohttp.ClientSession | None = None,
):
    headers = {"X-API-KEY": settings.SUPERUSER_API_KEY}

    base_url = URL(settings.INTERNAL_API_URL_PREFIX)
    # Add path and query parameters
    query_params = [("i", "none")]
    if chat_id:
        query_params.append(("chat_id", str(chat_id)))
    if message_type:
        query_params.append(("type", message_type))
    if limit and limit > 0:
        query_params.append(("limit", str(limit)))
    if message_id is not None:
        query_params.append(("message_id", str(message_id)))

    url = base_url.join(URL("history/messages/"))

    url = url.with_query(dict(query_params))

    async with aiohttp.ClientSession() if session is None else session as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                messages = await response.json()
                return messages
            else:
                response_text = await response.text()
                raise RuntimeError(
                    f"Failed to fetch messages. Status code: {response.status}. Response: {response_text}"
                )


# todo: add proper logs here.
async def append_to_history(
    ray: int,
    chat_id: int,
    message_id: int,
    message: str,
    message_type: str,
    related_tasks_ids: list[int] | None = None,
    session: aiohttp.ClientSession | None = None,
):
    VALID_MESSAGE_TYPES = [
        MESSAGE_REGULAR,
        MESSAGE_USER_REQUEST,
        MESSAGE_AI_RESPONSE,
        MESSAGE_TYPE_TASKS_LISTING,
        MESSAGE_TYPE_TASKS_LISTING_SEQUENTIAL,
        MESSAGE_TYPE_NOTIFICATION,
        MESSAGE_TYPE_TASKS_FROM_AI,
    ]
    if message_type not in VALID_MESSAGE_TYPES:
        raise ValueError(f"Invalid message type. Valid options are: {', '.join(VALID_MESSAGE_TYPES)}")

    if not related_tasks_ids:
        related_tasks_ids = []

    if not all(isinstance(task_id, int) for task_id in related_tasks_ids):
        raise ValueError("Related tasks IDs should be a list of integers.")

    url = URL(settings.INTERNAL_API_URL_PREFIX).join(URL("history/messages/"))

    headers = {"X-API-KEY": settings.SUPERUSER_API_KEY, "Content-Type": "application/json"}
    message_data = {
        "message_id": message_id,
        "chat_id": chat_id,
        "content": message,
        "type": message_type,
        "related_task_ids_json": related_tasks_ids,
    }

    async with aiohttp.ClientSession() if session is None else session as session:
        async with session.post(url, headers=headers, json=message_data) as response:
            if response.status != 201:
                response_text = await response.text()
                raise RuntimeError(
                    f"Failed to append message. Status code: {response.status}. Response: {response_text}"
                )
            else:
                return await response.json()


async def delete_from_history(
    ray: int,
    chat_id: int,
    message_id: int,
    session: aiohttp.ClientSession | None = None,
):
    url = URL(settings.INTERNAL_API_URL_PREFIX).join(URL("history/messages/"))
    headers = {"X-API-KEY": settings.SUPERUSER_API_KEY}
    message_data = {"message_id": message_id, "chat_id": chat_id}

    async with aiohttp.ClientSession() if session is None else session as session:
        async with session.delete(url, headers=headers, json=message_data) as response:
            if response.status != 200:
                response_text = await response.text()
                raise RuntimeError(
                    f"Failed to delete message. Status code: {response.status}. Response: {response_text}"
                )
            else:
                return True


async def edit_in_history(
    ray: int,
    chat_id: int,
    message_id: int,
    new_text: str,
    type: str,
    related_tasks_ids: list[int] | None = None,
    session: aiohttp.ClientSession | None = None,
):
    if not related_tasks_ids:
        related_tasks_ids = []

    url = URL(settings.INTERNAL_API_URL_PREFIX).join(URL("history/messages/"))

    headers = {"X-API-KEY": settings.SUPERUSER_API_KEY}
    message_data = {
        "message_id": message_id,
        "chat_id": chat_id,
        "content": new_text,
        "type": type,
        "related_task_ids_json": related_tasks_ids,
    }

    async with aiohttp.ClientSession() if session is None else session as session:
        async with session.patch(url, headers=headers, json=message_data) as response:
            if response.status != 200:
                response_text = await response.text()
                raise RuntimeError(f"Failed to edit message. Status code: {response.status}. Response: {response_text}")
            else:
                return await response.json()
