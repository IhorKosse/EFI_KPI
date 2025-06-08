def days(hours: int, days: int) -> str:
    day_word = "day" if days == 1 else "days"
    if hours != 0:
        hour_word = "hour" if hours == 1 else "hours"
        return f"{int(days)} {day_word} and {int(hours)} {hour_word} left"
    else:
        return f"{int(days)} {day_word} left"


def hours(hours: int) -> str:
    hour_word = "hour" if hours == 1 else "hours"
    return f"{int(hours)} {hour_word} left"

def minutes(minutes: int) -> str:
    minute_word = "minute" if minutes == 1 else "minutes"
    return f"{int(minutes)} {minute_word} left"

def right_now() -> str:
    return "Right now"