import datetime
import re

import aiohttp

import settings
from core import log
from core.i10n import tasks_listing as i10n
from core.i10n.tasks_listing__en import days_short as days_short_en
from core.i10n.tasks_listing__en import months_short as months_short_en
from core.stringutils import escape_markdown_v2, matches_one_line_tasks_list_pattern
from yarl import URL


async def enrich_ai_response_with_tasks_context(
    ray: int, ai_response: str, now: datetime, session, sequential_number: int = 1
) -> list:
    """
    Enriches the AI response with tasks context.
    For each task ID in the response, fetches the task details from the database and replaces the task ID with the task details.
    Checks task deadline and adds a ⭕️⏳ emoji if the task is overdue.
    Formats the task deadline to be more human-readable.

    Args:
        ai_response (str): The AI response string.
        session: The session object.

    Returns:
        list: messages that must be sent to the user (per line or per task basis).
    """

    response_objects = []
    lines = ai_response.split("\n")

    tasks_current_sequential_number = sequential_number
    for response_line in lines:
        # Ignore empty responses from AI.
        if response_line == "" or response_line == "\n" or response_line == " ":
            continue

        response_line = response_line.replace("###", "")

        if matches_one_line_tasks_list_pattern(response_line):
            sub_lines = response_line.split(" ")
            for entry in sub_lines:
                if entry == "":
                    continue

                response_objects += await enrich_ai_response_with_tasks_context(
                    ray,
                    entry,
                    now,
                    session,
                    sequential_number=tasks_current_sequential_number,
                )
                tasks_current_sequential_number += 1

        else:
            # From time to time AI reponds with dashes at the beginning of the line,
            # instad of task number, but dashes collide with markdown formatting,
            # and must be removed.
            dashes_patterns = ["- ", "-", " -", " - "]
            for pattern in dashes_patterns:
                if response_line.startswith(pattern):
                    response_line = response_line.replace(pattern, "", 1)

            entries = re.findall(r"#(?:<ID)?(\d+)>?", response_line)
            if entries:
                if len(entries) > 1:
                    # AI responded with more than 1 task per line.
                    # The message is most probably something like this:
                    # "You have 2 tasks: #123 and #456. Enjoy your day!"
                    # Because of the last part (which can be context-dependent to the tasks count),
                    # it is impossible to simply replace task IDs with task details.
                    #
                    # In this case, the output must be reformatted to
                    # 1. Replace task IDs with sequential task number (#123 -> 1, #456 -> 2)
                    #    Further the bot will add links to the tasks and user will be able to click on them.
                    # 2. The AI response-message must remain the same, but
                    # 3. the task details must be added to the end of the message (as a separated messages).

                    for task_id_entry in entries:
                        task_id = int(task_id_entry[:])
                        task_message = await __task_id_to_task_description(ray, task_id, now, session)
                        if not task_message:
                            continue

                        task_formatted_sequential_number = f"#{tasks_current_sequential_number}"
                        response_line = response_line.replace(task_id_entry, task_formatted_sequential_number)

                        task_message = f"{tasks_current_sequential_number}. {task_message}"
                        markdown_compatible_task_message = escape_markdown_v2(task_message)
                        # response_messages.append(markdown_compatible_task_message)
                        response_objects.append({"message": markdown_compatible_task_message, "tasks_info": None})
                        tasks_current_sequential_number += 1

                    markdown_response_line = escape_markdown_v2(response_line)
                    response_objects.insert(
                        0,
                        {
                            "message": markdown_response_line,
                            "tasks_info": None,  # Assuming you want to insert this without task info
                        },
                    )

                else:
                    task_id = int(entries[0][:])
                    task_message, task_name, task_chat_id = await __task_id_to_task_description(
                        ray, task_id, now, session
                    )
                    if not task_message:
                        markdown_response_line = escape_markdown_v2(entries[0])
                        response_objects.append({"message": markdown_response_line, "tasks_info": None})
                        continue

                    task_message = f"{tasks_current_sequential_number}. {task_message}"
                    task_line = response_line.replace(entries[0], task_message)
                    markdown_response_line = escape_markdown_v2(task_message)

                    response_object = {
                        "message": markdown_response_line,
                        "tasks_info": {
                            "task_id": task_id,
                            "task_name": task_name,
                            "chat_id": task_chat_id,
                        },
                    }
                    response_objects.append(response_object)
                    tasks_current_sequential_number += 1

            else:
                response_objects.append({"message": escape_markdown_v2(response_line), "tasks_info": None})

    return response_objects


async def to_message(task: dict, now: datetime) -> str:
    """
    Converts a task dictionary into a formatted message string, used for sending tasks to the user.

    Args:
        task (dict): The task dictionary containing task information.

    Returns:
        str: The formatted message string suitable for sending to the user.
    """

    title = task.get("name", "")

    priority_map = {"": " ", "!": "❕", "!!": "❗️", "!!!": "‼️"}
    task_priority = priority_map.get(task.get("priority", ""), " ")

    message = f"{task_priority} {title}"

    formatted_deadline = task.get("deadline_datetime")
    formatted_start = task.get("start_datetime")

    def format_datetime(datetime_str, now):
        dt = datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
        week_number = dt.isocalendar()[1]
        now_week_number = now.isocalendar()[1]

        if now_week_number == week_number:
            return dt.strftime("%a, %H:%M")  # LOCALIZATION
        else:
            return dt.strftime("%b %d, %H:%M")  # LOCALIZATION

    if formatted_start:
        formatted_start = format_datetime(formatted_start, now)

    if formatted_deadline:
        formatted_deadline = format_datetime(formatted_deadline, now)

    if formatted_start and formatted_deadline:
        if formatted_start == formatted_deadline:
            message += f" ({formatted_start})"
        else:
            message += f" ({formatted_start} — {formatted_deadline})"
    elif formatted_start:
        message += f" ({formatted_start})"
    elif formatted_deadline:
        message += f" ({formatted_deadline})"

    en_days_short = days_short_en()
    days_short = i10n.days_short()
    for i, day in enumerate(en_days_short):
        if day in message:
            message = message.replace(day, days_short[i])

    en_months_short = months_short_en()
    months_short = i10n.months_short()
    for i, month in enumerate(en_months_short):
        if month in message:
            message = message.replace(month, months_short[i])
    return escape_markdown_v2(message)


async def __task_id_to_task_description(ray: int, task_id: int, now: datetime, session: aiohttp.ClientSession) -> str:
    """
    Retrieves the task description for a given task ID.

    Args:
        ray (int): Log ray.
        task_id (int): The ID of the task for which the description must be built.
        session: The session object for making HTTP requests.

    Returns:
        str: The task description as a string.
        None: If the task with the given ID does not exist.
    """

    try:
        task = await __get_task_by_id(task_id, session)
        task_message = await to_message(task, now)
        task_name = task.get("name", "")
        task_chat_id = task.get("owner", {}).get("chat_id", 0)  # Assuming the task object has a chat_id field
        return task_message, task_name, task_chat_id
    except Exception as e:
        # If there is no task with the given ID, skip it.
        # From time to time AI could respond with a task ID that does not exist any more.
        # E.g. when some task ha been deleted and AI reports deletion.
        if "Status code: 404" in str(e):
            log.debug(ray, f"Task {task_id} not found. Skipping.")
            return None

        # If error is not related to the task ID, raise it to log it.
        else:
            raise e


async def __get_task_by_id(id: int, session: aiohttp.ClientSession) -> str:
    base_url = URL(settings.INTERNAL_API_URL_PREFIX)
    url = base_url / f"tasks/{id}/"
    headers = {"X-API-Key": settings.SUPERUSER_API_KEY}
    async with session.get(url, headers=headers) as resp:
        if resp.status != 200:
            raise Exception(f"Failed to get task {id}. Status code: {resp.status}")

        data = await resp.json()
        return data
