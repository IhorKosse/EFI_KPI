import datetime
import random


def no_tasks_for_today() -> str:
    with open("responses/it_no_tasks_for_today.txt", "r") as f:
        lines = f.readlines()
    return random.choice(lines).strip()


def working_one_moment() -> str:
    with open("responses/ua_one_moment_working.txt", "r") as f:
        lines = f.readlines()
    return random.choice(lines).strip()


def no_tasks() -> str:
    # TODO: Rendere il bot più naturale, fornire più di una risposta.
    return "Nessun compito ☺️\nVuoi aggiungerne uno?"


def no_tasks_for_this_day() -> str:
    # TODO: Rendere il bot più naturale, fornire più di una risposta.
    return "Non ci sono compiti per questo giorno."


def no_tasks_in_inbox() -> str:
    # TODO: Rendere il bot più naturale, fornire più di una risposta.
    return "Posta in arrivo vuota ☺️\nVuoi aggiungere qualcosa?"


def start_command_text() -> str:
    return (
        "Ciao, sono Efi, il tuo chat-bot per la pianificazione! 👋\n\n"
        "Siamo informali, parlami come preferisci. Sono il tuo eroe nel mondo della gestione delle attività! 🚀\n\n"
        "Pianifica, crea, chiudi, aggiorna - tutto è nelle tue mani. Per vedere come funziona, leggi <a href='https://telegra.ph/EFI-UA-05-01'>Telegraph</a> - è tutto chiaro lì. 📖\n\n"
        "Scrivimi ciò di cui hai bisogno e io farò il resto. Rendi le tue giornate efficaci e semplici insieme a me! 💪🏼"
    )


def timezone_prompt() -> str:
    return "Scegli il tuo fuso orario:"


def timezone_first() -> str:
    return "Per favore imposta prima il tuo fuso orario, usa /start"


def timezone_update_message(picked_timezone_shift: str) -> str:
    return f"Grazie, il tuo fuso orario è ora UTC {picked_timezone_shift}, puoi cambiarlo più tardi nelle impostazioni."


def tutorial_start_message(task_prompt: str) -> str:
    return (
        f"È molto semplice, proviamo subito. Aggiungi il tuo primo compito, ecco esempi generali di attività:\n {task_prompt}"
        "\nOppure scrivi qualcosa di tuo e guarda il risultato. Per capire in dettaglio come creare, aggiornare, eliminare e cercare compiti leggi [Telegraph](https://telegra.ph/EFI-EN-05-01)."
    )


def task_start_prompt() -> str:
    return (
        "\n *\- Ricordami di guardare il podcast tra 20 minuti.\n"
        " \- Ricordami di pulire la galleria tra un'ora (ci vorrà un'ora).\n"
        " \- Allenamento dalle 14 alle 16 oggi.*\n"
    )


def task_completion_prompt() -> str:
    return "Rimanda la lettura del Telegraph di Efi per un'altra ora."


def task_completion_message(task_prompt: str) -> str:
    return f"Ottimo, hai aggiunto il tuo primo compito, ora prova ad aggiornarlo scrivendo: '{task_prompt}' 📖"


def task_update_prompt() -> str:
    return "Ho già letto il Telegraph di Efi."


def task_update_message(task_prompt: str) -> str:
    return f"Super, compito aggiornato. Leggi il Telegraph e cancella il compito o semplicemente scrivi: '{task_prompt}' 📖"


def task_close_message() -> str:
    return (
        "Ta-dam, ho eliminato il compito e ora sai quanto è facile gestire le attività con me. 💪\n\n"
        "Ti aspettano molte altre funzionalità interessanti. Andiamo verso l'efficienza con Efi! ✨👊"
    )


def close_tutorial() -> str:
    return "Fine del tutorial."


def tutorial_complete_message() -> str:
    return (
        "Tutorial completato, se non hai terminato il tutorial fino alla fine, non dimenticare di chiudere i tuoi compiti di prova). "
        "Per saperne di più, vedi <a href='https://telegra.ph/EFI-EN-05-01'>Telegraph</a>"
    )


def oops() -> str:
    return (
        "Ops, qualcosa è andato storto. Proviamo di nuovo? "
        "Meglio riformulare il compito. Contattaci se vuoi aiuto su @efi_support"
    )


def invalid_command() -> str:
    return "Comando non valido. Contattaci se vuoi aiuto su @efi_support"


def smth_wrong() -> str:
    return (
        "Qualcosa è andato storto da parte nostra, sappiamo già e stiamo lavorando per risolvere. "
        "Contattaci se vuoi aiuto su @efi_support"
    )


def non_text_message() -> str:
    return "I messaggi non testuali non sono supportati al momento. Contattaci se vuoi aiuto su @efi_support."


def settings_menu_text() -> str:
    return "Impostazioni, scegli cosa vuoi cambiare"


def settings_timezone_update_message(picked_timezone_shift_hours: str) -> str:
    return f"Grazie, il tuo fuso orario è ora {picked_timezone_shift_hours} UTC."


def current_time(offset_time: datetime) -> str:
    return f"Ora corrente: {offset_time.replace(microsecond=0)}"


def today() -> str:
    return "📅 Oggi"


def all_tasks() -> str:
    return "Tutti i compiti"


def auto_reminders() -> str:
    return "Promemoria automatici:"


def auto_reminders_on() -> str:
    return "In orario"


def auto_reminders_off() -> str:
    return "Disattivati"


def auto_reminders_15() -> str:
    return "15 min prima"


def auto_reminders_30() -> str:
    return "30 min prima"


def auto_reminders_60() -> str:
    return "60 min prima"


def todays_tasks() -> str:
    return "Compiti di oggi"


def overdue_tasks() -> str:
    return "Compiti scaduti"


def no_todays_tasks() -> str:
    return "Nessun compito per oggi"


def tomorrows_tasks() -> str:
    return "Compiti di domani"


def no_tomorrows_tasks() -> str:
    return "Nessun compito per domani"


def weeks_tasks() -> str:
    return "Compiti della settimana"


def no_weeks_tasks() -> str:
    return "Nessun compito per questa settimana"


def workweeks_tasks() -> str:
    return "Compiti giorni lavorativi"


def no_workweeks_tasks() -> str:
    return "Nessun compito per i giorni lavorativi"


def weekends_tasks() -> str:
    return "Compiti del fine settimana"


def no_weekends_tasks() -> str:
    return "Nessun compito per il fine settimana"


def two_weeks_tasks() -> str:
    return "Compiti delle prossime due settimane"


def no_two_weeks_tasks() -> str:
    return "Nessun compito per le prossime due settimane"


def inbox_tasks() -> str:
    return "Compiti nella posta in arrivo"


def no_inbox_tasks() -> str:
    return "Nessun compito nella posta in arrivo"


def days() -> list[str]:
    return ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]


def days_short() -> list[str]:
    return ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]


def months() -> list[str]:
    return [
        "Gennaio",
        "Febbraio",
        "Marzo",
        "Aprile",
        "Maggio",
        "Giugno",
        "Luglio",
        "Agosto",
        "Settembre",
        "Ottobre",
        "Novembre",
        "Dicembre",
    ]


def months_short() -> list[str]:
    return ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]


def total_tasks() -> str:
    return "Totale compiti"


def load_more_tasks() -> str:
    return "Carica altri compiti"


def by() -> str:
    return "di "
