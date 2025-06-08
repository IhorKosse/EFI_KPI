import aiohttp
from core.common import TelegramUserCtx
import settings

from core import functions
from yarl import URL



async def fetch_related_task_ids(ray: int, user: TelegramUserCtx, arguments: str) -> list:
    async with aiohttp.ClientSession() as session:
        query = await functions.compose_tasks_query(session, URL(settings.API_BASE_URL).join(URL("tasks/search/")), user, arguments)  
        async with session.get(query['url'], headers=query['headers']) as response:
            data = await response.json()
            if "error" in data:
                raise RuntimeError("HTTP API Backend raised error: {data}")
            return data
