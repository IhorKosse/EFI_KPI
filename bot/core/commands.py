from core.settings.commands import handle_settings_command
from core.tasks.listing.commands import (
    list_all_tasks_sequentially,
    list_inbox_tasks_sequentially,
    list_month_tasks,
    list_next_month_tasks,
    list_next_week_tasks,
    list_today_tasks_sequentially,
    list_tommorow_tasks_sequentially,
    list_week_tasks,
    list_workweek_tasks,
)
from core.tutorial.commands import handle_start_command

# TODO: [Dima] Drop it.
# async def show_tasks_on_users_ui(bot, ai, rc, arguments, user_id, user_full_name):
#     pass
#     # return await __list_tasks(
#     #     0,
#     #     bot,
#     #     ai,
#     #     rc,
#     #     user_id,
#     #     user_full_name,
#     #     arguments,
#     #     None,
#     #     "list all tasks",
#     #     None,
#     #     populate_thread_context=True,
#     # )


commands = {
    "/start": handle_start_command,
    "start": handle_start_command,

    "/settings": handle_settings_command,
    "settings": handle_settings_command,

    #
    # Tasks listing
    #

    # Sequential listings
    "/i": list_inbox_tasks_sequentially,
    "i": list_inbox_tasks_sequentially,

    "/l": list_all_tasks_sequentially,
    "l": list_all_tasks_sequentially,

    "/d": list_today_tasks_sequentially,
    "d": list_today_tasks_sequentially,

    "/t": list_tommorow_tasks_sequentially,
    "t": list_tommorow_tasks_sequentially,

    # "/wd": list_weekend_tasks,
    # "wd": list_weekend_tasks,

    # Week-based listings
    "/w": list_week_tasks,
    "w": list_week_tasks,

    "/ww": list_workweek_tasks,
    "ww": list_workweek_tasks,
    
    "/nw": list_next_week_tasks,
    "nw": list_next_week_tasks,

    # Month-based listings
    "/m": list_month_tasks,
    "m": list_month_tasks,

    "/nm": list_next_month_tasks,
    "nm": list_next_month_tasks,
}


def match(command: str):
    return commands.get(command)
