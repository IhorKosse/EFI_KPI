from core.common import TelegramUserCtx
from core.i10n import tasks_listing as i10n


def get_first_day_of_the_week(telegram_user: TelegramUserCtx) -> str:
    """
    Returns the first day of the week for the user's locale.
    Possible options are: MON, SUN.
    """

    #   Determine proper first day of the week for the user.
    #   Use back-end API to get user's locale and return proper day.

    # For now, return Monday as the first day of the week.
    return i10n.days_short()[0]


def short_days_titles(telegram_user: TelegramUserCtx) -> list:
    """
    Returns the list of short day titles for the user's locale.
    """

    #   Use back-end API to get user's locale and return proper short day titles.

    # For now, return short day titles from settings.
    return i10n.days_short()