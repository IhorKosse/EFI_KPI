import settings


def invoice_title(requests: int) -> str:
    request_word = "Richiesta" if requests == 1 else "Richieste"
    return f"{requests} {request_word}"


def invoice_description(requests: int) -> str:
    request_word = "richiesta" if requests == 1 else "richieste"
    return f"Pacchetto di {requests} {request_word}"


def one_month_subscription_price(price: str) -> str:
    return f"1 mese — {price}$/mese"


def three_months_subscription_price(price: str) -> str:
    return f"3 mesi — {price}$/mese"


def six_months_subscription_price(price: str) -> str:
    return f"6 mesi — {price}$/mese"


def currency() -> str:
    return "USD"


def choose_subscription() -> str:
    return "Seleziona il tuo abbonamento desiderato:"


def subscription_paid_message() -> str:
    return "Grazie per il tuo abbonamento, ora puoi utilizzare tutte le funzionalità di Efi! 🚀 Facci sapere se hai bisogno di aiuto @efi_support"


def active_subscription(date: str) -> str:
    return f"Abbonamento attivo fino al {date}"


def continue_subscription() -> str:
    return "Continua abbonamento"


def support() -> str:
    return "Supporto"


def support_link(link: str) -> str:
    return f"Link al canale di supporto: {link}"


def subscribe() -> str:
    return "Abbonati"


def subscription() -> str:
    return "Piani e Abbonamenti"


def subscription_details() -> str:
    return "Dettagli dell'abbonamento:"


def requests_100_price(price: str) -> str:
    return f"100 richieste — {price}$"


def requests_500_price(price: str) -> str:
    return f"500 richieste — {price}$"


def requests_1000_price(price: str) -> str:
    return f"1000 richieste — {price}$"


def choose_request_package() -> str:
    return "Scegli il numero di richieste desiderato:"


def remaining_requests(requests: str) -> str:
    return f"Hai {requests} richieste rimanenti"


def purchase_requests() -> str:
    return "Acquista più richieste"


def cancel_subscription() -> str:
    return "Annulla abbonamento"


def resume_subscription() -> str:
    return "Riprendi abbonamento"


def back() -> str:
    return "Indietro"


def subscription_settings() -> str:
    return "Impostazioni piani e abbonamenti:"


def create_subscription() -> str:
    return "🔋 Crea abbonamento"


def create_subscription_header() -> str:
    return "Completa il tuo abbonamento utilizzando il pulsante qui sotto:"


def subscription_paused_remaining_requests() -> str:
    return "Il tuo abbonamento è stato sospeso. Puoi utilizzare le richieste rimanenti entro i prossimi 30 giorni, dopodiché scadranno."


def subscription_resumed() -> str:
    return "Il tuo abbonamento è stato ripreso. Bentornato 💚"


def subscription_resumption_error() -> str:
    return "Si è verificato un errore durante la ripresa dell'abbonamento. Contatta il supporto se riscontri problemi @efi_support"


def payment_failed() -> str:
    return "Pagamento fallito. Riprova o contatta il supporto @efi_support."


def subscription_settings_portal() -> str:
    return "Impostazioni abbonamento"


def open_portal_link() -> str:
    return "Apri impostazioni"


def open_portal_link_header() -> str:
    return "Clicca il pulsante qui sotto per andare alle impostazioni"


def subscription_successful() -> str:
    return "🎉 Il tuo abbonamento è stato attivato! Buon divertimento! ☺️ \n\nSe hai domande, contatta il nostro supporto @efi_support"


def payment_unsuccessful() -> str:
    return "Purtroppo, qualcosa è andato storto con il sistema di pagamento durante il tentativo di abbonamento 😔\n\nProviamo di nuovo?"


def efi_features() -> str:
    return (
        "🟢 Pianifica attività e compiti con l'aiuto dell'AI\\. È come avere un assistente personale sempre disponibile\\.\n\n"
        "🟢 Aggiungi contesto rapidamente e facilmente, direttamente dal tuo messenger preferito\\.\n\n"
        "🟢 Organizza automaticamente gli eventi considerando tutti gli aspetti possibili, sperimenta i vantaggi della gestione efficace del tempo\\.\n\n"
        "[🎯 Scopri di più sulle funzionalità e i vantaggi di Efi](https://telegra.ph/EFI-EN-05-01)"
    )


def subscription_includes() -> str:
    monthly_calls = settings.MONTHLY_MESSAGE_LIMIT
    yearly_calls = settings.YEARLY_MESSAGE_LIMIT
    savings = settings.SUBSCRIPTION_PRICES["savings"]

    return (
        f"L'abbonamento include *{monthly_calls}* messaggi dell'assistente AI al mese, o *{yearly_calls}* all'anno \\(risparmio — ${savings}\\)\n\n"
        f"_Questo è sufficiente per pianificare ed eseguire circa {monthly_calls} compiti, ma il costo finale dipende da come utilizzi l'assistente AI\\._\n\n"
        "[Elenco completo dei termini del servizio\\.](https://telegra.ph/Pricing-Plan-07-18)"
    )


def subscription_price_400_month() -> str:
    monthly_price = settings.SUBSCRIPTION_PRICES["monthly"]
    monthly_calls = settings.MONTHLY_MESSAGE_LIMIT

    return f"🔋 ${monthly_price} — {monthly_calls} messaggi/mese"


def subscription_price_4800_year() -> str:
    yearly_price = settings.SUBSCRIPTION_PRICES["yearly"]
    yearly_calls = settings.YEARLY_MESSAGE_LIMIT

    return f"🔋 ${yearly_price} — {yearly_calls} messaggi/anno"


def remaining_messages_info() -> str:
    return (
        "Hai 40 messaggi rimanenti all'AI questo mese\\.\n\n"
        "Cosa fare se hai bisogno di più messaggi questo mese\\.\n\n"
        "[Come utilizzare i messaggi in modo ottimale?](https://telegra.ph/FAQ-07-18-9)\n\n"
        "[Come controllare i messaggi rimanenti?](https://telegra.ph/FAQ-07-18-9)\n\n"
        "[Cosa succede se i messaggi all'AI finiscono?](https://telegra.ph/FAQ-07-18-9)"
    )


def trial_activated_message(total_messages: int, remaining_messages: int, end_date: str) -> str:
    return (
        f"Periodo di prova attivato 🎉\n\n"
        f"Messaggi totali\\: {total_messages}\n"
        f"*Messaggi rimanenti\\: {remaining_messages}*\n"
        f"Data di fine\\: {end_date}\n\n"
        "[Quali sono i vantaggi dell'abbonamento\\?](https://telegra.ph/FAQ-07-18-9)\n\n"
        "[Come aggiungere un abbonamento\\?](https://telegra.ph/FAQ-07-18-9)\n\n"
        "[Come utilizzare i messaggi in modo ottimale\\?](https://telegra.ph/FAQ-07-18-9)"
    )


def trial_ended_message(total_messages: int, remaining_messages: int, end_date: str) -> str:
    return (
        f"Periodo di prova terminato\\.\n\n"
        f"Messaggi totali\\: {total_messages}\n"
        f"*Messaggi rimanenti\\: {remaining_messages}*\n"
        f"Data di fine\\: {end_date}\n\n"
        "[Come posso continuare a utilizzare il servizio\\?](https://telegra.ph/FAQ-07-18-9)"
    )


def subscription_active_message(
    start_date: str, plan_price: str, next_billing_date: str, total_messages: int, remaining_messages: int
) -> str:
    period = "mese" if plan_price == settings.SUBSCRIPTION_PRICES_MARKDOWN["monthly"] else "anno"
    return (
        f"Il tuo abbonamento è attivo\\! 🎉\n\n"
        f"Creato il: {start_date}\n"
        f"Prezzo del piano: {plan_price}\\$ / {period}\n"
        f"Prossima data di fatturazione: {next_billing_date}\n\n"
        f"Messaggi totali: {total_messages}\n"
        f"*Messaggi rimanenti: {remaining_messages}*\n\n"
        "[Cosa succede se utilizzo più messaggi di quelli previsti dal piano?](https://telegra.ph/FAQ-07-18-9)\n\n"
        "[Come annullare l'abbonamento?](https://telegra.ph/FAQ-07-18-9)\n\n"
        "[Come utilizzare i messaggi in modo ottimale?](https://telegra.ph/FAQ-07-18-9)\n"
    )


def subscription_cancelled_message(cancellation_date: str, plan_price: str) -> str:
    period = "mese" if plan_price == settings.SUBSCRIPTION_PRICES_MARKDOWN["monthly"] else "anno"
    return (
        f"Il tuo abbonamento è stato annullato 😔\n\n"
        f"Data di annullamento: {cancellation_date}\n"
        f"Prezzo del piano: {plan_price}\\$ / {period}\n\n"
        "[Come posso continuare a utilizzare il servizio?](https://telegra.ph/FAQ-07-18-9)"
    )


def tariffs() -> str:
    return "Tariffe:"


def subscription_management() -> str:
    return "⚙️ Gestione Abbonamento"


def view_payments() -> str:
    return "Visualizza Pagamenti"


def subscription_will_be_cancelled_message(remaining_messages: int, end_date: str) -> str:
    return (
        f"Il tuo abbonamento sarà annullato\\.\n\n"
        f"*I messaggi rimanenti \\({remaining_messages} messaggi\\) possono essere utilizzati fino al {end_date},*"
        f"dopo di che l'accesso alle funzionalità AI sarà terminato, ma l'accesso ai compiti rimarrà per sempre\\.\n\n"
        "Continuare\\?"
    )


def i_like_efi() -> str:
    return "No, mi piace Efi 💚"


def confirmation_of_cancel_subscription() -> str:
    return "Sì, annulla l'abbonamento"


def mutual_love() -> str:
    return "È reciproco! 💚"


def subscription_cancelled_message_heartbreak() -> str:
    return "Il tuo abbonamento è stato annullato 💔"


def free_trial_activated_message() -> str:
    return (
        "🎉 Il tuo periodo di prova gratuito è stato attivato\\! Buon divertimento\\! 😉\n\n"
        "Puoi trovare maggiori informazioni [a questo link](https://telegra.ph/Trial-Period-Usage-07-08-2)\\, o nelle impostazioni ⚙️"
    )


def free_trial_ended() -> str:
    return (
        "Il tuo periodo di prova gratuito è terminato. Per continuare a utilizzare il servizio, crea un abbonamento.\n\n"
        "Questo ti permetterà di continuare a utilizzare le funzionalità AI di 🤖 Efi e supportare il progetto 💚\n\n"
        "Puoi sempre visualizzare i compiti creati in precedenza. Tutto rimane come era."
    )


def free_messages_credited(message_count: int) -> str:
    return f"{message_count} messaggi gratuiti accreditati\\! _Buon divertimento 💚\n\nCon cura\\, il team di Efi\\!_"


def payment_failed_retry() -> str:
    return "Il pagamento del tuo abbonamento è fallito. Riprova."


def retry_payment_button() -> str:
    return "Riprova Pagamento"
