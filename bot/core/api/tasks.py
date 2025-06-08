import datetime
from urllib.parse import quote

import aiohttp
from core.timeutils import now_according_to_users_timezone

import settings
from core import users
from core.common import TelegramUserCtx
from yarl import URL


class TasksList(list):
    """
    A custom list class representing a list of tasks, returned by the API.
    This class behaves like a list, but also has additional attributes.

    Attributes:
        tasks_count (int): The number of tasks returned.
        more_available (bool): Indicates if there are more tasks available for fetching.
    """

    def __init__(self, api_response: dict):
        """
        Args:
            api_response (dict): The API response containing the `tasks`, `count` and `more_available` fields.
        """
        super().__init__(api_response.get("tasks", []))
        self.tasks_count = api_response.get("count", 0)
        self.more_available = bool(api_response.get("more_available", False))

    def __str__(self):
        return f"<TasksList: {self.tasks}>"


async def get_tasks(
    user_ctx: TelegramUserCtx,
    inbox: bool = False,
    limit: int | None = None,
    offset: int | None = None,
    after: datetime.datetime | None = None,
    before: datetime.datetime | None = None,
    session: aiohttp.ClientSession | None = None,
    listing_sequential: bool = False
) -> TasksList:
    if not session:
        async with aiohttp.ClientSession() as session:
            return await __get_tasks(session, user_ctx, inbox, limit, offset, after, before, listing_sequential)

    else:
        return await __get_tasks(session, user_ctx, inbox, limit, offset, after, before, listing_sequential)


async def __get_tasks(
    session: aiohttp.ClientSession,
    user_ctx: TelegramUserCtx,
    inbox: bool = False,
    limit: int | None = None,
    offset: int | None = None,
    after: datetime.datetime | None = None,
    before: datetime.datetime | None = None,
    listing_sequential: bool = False
) -> TasksList:
    query = await __compose_tasks_query(
        session,
        user_ctx,
        inbox=inbox,
        limit=limit,
        offset=offset,
        before=before,
        after=after,
        listing_sequential=listing_sequential,
    )

    async with session.get(query["url"], headers=query["headers"]) as response:
        data = await response.json()
        if "error" in data:
            raise RuntimeError("HTTP API Backend raised error: {data}")

        return TasksList(data)


async def __compose_tasks_query(
    session: aiohttp.ClientSession,
    user: TelegramUserCtx,
    inbox=False,
    limit: int | None = None,
    offset: int | None = None,
    after: datetime.datetime | None = None,
    before: datetime.datetime | None = None,
    query: str = "",
    listing_sequential = False
) -> dict:
    # Use Eugene's implementation of headers provision.
    headers = await users.get_user_api_key_by_chat_id(session, user)

    url = URL(settings.API_BASE_URL).join(URL("tasks/"))

    params = {}

    if listing_sequential:
        params["s"] = "null"

    if inbox:
        params["inbox"] = "true"

    if limit:
        if limit > 100:
            raise ValueError("Limit can't be more than 100")
        if limit < 1:
            raise ValueError("Limit can't be less than 1")
        params["limit"] = str(limit)

    if offset:
        if offset < 0:
            raise ValueError("Offset can't be less than 0")
        # This part of the code has been commented out via a list
        # if before is not None or after is not None:
        #     raise ValueError("You can't use both offset and before/after parameters at the same time")
        params["offset"] = str(offset)

    if before:
        if after and before < after:
            raise ValueError("Before can't be less than after")
        params["deadline_range_before"] = before.isoformat()

    if after:
        if before and after > before:
            raise ValueError("After can't be greater than before")
        now = await now_according_to_users_timezone(user)
        if after.date() != now.date():
            params["deadline_range_after"] = after.isoformat()
        else:
            params["t"] = "True"

    if query:
        params["query"] = query

    url = url.with_query(params)

    return {
        "headers": headers,
        "url": str(url),
    }

async def close_one(user: TelegramUserCtx, task_id: int, completed: bool, session: aiohttp.ClientSession | None = None):
    """
    Closes a single task.
    If completed is True, the task will be marked as completed,
    otherwise it will be just closed.

    Args:
        user (TelegramUserCtx): The bot user.
        task_id (int): The ID of the task to close.
        completed (bool): Indicates whether the task is completed or not.
        session (aiohttp.ClientSession | None, optional): The client session to use for the API request.
            If not provided, a new session will be created.

    Returns:
        dict: The response data from the API (as is).

    Raises:
        RuntimeError: If the HTTP API Backend raises an error.
    """

    if not session:
        async with aiohttp.ClientSession() as session:
            return await close_one(user, task_id, completed, session)

    headers = await users.get_user_api_key_by_chat_id(session, user)
    payload = {"status": "closed"}
    if completed:
        payload["completed"] = True

    async with session.patch(URL(settings.API_BASE_URL).join(URL(f"tasks/{task_id}/")), json=payload, headers=headers) as response:
        data = await response.json()
        if "error" in data:
            raise RuntimeError("HTTP API Backend raised error: {data}")
        return data


async def close_batch(
    user: TelegramUserCtx, task_ids: list[int], completed: list[bool], session: aiohttp.ClientSession | None = None
):
    """
    Close a batch of tasks.
    For each task passes, if corresponding completed flag is True,
    the task will be marked as completed, otherwise it will be just closed.

    Args:
        user (TelegramUserCtx): The bot user.
        task_ids (list[int]): A list of task IDs to close.
        completed (list[bool]): A list of completion statuses for the tasks.
        session (aiohttp.ClientSession | None, optional): The client session to use for the API request.
            If not provided, a new session will be created.

    Returns:
        dict: The response data from the API.

    Raises:
        ValueError: If the lengths of task_ids and completed lists are not the same.
        RuntimeError: If the HTTP API Backend returns an error.
    """
    if len(task_ids) != len(completed):
        raise ValueError("task_ids and completed lists must be of the same length")

    if not session:
        async with aiohttp.ClientSession() as session:
            return await close_batch(user, task_ids, completed, session)

    headers = await users.get_user_api_key_by_chat_id(session, user)
    tasks_payload = [
        {"id": task_id, "status": "closed", "completed": comp} for task_id, comp in zip(task_ids, completed)
    ]

    async with session.patch(URL(settings.API_BASE_URL).join(URL("tasks/")), json={"tasks": tasks_payload}, headers=headers) as response:
        data = await response.json()
        if "error" in data:
            raise RuntimeError("HTTP API Backend raised error: {data}")
        return data
async def reopen_one(user: TelegramUserCtx, task_id: int, session: aiohttp.ClientSession | None = None):
    """
    Reopens a single task.

    Args:
        user (TelegramUserCtx): The bot user.
        task_id (int): The ID of the task to reopen.
        session (aiohttp.ClientSession | None, optional): The client session to use for the API request.
            If not provided, a new session will be created.

    Returns:
        dict: The response data from the API (as is).

    Raises:
        RuntimeError: If the HTTP API Backend raises an error.
    """

    if not session:
        async with aiohttp.ClientSession() as session:
            return await reopen_one(user, task_id, session)

    headers = await users.get_user_api_key_by_chat_id(session, user)
    payload = {"status": None}  

    async with session.patch(URL(settings.API_BASE_URL).join(URL(f"tasks/{task_id}/")), json=payload, headers=headers) as response:
        data = await response.json()
        if "error" in data:
            raise RuntimeError(f"HTTP API Backend raised error: {data}")
        return data
