from core.i10n import tasks_listing as i10n



def name_of_day(index: int, short=False) -> str:
    if short:
        return i10n.days_short()[index]
    else:
        return i10n.days()[index]

