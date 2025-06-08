def days(hours: int, days: int) -> str:
    day_word = "giorno" if days == 1 else "giorni"
    if hours != 0:
        hour_word = "ora" if hours == 1 else "ore"
        return f"{int(days)} {day_word} e {int(hours)} {hour_word} rimanenti"
    else:
        return f"{int(days)} {day_word} rimanenti"


def hours(hours: int) -> str:
    hour_word = "ora" if hours == 1 else "ore"
    return f"{int(hours)} {hour_word} rimanenti"


def minutes(minutes: int) -> str:
    minute_word = "minuto" if minutes == 1 else "minuti"
    return f"{int(minutes)} {minute_word} rimanenti"


def right_now() -> str:
    return "Proprio adesso"
