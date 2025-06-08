from core.i10n.common import gen_response
from core.i10n import payments__ua as ua
from core.i10n import payments__en as en
from core.i10n import payments__it as it


def invoice_title(months: int) -> str:
    return gen_response(en.invoice_title, ua.invoice_title, it.invoice_title, months)


def invoice_description(months: int) -> str:
    return gen_response(en.invoice_description, ua.invoice_description, it.invoice_description, months)


def one_month_subscription_price(price: str) -> str:
    return gen_response(
        en.one_month_subscription_price, ua.one_month_subscription_price, it.one_month_subscription_price, price
    )


def three_months_subscription_price(price: str) -> str:
    return gen_response(
        en.three_months_subscription_price,
        ua.three_months_subscription_price,
        it.three_months_subscription_price,
        price,
    )


def six_months_subscription_price(price: str) -> str:
    return gen_response(
        en.six_months_subscription_price, ua.six_months_subscription_price, it.six_months_subscription_price, price
    )


def currency() -> str:
    return gen_response(en.currency, ua.currency, it.currency)


def choose_subscription() -> str:
    return gen_response(en.choose_subscription, ua.choose_subscription, it.choose_subscription)


def subscription_paid_message() -> str:
    return gen_response(en.subscription_paid_message, ua.subscription_paid_message, it.subscription_paid_message)


def active_subscription(date: str) -> str:
    return gen_response(en.active_subscription, ua.active_subscription, it.active_subscription, date)


def continue_subscription() -> str:
    return gen_response(en.continue_subscription, ua.continue_subscription, it.continue_subscription)


def support() -> str:
    return gen_response(en.support, ua.support, it.support)


def support_link(link: str) -> str:
    return gen_response(en.support_link, ua.support_link, it.support_link, link)


def subscribe() -> str:
    return gen_response(en.subscribe, ua.subscribe, it.subscribe)


def subscription() -> str:
    return gen_response(en.subscription, ua.subscription, it.subscription)


def subscription_details() -> str:
    return gen_response(en.subscription_details, ua.subscription_details, it.subscription_details)


def requests_100_price(price: str) -> str:
    return gen_response(en.requests_100_price, ua.requests_100_price, it.requests_100_price, price)


def requests_500_price(price: str) -> str:
    return gen_response(en.requests_500_price, ua.requests_500_price, it.requests_500_price, price)


def requests_1000_price(price: str) -> str:
    return gen_response(en.requests_1000_price, ua.requests_1000_price, it.requests_1000_price, price)


def choose_request_package() -> str:
    return gen_response(en.choose_request_package, ua.choose_request_package, it.choose_request_package)


def remaining_requests(requests: str) -> str:
    return gen_response(en.remaining_requests, ua.remaining_requests, it.remaining_requests, requests)


def purchase_requests() -> str:
    return gen_response(en.purchase_requests, ua.purchase_requests, it.purchase_requests)


def cancel_subscription() -> str:
    return gen_response(en.cancel_subscription, ua.cancel_subscription, it.cancel_subscription)


def resume_subscription() -> str:
    return gen_response(en.resume_subscription, ua.resume_subscription, it.resume_subscription)


def back() -> str:
    return gen_response(en.back, ua.back, it.back)


def subscription_settings() -> str:
    return gen_response(en.subscription_settings, ua.subscription_settings, it.subscription_settings)


def create_subscription() -> str:
    return gen_response(en.create_subscription, ua.create_subscription, it.create_subscription)


def create_subscription_header() -> str:
    return gen_response(en.create_subscription_header, ua.create_subscription_header, it.create_subscription_header)


def subscription_paused_remaining_requests() -> str:
    return gen_response(
        en.subscription_paused_remaining_requests,
        ua.subscription_paused_remaining_requests,
        it.subscription_paused_remaining_requests,
    )


def subscription_resumed() -> str:
    return gen_response(en.subscription_resumed, ua.subscription_resumed, it.subscription_resumed)


def subscription_resumption_error() -> str:
    return gen_response(
        en.subscription_resumption_error, ua.subscription_resumption_error, it.subscription_resumption_error
    )


def payment_failed() -> str:
    return gen_response(en.payment_failed, ua.payment_failed, it.payment_failed)


def subscription_settings_portal() -> str:
    return gen_response(
        en.subscription_settings_portal, ua.subscription_settings_portal, it.subscription_settings_portal
    )


def open_portal_link() -> str:
    return gen_response(en.open_portal_link, ua.open_portal_link, it.open_portal_link)


def open_portal_link_header() -> str:
    return gen_response(en.open_portal_link_header, ua.open_portal_link_header, it.open_portal_link_header)


def subscription_successful() -> str:
    return gen_response(en.subscription_successful, ua.subscription_successful, it.subscription_successful)


def payment_unsuccessful() -> str:
    return gen_response(en.payment_unsuccessful, ua.payment_unsuccessful, it.payment_unsuccessful)


def efi_features() -> str:
    return gen_response(en.efi_features, ua.efi_features, it.efi_features)


def subscription_includes() -> str:
    return gen_response(en.subscription_includes, ua.subscription_includes, it.subscription_includes)


def subscription_price_400_month() -> str:
    return gen_response(
        en.subscription_price_400_month, ua.subscription_price_400_month, it.subscription_price_400_month
    )


def subscription_price_4800_year() -> str:
    return gen_response(
        en.subscription_price_4800_year, ua.subscription_price_4800_year, it.subscription_price_4800_year
    )


def remaining_messages_info() -> str:
    return gen_response(en.remaining_messages_info, ua.remaining_messages_info, it.remaining_messages_info)


def trial_activated_message(total_messages: int, remaining_messages: int, end_date: str) -> str:
    return gen_response(
        en.trial_activated_message,
        ua.trial_activated_message,
        it.trial_activated_message,
        total_messages,
        remaining_messages,
        end_date,
    )


def trial_ended_message(total_messages: int, remaining_messages: int, end_date: str) -> str:
    return gen_response(
        en.trial_ended_message,
        ua.trial_ended_message,
        it.trial_ended_message,
        total_messages,
        remaining_messages,
        end_date,
    )


def subscription_active_message(
    start_date: str, plan_price: str, next_billing_date: str, total_messages: int, remaining_messages: int
) -> str:
    return gen_response(
        en.subscription_active_message,
        ua.subscription_active_message,
        it.subscription_active_message,
        start_date,
        plan_price,
        next_billing_date,
        total_messages,
        remaining_messages,
    )


def subscription_cancelled_message(cancellation_date: str, plan_price: str) -> str:
    return gen_response(
        en.subscription_cancelled_message,
        ua.subscription_cancelled_message,
        it.subscription_cancelled_message,
        cancellation_date,
        plan_price,
    )


def tariffs() -> str:
    return gen_response(en.tariffs, ua.tariffs, it.tariffs)


def subscription_management() -> str:
    return gen_response(en.subscription_management, ua.subscription_management, it.subscription_management)


def view_payments() -> str:
    return gen_response(en.view_payments, ua.view_payments, it.view_payments)


def subscription_will_be_cancelled_message(remaining_messages: int, end_date: str) -> str:
    return gen_response(
        en.subscription_will_be_cancelled_message,
        ua.subscription_will_be_cancelled_message,
        it.subscription_will_be_cancelled_message,
        remaining_messages,
        end_date,
    )


def i_like_efi() -> str:
    return gen_response(en.i_like_efi, ua.i_like_efi, it.i_like_efi)


def confirmation_of_cancel_subscription() -> str:
    return gen_response(
        en.confirmation_of_cancel_subscription,
        ua.confirmation_of_cancel_subscription,
        it.confirmation_of_cancel_subscription,
    )


def mutual_love() -> str:
    return gen_response(en.mutual_love, ua.mutual_love, it.mutual_love)


def subscription_cancelled_message_heartbreak() -> str:
    return gen_response(
        en.subscription_cancelled_message_heartbreak,
        ua.subscription_cancelled_message_heartbreak,
        it.subscription_cancelled_message_heartbreak,
    )


def free_trial_activated_message() -> str:
    return gen_response(
        en.free_trial_activated_message, ua.free_trial_activated_message, it.free_trial_activated_message
    )


def free_trial_ended() -> str:
    return gen_response(en.free_trial_ended, ua.free_trial_ended, it.free_trial_ended)


def free_messages_credited(message_count: int) -> str:
    return gen_response(en.free_messages_credited, ua.free_messages_credited, it.free_messages_credited, message_count)


def payment_failed_retry() -> str:
    return gen_response(en.payment_failed_retry, ua.payment_failed_retry, it.payment_failed_retry)


def retry_payment_button() -> str:
    return gen_response(en.retry_payment_button, ua.retry_payment_button, it.retry_payment_button)
