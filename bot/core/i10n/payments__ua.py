import settings


def request_declension(requests: int) -> str:
    if requests % 10 == 1 and requests % 100 != 11:
        return "запит"
    elif 2 <= requests % 10 <= 4 and (requests % 100 < 10 or requests % 100 >= 20):
        return "запити"
    else:
        return "запитів"


def invoice_title(requests: int) -> str:
    return f"Покупка {requests} {request_declension(requests)}"


def invoice_description(requests: int) -> str:
    return f"Пакет на {requests} {request_declension(requests)}"


def one_month_subscription_price(price: str) -> str:
    return f"1 місяць — {price} грн/місяць"


def three_months_subscription_price(price: str) -> str:
    return f"3 місяці — {price} грн/місяць"


def six_months_subscription_price(price: str) -> str:
    return f"6 місяців — {price} грн/місяць"


def currency() -> str:
    return "UAH"


def choose_subscription() -> str:
    return "Оберіть бажану підписку:"


def subscription_paid_message() -> str:
    return "Дякуємо за підписку, тепер ви можете використовувати всі функції Efi! 🚀. Напишіть нам в підтримку, якщо у вас виникли проблеми @efi_support"


def active_subscription(date: str) -> str:
    return f"Ваша підписка активна до {date}"


def continue_subscription() -> str:
    return "Продовжити підписку"


def support() -> str:
    return "Підтримка"


def support_link(link: str) -> str:
    return f"Посилання на канал підтримки: {link}"


def subscribe() -> str:
    return "Підписатися"


def subscription() -> str:
    return "Тарифи та налаштування підписки"


def subscription_details() -> str:
    return "Деталі підписки:"


def requests_100_price(price: str) -> str:
    return f"100 запитів — {price} $"


def requests_500_price(price: str) -> str:
    return f"500 запитів — {price}$"


def requests_1000_price(price: str) -> str:
    return f"1000 запитів — {price}$"


def choose_request_package() -> str:
    return "Оберіть бажану кількість запитів:"


def remaining_requests(requests: str) -> str:
    return f"У вас залишилося {requests} запитів"


def purchase_requests() -> str:
    return "Докупити запити"


def cancel_subscription() -> str:
    return "Скасувати підписку"


def resume_subscription() -> str:
    return "Відновити підписку"


def back() -> str:
    return "Назад"


def subscription_settings() -> str:
    return "Тарифи та налаштування підписок:"


def create_subscription() -> str:
    return "🔋 Створити підписку"


def create_subscription_header() -> str:
    return "Будь ласка, оформіть свою підписку за допомогою кнопки нижче:"


def subscription_paused_remaining_requests() -> str:
    return "Вашу підписку призупинено. Залишкові запити ви можете використовувати протягом наступних 30 днів, після чого вони анулюються."


def subscription_resumed() -> str:
    return "Вашу підписку відновлено. З поверненням  💚 "


def subscription_resumption_error() -> str:
    return (
        "Сталася помилка при відновленні підписки. Напишіть нам у підтримку, якщо у вас виникли проблеми @efi_support"
    )


def payment_failed() -> str:
    return "Платіж не пройшов. Будь ласка, спробуйте ще раз або зверніться до підтримки @efi_support."


def subscription_settings_portal() -> str:
    return "Настройки підписки"


def open_portal_link() -> str:
    return "Відкрити настройки"


def open_portal_link_header() -> str:
    return "Натисніть на кнопку нижче аби перейти до настройок"


def subscription_successful() -> str:
    return "🎉 Підписку активовано! Enjoy! ☺️ \n\n Якщо в тебе будуть питання пиши до нашої підтримки @efi_support"


def payment_unsuccessful() -> str:
    return "Нажаль, під час спроби оформлення підписки щось пішло не так на стороні платіжної системи 😔\n\nСпробуємо ще раз?"


def efi_features() -> str:
    return (
        "🟢 Плануйте задачі та активності з допомогою АІ\\. Це як персональний помічник, що завжди доступний\\.\n\n"
        "🟢 Додавайте контекст швидко і просто, прямо з улюбленого месенджера\\.\n\n"
        "🟢 Автоматично організовуйте події з врахуванням всіх можливих аспектів, відчуйте переваги ефективного тайм менеджменту\\.\n\n"
        "[🎯 Детальніше про можливості та переваги Efi](https://telegra.ph/EFI\\-UA\\-05\\-01)"
    )


def subscription_includes() -> str:
    monthly_calls = settings.MONTHLY_MESSAGE_LIMIT
    yearly_calls = settings.YEARLY_MESSAGE_LIMIT
    savings = settings.SUBSCRIPTION_PRICES["savings"]

    return (
        f"В підписку включено *{monthly_calls}* викликів АІ\\-помічника на місяць, або *{yearly_calls}* на рік \\(вигода — ${savings}\\)\n\n"
        f"_Цього вистачить, щоб спланувати та виконати орієнтовно {monthly_calls} задач, проте кінцева вартість залежить від способу використання АІ\\-помічника\\._\n\n"
        "[Повний перелік умов надання послуг](https://telegra.ph/Tarifnij-plan-07-08)"
    )


def subscription_price_400_month() -> str:
    monthly_price = settings.SUBSCRIPTION_PRICES["monthly"]
    monthly_calls = settings.MONTHLY_MESSAGE_LIMIT

    return f"🔋 ${monthly_price} — {monthly_calls} пов./місяць"


def subscription_price_4800_year() -> str:
    yearly_price = settings.SUBSCRIPTION_PRICES["yearly"]
    yearly_calls = settings.YEARLY_MESSAGE_LIMIT

    return f"🔋 ${yearly_price} — {yearly_calls} пов./рік"


def remaining_messages_info() -> str:
    return (
        "У тебе залишилось 40 повідомлень до АІ у цьому місяці\\.\n\n"
        "[Як діяти, якщо тобі знадобиться більше повідомлень у цьому місяці\\.](https://telegra.ph/FAQ-07-08-16)\n\n"
        "[Як використовувати повідомлення оптимально?](https://telegra.ph/FAQ-07-08-16)\n\n"
        "[Як переглянути залишок повідомлень?](https://telegra.ph/FAQ-07-08-16)\n\n"
        "[Що якщо повідомлення до АІ вичерпаються?](https://telegra.ph/FAQ-07-08-16)"
    )


def trial_activated_message(total_messages: int, remaining_messages: int, end_date: str) -> str:
    return (
        f"Активовано випробувальний період 🎉\n\n"
        f"Всього повідомлень\\: {total_messages}\n"
        f"*Повідомлень залишилось\\: {remaining_messages}*\n"
        f"Дата завершення: {end_date}\n\n"
        "[Які переваги у підписки\\?\n\n](https://telegra.ph/FAQ-07-08-16)"
        "[Як додати підписку\\?\n\n](https://telegra.ph/FAQ-07-08-16)"
        "[Як оптимально використовувати повідомлення\\?](https://telegra.ph/FAQ-07-08-16)"
    )


def trial_ended_message(total_messages: int, remaining_messages: int, end_date: str) -> str:
    return (
        f"Випробувальний період завершено\\.\n\n"
        f"Всього повідомлень\\: {total_messages}\n"
        f"*Повідомлень залишилось\\: {remaining_messages}*\n"
        f"Дата завершення\\: {end_date}\n\n"
        "[Як я можу продовжити користування?](https://telegra.ph/FAQ-07-08-16)"
    )


def subscription_active_message(
    start_date: str, plan_price: str, next_billing_date: str, total_messages: int, remaining_messages: int
) -> str:
    period = "міс\\." if plan_price == settings.SUBSCRIPTION_PRICES_MARKDOWN["monthly"] else "рік"
    return (
        f"Ваша підписка активна\\! 🎉\n\n"
        f"Створено\\: {start_date}\n"
        f"Тарифний план\\: {plan_price}\\$ / {period}\n"
        f"Дата наступного списання\\:\n"
        f"{next_billing_date}\n\n"
        f"Всього повідомлень\\: {total_messages}\n"
        f"*Повідомлень залишилось\\: {remaining_messages}*\n\n"
        "[Що якщо я використаю більше повідомлень, ніж передбачено тарифним планом?](https://telegra.ph/FAQ-07-08-16)\n\n"
        "[Як скасувати підписку?](https://telegra.ph/FAQ-07-08-16)\n\n"
        "[Як оптимально використовувати повідомлення?](https://telegra.ph/FAQ-07-08-16)\n"
    )


def subscription_cancelled_message(cancellation_date: str, plan_price: str) -> str:
    period = "міс\\." if plan_price == settings.SUBSCRIPTION_PRICES_MARKDOWN["monthly"] else "рік"
    return (
        f"Вашу підписку було скасовано 😔\n\n"
        f"Дата скасування\\: {cancellation_date}\n"
        f"Тарифний план\\: {plan_price}\\$ / {period}\n\n"
        "[Як я можу продовжити користування?](https://telegra.ph/FAQ-07-08-16)"
    )


def tariffs() -> str:
    return "Тарифи:"


def subscription_management() -> str:
    return "⚙️ Керування підпискою"


def view_payments() -> str:
    return "Переглянути платежі"


def subscription_will_be_cancelled_message(remaining_messages: int, end_date: str) -> str:
    return (
        f"Твою підписку буде скасовано\\.\n\n"
        f"*Залишок повідомлень \\({remaining_messages} пов\\.\\) можна буде використати до {end_date} р\\.,*"
        f"після цього доступ до АІ\\-функцій буде припинено, проте доступ до задач залишиться назавжди\\.\n\n"
        "Продовжити\\?"
    )


def i_like_efi() -> str:
    return "Ні, мені подобається Efi 💚"


def confirmation_of_cancel_subscription() -> str:
    return "Так, скасувати підписку"


def mutual_love() -> str:
    return "Це взаємно! 💚"


def subscription_cancelled_message_heartbreak() -> str:
    return "Твою підписку було скасовано 💔"


def free_trial_activated_message() -> str:
    return (
        "🎉 Твій безкоштовний період користування активовано\\! Enjoy\\! 😉\n\n"
        "Більше про нього можна знайти [за цим посиланням](https://telegra.ph/Per%D1%96od-viprobuvalnogo-koristuvannya-07-08)\\, або ж в налаштуваннях ⚙️"
    )


def free_trial_ended() -> str:
    return (
        "Твій безкоштовний період користування завершився. Щоб продовжити користування, будь ласка, створи підписку.\n\n"
        "Вона дозволить тобі і надалі користуватись 🤖 АІ-функціями Efi, а також підтримати проект 💚\n\n"
        "Вже створені раніше задачі ти завжди можеш переглянути. Все, як і раніше."
    )


def free_messages_credited(message_count: int) -> str:
    return f"{message_count} безкоштовних повідомлень нараховано\\! _Enjoy 💚\n\nЗ турботою\\, команда Efi\\!_"


def payment_failed_retry() -> str:
    return "Оплата за вашу підписку не пройшла. Будь ласка, спробуйте ще раз."


def retry_payment_button() -> str:
    return "Повторити оплату"
