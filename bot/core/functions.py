import asyncio
from datetime import datetime, timedelta
import json

import aiohttp
from core.common import TelegramUserCtx
from core.timeutils import now_according_to_users_timezone
from core import index
from core.settings.common import __internal_reminders_cache
import settings
from core import commands, log, users
from yarl import URL
from core.i10n import tasks_listing as i10n


#
#
# DEPRECATED
#
# WARNING: This file is a part of the old implementation!
# Please use core.api.tasks instead of this module.


async def get_tasks(user: TelegramUserCtx, arguments: str, full_format=False):
    async with aiohttp.ClientSession() as session:
        query = await compose_tasks_query(
            session,
            URL(settings.API_BASE_URL).join(URL("tasks/")),
            user,
            arguments,
        )
        async with session.get(query["url"], headers=query["headers"]) as response:
            data = await response.json()
            if "error" in data:
                raise RuntimeError("HTTP API Backend raised error: {data}")

            if full_format:
                return data

            else:
                response = {}
                for task in data.get("tasks", []):
                    if task.get("reminders", []):
                        response[task["id"]] = task
                    else:
                        response[task["id"]] = task["name"]

                return response


async def add_task(user: TelegramUserCtx, arguments: str):
    # From time to time AI passes invalid JSON as arguments (empty string).
    if arguments == "":
        arguments = "{}"


    args = json.loads(arguments)

    # Check if 'start' is in arguments and is in the correct format
    if 'start' in args:
        try:
            start_datetime = datetime.strptime(args['start'], '%Y-%m-%dT%H:%M:%S')
            user_reminder_setting = __internal_reminders_cache.get(user.id, i10n.auto_reminders_on())

            # Initialize reminders list if not present
            if 'reminders' not in args:
                args['reminders'] = []

            reminder_datetime = None
            if user_reminder_setting == i10n.auto_reminders_on():
                reminder_datetime = start_datetime
            elif user_reminder_setting == i10n.auto_reminders_15():
                reminder_datetime = start_datetime - timedelta(minutes=15)
            elif user_reminder_setting == i10n.auto_reminders_30():
                reminder_datetime = start_datetime - timedelta(minutes=30)
            elif user_reminder_setting == i10n.auto_reminders_60():
                reminder_datetime = start_datetime - timedelta(minutes=60)

            # Check if the reminder_datetime is not None and not already in the reminders
            if reminder_datetime and not any(reminder['on'] == reminder_datetime.isoformat() + "Z" for reminder in args['reminders']):
                args['reminders'].append({"on": reminder_datetime.isoformat() + "Z"})

        except:
            pass

    # Convert args back to string to proceed with your existing logic
    arguments = json.dumps(args)

    async with aiohttp.ClientSession() as session:
        args = __ai_arguments_to_json(arguments)
        headers = await users.get_user_api_key_by_chat_id(session, user)

        async with session.post(
            URL(settings.API_BASE_URL).join(URL("tasks/")), json=args, headers=headers
        ) as response:
            data = await response.json()
            if "error" in data:
                raise RuntimeError("HTTP API Backend raised error: {data}")
            return data


async def delete_tasks(user: TelegramUserCtx, arguments: str):
    # From time to time AI passes invalid JSON as arguments (empty string).
    if arguments == "":
        arguments = "{}"

    async with aiohttp.ClientSession() as session:
        args = __ai_arguments_to_json(arguments)
        headers = await users.get_user_api_key_by_chat_id(session, user)

        async with session.delete(
            URL(settings.API_BASE_URL).join(URL("tasks/")), json=args, headers=headers
        ) as response:
            data = await response.json()
            if "error" in data:
                raise RuntimeError("HTTP API Backend raised error: {data}")
            return data


async def update_task(user: TelegramUserCtx, arguments: str):
    # From time to time AI passes invalid JSON as arguments (empty string).
    if arguments == "":
        arguments = "{}"

    # Check if 'start' is in arguments and is in the correct format
    args = json.loads(arguments)
    if 'start' in args:
        try:
            start_datetime = datetime.strptime(args['start'], '%Y-%m-%dT%H:%M:%S')
            user_reminder_setting = __internal_reminders_cache.get(user.id, i10n.auto_reminders_on())

            # Initialize reminders list if not present
            if 'reminders' not in args:
                args['reminders'] = []

            reminder_datetime = None
            if user_reminder_setting == i10n.auto_reminders_on():
                reminder_datetime = start_datetime
            elif user_reminder_setting == i10n.auto_reminders_15():
                reminder_datetime = start_datetime - timedelta(minutes=15)
            elif user_reminder_setting == i10n.auto_reminders_30():
                reminder_datetime = start_datetime - timedelta(minutes=30)
            elif user_reminder_setting == i10n.auto_reminders_60():
                reminder_datetime = start_datetime - timedelta(minutes=60)

            # Check if the reminder_datetime is not None and not already in the reminders
            if reminder_datetime and not any(reminder['on'] == reminder_datetime.isoformat() + "Z" for reminder in args['reminders']):
                args['reminders'].append({"on": reminder_datetime.isoformat() + "Z"})

        except:
            pass

    # Convert args back to string to proceed with your existing logic
    arguments = json.dumps(args)

    async with aiohttp.ClientSession() as session:
        args = __ai_arguments_to_json(arguments)
        headers = await users.get_user_api_key_by_chat_id(session, user)

        task_id = args.get("id")
        if not task_id:
            raise RuntimeError("required argument is missed")
        del args["id"]

        async with session.patch(
            URL(settings.API_BASE_URL).join(URL(f"tasks/{task_id}/")), json=args, headers=headers
        ) as response:
            data = await response.json()
            if "error" in data:
                raise RuntimeError("HTTP API Backend raised error: {data}")
            return data


async def resolve_functions_input(
    ray,
    bot,
    ai,
    rc,
    user: TelegramUserCtx,
    thread_id: str,
    run_id: str,
    required_actions,
):
    log.info(ray, f"(function call): {required_actions}")

    tool_outputs = []
    for action in required_actions:
        if action[1] == "submit_tool_outputs":
            continue

        for call in action[1].tool_calls:
            function_name = call.function.name

            if function_name == "show_tasks":
                tasks_shown_to_user = await commands.show_tasks_on_users_ui(
                    bot, ai, rc, call.function.arguments, user.id
                )
                if not tasks_shown_to_user:
                    tool_outputs.append(
                        {
                            "tool_call_id": call.id,
                            "output": '{"hint":"no tasks"}',
                        }
                    )
                else:
                    tool_outputs.append(
                        {
                            "tool_call_id": call.id,
                            "output": json.dumps(
                                tasks_shown_to_user,
                                ensure_ascii=False,
                                separators=(",", ":"),
                            ),
                        }
                    )

            elif function_name == "get_tasks":
                tool_outputs.append(
                    {
                        "tool_call_id": call.id,
                        "output": json.dumps(
                            await get_tasks(user, call.function.arguments),
                            ensure_ascii=False,
                        ),
                    }
                )

            elif function_name == "add_task":
                tool_outputs.append(
                    {
                        "tool_call_id": call.id,
                        "output": json.dumps(
                            await add_task(user, call.function.arguments),
                            ensure_ascii=False,
                        ),
                    }
                )

            # Yes, there is no function "delete_tasks" in function calls definition.
            # But for some reason, AI passes this function call to us.
            # Most probably, this is a hallucination of AI, and it it is just easier to ignore it.
            elif function_name == "delete_task":
                tool_outputs.append(
                    {
                        "tool_call_id": call.id,
                        "output": json.dumps(
                            await delete_tasks(user, call.function.arguments),
                            ensure_ascii=False,
                        ),
                    }
                )

            # elif function_name == "close_task":
            #     tool_outputs.append(
            #         {
            #             "tool_call_id": call.id,
            #             "output": json.dumps(
            #                 await update_task(
            #                     user, call.function.arguments
            #                 ),
            #                 ensure_ascii=False,
            #             ),
            #         }
            #     )

            elif function_name == "update_task":
                tool_outputs.append(
                    {
                        "tool_call_id": call.id,
                        "output": json.dumps(
                            await update_task(user, call.function.arguments),
                            ensure_ascii=False,
                        ),
                    }
                )

            elif function_name == "search":
                tool_outputs.append(
                    {
                        "tool_call_id": call.id,
                        "output": json.dumps(
                            await index.fetch_related_task_ids(ray, user, call.function.arguments),
                            ensure_ascii=False,
                            separators=(",", ":"),
                        ),
                    }
                )

            else:
                log.info(ray, f"unexpected function called: {function_name}")
                raise RuntimeError(f"unexpected function called: {function_name}")

    if tool_outputs:
        try:
            await ai.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id, run_id=run_id, tool_outputs=tool_outputs
            )

            log.info(ray, f"Submitted function call outputs: {tool_outputs}")

        except:  # noqa: E722
            # For some reason, from time to time OAI API returns 404 on this call.
            # Potentially, retry will help.
            await ai.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id, run_id=run_id, tool_outputs=tool_outputs
            )

            # Wait for some time, for AI to process the function outputs.
            await asyncio.sleep(1.5)


async def compose_tasks_query(
    session,
    url_prefix: str,
    user: TelegramUserCtx,
    arguments: str,
) -> dict:
    # From time to time AI passes invalid JSON as arguments (empty string).
    if arguments == "":
        arguments = "{}"

    args = __ai_arguments_to_json(arguments)
    headers = await users.get_user_api_key_by_chat_id(session, user)

    url = URL(url_prefix)

    params = {}
    if args.get("inbox", False):
        params["inbox"] = "true"

    if args.get("priority", False):
        priority_map = {"!": "%21", "!!": "%21%21", "!!!": "%21%21%21"}
        params["p"] = priority_map.get(args["priority"], "")

    if args.get("any_all_priority_tasks") is True:
        params["all_priority_tasks"] = "true"

    if args.get("status", False):
        params["s"] = "closed"
    else:
        params["s"] = "null"

    if args.get("all_context", False):
        params["all_context"] = "true"

    # Date range filters
    today = await now_according_to_users_timezone(user)
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = timedelta(microseconds=-1)
    period_map = {
        "today": (today, today + timedelta(days=1) + end_of_day),
        "tomorrow": (today + timedelta(days=1), today + timedelta(days=2) + end_of_day),
        "next_3_days": (today + timedelta(days=1), today + timedelta(days=4) + end_of_day),
        "current_work_week": (today - timedelta(days=today.weekday()), today + timedelta(days=5 - today.weekday()) + end_of_day),
        "current_weekend": (today + timedelta(days=(5 - today.weekday())), today + timedelta(days=(7 - today.weekday())) + end_of_day),
        "current_week": (today - timedelta(days=today.weekday()), today + timedelta(days=(7 - today.weekday())) + end_of_day),
        "next_week": (today - timedelta(days=today.weekday()) + timedelta(weeks=1), today + timedelta(days=(7 - today.weekday())) + timedelta(weeks=1) + end_of_day),
        "next_work_week": (today - timedelta(days=today.weekday()) + timedelta(weeks=1), today + timedelta(days=5 - today.weekday()) + timedelta(weeks=1) + end_of_day),
        "next_week_weekend": (today + timedelta(days=(5 - today.weekday())) + timedelta(weeks=1), today + timedelta(days=(7 - today.weekday())) + timedelta(weeks=1) + end_of_day),
        "next_weekend": (today + timedelta(days=(5 - today.weekday())) + timedelta(weeks=1), today + timedelta(days=(7 - today.weekday())) + timedelta(weeks=1) + end_of_day),
        "next_monday": (today + timedelta(days=(7 - today.weekday())), today + timedelta(days=(8 - today.weekday())) + end_of_day),
        "next_tuesday": (today + timedelta(days=(8 - today.weekday())), today + timedelta(days=(9 - today.weekday())) + end_of_day),
        "next_wednesday": (today + timedelta(days=(9 - today.weekday())), today + timedelta(days=(10 - today.weekday())) + end_of_day),
        "next_thursday": (today + timedelta(days=(10 - today.weekday())), today + timedelta(days=(11 - today.weekday())) + end_of_day),
        "next_friday": (today + timedelta(days=(11 - today.weekday())), today + timedelta(days=(12 - today.weekday())) + end_of_day),
        "next_saturday": (today + timedelta(days=(12 - today.weekday())), today + timedelta(days=(13 - today.weekday())) + end_of_day),
        "next_sunday": (today + timedelta(days=(13 - today.weekday())), today + timedelta(days=(14 - today.weekday())) + end_of_day),
        # "for_period" seems to be a placeholder and might need to be handled differently
    }

    for_period = args.get("for_period")

    if args.get("after"):
        params["deadline_range_after"] = args.get("after")
    if args.get("before"):
        params["deadline_range_before"] = args.get("before")
    if for_period:    
        if for_period in period_map:
            after, before = period_map[for_period]
            if args.get("for_period") != "today":
                params["deadline_range_after"] = after.isoformat()
            params["deadline_range_before"] = before.isoformat()
            if for_period == "today":
                params["t"] = "True"
    else:
        if args.get("after"):
            params["deadline_range_after"] = __correct_timestamp(args.get("after"))
        if args.get("before"):
            params["deadline_range_before"] = __correct_timestamp(args.get("before"))

    if "query" in args:
        params["query"] = args["query"]

    url = url.with_query(params)

    return {
        "headers": headers,
        "url": str(url),
    }


def __ai_arguments_to_json(arguments: str) -> dict:
    """
    Corrects function argumetns provided by AI (sjon string) which usually contains errors.
    Returns a dictionary with corrected arguments.
    """

    arguments = (
        arguments.replace("\\\\r", "")
        .replace("\\\\n", "")
        .replace("\\\\t", "")
        .replace("\\r", "")
        .replace("\\n", "")
        .replace("\\t", "")
    )
    return json.loads(arguments)


def __correct_timestamp(timestamp: str) -> str:
    """
    Corrects the timestamp generated by the AI, and usually containing errors.

    Args:
        timestamp (str): The timestamp to be corrected.

    Returns:
        str: The corrected timestamp.
    """

    if "t" in timestamp:
        timestamp = timestamp.replace("t", "T")

    if timestamp[-1] != "Z":
        # Replace small z with upper case Z.
        if timestamp[-1] == "z":
            timestamp = timestamp[:-1] + "Z"
        else:
            timestamp += "Z"

    return timestamp

async def decrement_user_requests(user: TelegramUserCtx):
    async with aiohttp.ClientSession() as session:
        headers = await users.get_user_api_key_by_chat_id(session, user)
        url = settings.PAYMENTS_API_URL + 'subtract-request/'
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                response_text = await response.text()
                raise RuntimeError(f"Failed to decrement user requests: {response.status} - {response_text}")