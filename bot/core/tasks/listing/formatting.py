import datetime

from core.responses import name_of_day
from core.stringutils import escape_markdown_v2
from core.i10n import tasks_listing as i10n

def monthly_listing_header_markdown(target_day: datetime.datetime, now: datetime.datetime, tasks_count: int = 0) -> str:
    # LOCALIZATION
    # TODO: For now, only Ukrainian is supported.
    return __listing_header_ua_markdown(target_day, now, tasks_count)


def weekly_listing_header_markdown(target_day: datetime.datetime, now: datetime.datetime, tasks_count: int = 0) -> str:
    # LOCALIZATION
    # TODO: For now, only Ukrainian is supported.
    return __listing_header_ua_markdown(target_day, now, tasks_count)


def monthly_listing_tasks_markdown(day: datetime, tasks: list, now: datetime.datetime) -> str:
    # LOCALIZATION
    # TODO: For now, only Ukrainian is supported.
    return __listing_tasks_ua_markdown(day, tasks, now)


def weekly_listing_tasks_markdown(day: datetime, tasks: list, now: datetime.datetime) -> str:
    # LOCALIZATION
    # TODO: For now, only Ukrainian is supported.
    return __listing_tasks_ua_markdown(day, tasks, now)


def sequential_listing_dates_splitter_header(d: datetime) -> str:
    # LOCALIZATION
    # TODO: For now, only Ukrainian is supported.
    return __sequential_listing_dates_splitter_header_ua(d)


def __sequential_listing_dates_splitter_header_ua(d: datetime) -> str:
    day = name_of_day(d.weekday())
    return f"*{day}, {d.strftime('%d / %m')}*"


# TODO: Use user's timezone here instead of now.
async def to_message(task: dict, now: datetime.datetime) -> str:
    """
    Converts a task dictionary into a formatted message string, used for sending tasks to the user.

    Args:
        task (dict): The task dictionary containing task information.

    Returns:
        str: The formatted message string suitable for sending to the user.
    """

    title = escape_markdown_v2(task.get("name", ""))

    deadline_date = task.get("deadline_date")
    deadline_datetime = task.get("deadline_datetime")
    start_date = task.get("start_date")
    start_datetime = task.get("start_datetime")
    deadline = None
    if start_datetime:
        deadline = datetime.datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%SZ")
    elif start_date:
        deadline = datetime.datetime.strptime(start_date, "%Y-%m-%d")

    if deadline_datetime:
        deadline = datetime.datetime.strptime(deadline_datetime, "%Y-%m-%dT%H:%M:%SZ")
    elif deadline_date:
        deadline = datetime.datetime.strptime(deadline_date, "%Y-%m-%d")

    priority_map = {
        "": " ",
        "!": "❕",
        "!!": "❗️",
        "!!!": "‼️"
    }
    task_priority = priority_map.get(task.get("priority", ""), " ")



    if deadline and deadline.date() < now.date():
        return f"{task_priority} {title}"
    elif not deadline:
        return f"{task_priority} {title}"
    else:
        time_info = __format_task_time_info(task, now)
        return f"{task_priority} {title} {time_info}"

def __listing_header_ua_markdown(target_day: datetime.datetime, now: datetime.datetime, tasks_count: int = 0) -> str:
    day_name = name_of_day(target_day.weekday())
    day_number = target_day.strftime("%d")
    month_number = target_day.strftime("%m")

    header = f"> *{day_name}, {day_number}/{month_number}*"
    if tasks_count:
        header += f"\n{i10n.total_tasks()} — {tasks_count}"

    return header + "\n\n"


def __listing_tasks_ua_markdown(day: datetime, tasks: list, now: datetime.datetime) -> str:
    if not tasks:
        return f"{i10n.no_tasks_for_this_day()}"

    overdue_tasks = []
    today_tasks = []
    today_date = now.date()

    message = ""
    for task in tasks:
        deadline_date = task.get("deadline_date")
        deadline_datetime = task.get("deadline_datetime")
        start_date = task.get("start_date")
        start_datetime = task.get("start_datetime")
        deadline = None
        if start_datetime:
            deadline = datetime.datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%SZ")
        elif start_date:
            deadline = datetime.datetime.strptime(start_date, "%Y-%m-%d")

        if deadline_datetime:
            deadline = datetime.datetime.strptime(deadline_datetime, "%Y-%m-%dT%H:%M:%SZ")
        elif deadline_date:
            deadline = datetime.datetime.strptime(deadline_date, "%Y-%m-%d")

        if day.date() == today_date:
            message = ""
            if deadline and deadline < now:
                if deadline.date() < today_date:
                    overdue_tasks.append(task)
                else:
                    today_tasks.append(task)
            else:
                today_tasks.append(task)
            

            if overdue_tasks:
                message += f"{i10n.overdue_tasks()}\n"
                for task in overdue_tasks:
                    message += __format_task_for_short_listing_ua(task, now, True)


            if overdue_tasks:
                message += "\n"  # Add a separator if there are overdue tasks
            message += f"{i10n.todays_tasks()}\n"
            for task in today_tasks:
                message += __format_task_for_short_listing_ua(task, now, False)


        else:
            message += __format_task_for_short_listing_ua(task, now, False)

    return message

def __format_task_for_short_listing_ua(task: dict, now: datetime.datetime, overdue: bool) -> str:
    priority_map = {
        "": " ",
        "!": "❕",
        "!!": "❗️",
        "!!!": "‼️"
    }
    task_priority = priority_map.get(task.get("priority", ""), " ")
    task_name = escape_markdown_v2(task.get("name", "<No name>"))
    status = task.get("status")

    if status == "closed":
        return f"\\- ~{task_name}~\n"

    if overdue:
        return f"\\- {task_priority} {task_name} \n"
    else:
        time_info = __format_task_time_info(task, now)
        return f"\\- {task_priority} {task_name} {time_info}\n"
        

def format_time(dt_str):
    return datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ").strftime("%H:%M")

def append_time_info(time_str, is_end, now, message):
    if now > datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ"):
        prefix = "⌛"
    elif now + datetime.timedelta(hours=3) > datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ"):
        prefix = "⏳"
    else:
        prefix = ""
    
    suffix = i10n.by() if is_end else ""
    return f"{prefix} {message} \\({suffix}{format_time(time_str)}\\)"


def __format_task_time_info(task: dict, now: datetime.datetime) -> str:
    message = ""
    raw_deadline = task.get("deadline_datetime")
    raw_start = task.get("start_datetime")
    day_deadline = task.get("deadline_date")

    if raw_start and raw_deadline:
        formatted_start = format_time(raw_start)
        formatted_deadline = format_time(raw_deadline)
        start_dt = datetime.datetime.strptime(raw_start, "%Y-%m-%dT%H:%M:%SZ")
        deadline_dt = datetime.datetime.strptime(raw_deadline, "%Y-%m-%dT%H:%M:%SZ")

        if deadline_dt < now:
            message += "⌛ "
        elif now + datetime.timedelta(hours=3) > start_dt:
            message += "⏳ "

        time_range = formatted_start if formatted_start == formatted_deadline else f"{formatted_start} — {formatted_deadline}"
        message += f"\\({time_range}\\)"

    elif raw_start:
        message += append_time_info(raw_start, False, now, "")

    elif raw_deadline:
        message += append_time_info(raw_deadline, True, now, "")


    elif day_deadline:
        day_deadline_dt = datetime.datetime.strptime(day_deadline, "%Y-%m-%d")
        if day_deadline_dt < now.replace(hour=0, minute=0, second=0, microsecond=0):
            message += "⌛ "


    return message