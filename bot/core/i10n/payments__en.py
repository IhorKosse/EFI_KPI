import settings


def invoice_title(requests: int) -> str:
    request_word = "Request" if requests == 1 else "Requests"
    return f"{requests} {request_word}"


def invoice_description(requests: int) -> str:
    request_word = "request" if requests == 1 else "requests"
    return f"{requests} {request_word} package"


def one_month_subscription_price(price: str) -> str:
    return f"1 month — {price}$/month"


def three_months_subscription_price(price: str) -> str:
    return f"3 months — {price}$/month"


def six_months_subscription_price(price: str) -> str:
    return f"6 months — {price}$/month"


def currency() -> str:
    return "USD"


def choose_subscription() -> str:
    return "Select your desired subscription:"


def subscription_paid_message() -> str:
    return "Thank you for your subscription, now you can use all the features of Efi! 🚀 Let us know if you'd like some help from us @efi_support"


def active_subscription(date: str) -> str:
    return f"Subscription is active until {date}"


def continue_subscription() -> str:
    return "Continue subscription"


def support() -> str:
    return "Support"


def support_link(link: str) -> str:
    return f"Link to support channel: {link}"


def subscribe() -> str:
    return "Subscribe"


def subscription() -> str:
    return "Plans and Subscriptions"


def subscription_details() -> str:
    return "Subscription details:"


def requests_100_price(price: str) -> str:
    return f"100 requests — {price}$"


def requests_500_price(price: str) -> str:
    return f"500 requests — {price}$"


def requests_1000_price(price: str) -> str:
    return f"1000 requests — {price}$"


def choose_request_package() -> str:
    return "Choose your desired number of requests:"


def remaining_requests(requests: str) -> str:
    return f"You have {requests} requests left"


def purchase_requests() -> str:
    return "Purchase more requests"


def cancel_subscription() -> str:
    return "Cancel subscription"


def resume_subscription() -> str:
    return "Resume subscription"


def back() -> str:
    return "Back"


def subscription_settings() -> str:
    return "Plans and subscription settings:"


def create_subscription() -> str:
    return "🔋 Create subscription"


def create_subscription_header() -> str:
    return "Please complete your subscription using the button below:"


def subscription_paused_remaining_requests() -> str:
    return "Your subscription has been paused. You can use the remaining requests within the next 30 days, after which they will expire."


def subscription_resumed() -> str:
    return "Your subscription has been resumed. Welcome back 💚"


def subscription_resumption_error() -> str:
    return "An error occurred while resuming the subscription. Please contact support if you are experiencing issues @efi_support"


def payment_failed() -> str:
    return "Payment failed. Please try again or contact support @efi_support."


def subscription_settings_portal() -> str:
    return "Subscription settings"


def open_portal_link() -> str:
    return "Open settings"


def open_portal_link_header() -> str:
    return "Click the button below to go to the settings"


def subscription_successful() -> str:
    return "🎉 Your subscription has been activated! Enjoy! ☺️ \n\nIf you have any questions, please contact our support @efi_support"


def payment_unsuccessful() -> str:
    return "Unfortunately, something went wrong with the payment system during the subscription attempt 😔\n\nShall we try again?"


def efi_features() -> str:
    return (
        "🟢 Plan tasks and activities with the help of AI\\. It's like having a personal assistant always available\\.\n\n"
        "🟢 Add context quickly and easily, right from your favorite messenger\\.\n\n"
        "🟢 Automatically organize events considering all possible aspects, experience the benefits of effective time management\\.\n\n"
        "[🎯 Learn more about the features and benefits of Efi](https://telegra.ph/EFI-EN-05-01)"
    )


def subscription_includes() -> str:
    monthly_calls = settings.MONTHLY_MESSAGE_LIMIT
    yearly_calls = settings.YEARLY_MESSAGE_LIMIT
    savings = settings.SUBSCRIPTION_PRICES["savings"]

    return (
        f"The subscription includes *{monthly_calls}* AI assistant messages per month, or *{yearly_calls}* per year \\(savings — ${savings}\\)\n\n"
        f"_This is enough to plan and execute approximately {monthly_calls} tasks, but the final cost depends on how you use the AI assistant\\._\n\n"
        "[Full list of service terms\\.](https://telegra.ph/Pricing-Plan-07-18)"
    )


def subscription_price_400_month() -> str:
    monthly_price = settings.SUBSCRIPTION_PRICES["monthly"]
    monthly_calls = settings.MONTHLY_MESSAGE_LIMIT

    return f"🔋 ${monthly_price} — {monthly_calls} messages/month"


def subscription_price_4800_year() -> str:
    yearly_price = settings.SUBSCRIPTION_PRICES["yearly"]
    yearly_calls = settings.YEARLY_MESSAGE_LIMIT

    return f"🔋 ${yearly_price} — {yearly_calls} messages/year"


def remaining_messages_info() -> str:
    return (
        "You have 40 messages left to the AI this month\\.\n\n"
        "What to do if you need more messages this month\\.\n\n"
        "[How to use messages optimally?](https://telegra.ph/FAQ-07-18-9)\n\n"
        "[How to check the remaining messages?](https://telegra.ph/FAQ-07-18-9)\n\n"
        "[What if the messages to the AI run out?](https://telegra.ph/FAQ-07-18-9)"
    )


def trial_activated_message(total_messages: int, remaining_messages: int, end_date: str) -> str:
    return (
        f"Trial period activated 🎉\n\n"
        f"Total messages\\: {total_messages}\n"
        f"*Messages remaining\\: {remaining_messages}*\n"
        f"End date\\: {end_date}\n\n"
        "[What are the benefits of the subscription\\?](https://telegra.ph/FAQ-07-18-9)\n\n"
        "[How to add a subscription\\?](https://telegra.ph/FAQ-07-18-9)\n\n"
        "[How to use messages optimally\\?](https://telegra.ph/FAQ-07-18-9)"
    )


def trial_ended_message(total_messages: int, remaining_messages: int, end_date: str) -> str:
    return (
        f"Trial period ended\\.\n\n"
        f"Total messages\\: {total_messages}\n"
        f"*Messages remaining\\: {remaining_messages}*\n"
        f"End date\\: {end_date}\n\n"
        "[How can I continue using the service\\?](https://telegra.ph/FAQ-07-18-9)"
    )


def subscription_active_message(
    start_date: str, plan_price: str, next_billing_date: str, total_messages: int, remaining_messages: int
) -> str:
    period = "month" if plan_price == settings.SUBSCRIPTION_PRICES_MARKDOWN["monthly"] else "year"
    return (
        f"Your subscription is active\\! 🎉\n\n"
        f"Created on: {start_date}\n"
        f"Plan price: {plan_price}\\$ / {period}\n"
        f"Next billing date: {next_billing_date}\n\n"
        f"Total messages: {total_messages}\n"
        f"*Messages remaining: {remaining_messages}*\n\n"
        "[What if I use more messages than the plan allows?](https://telegra.ph/FAQ-07-18-9)\n\n"
        "[How to cancel the subscription?](https://telegra.ph/FAQ-07-18-9)\n\n"
        "[How to use messages optimally?](https://telegra.ph/FAQ-07-18-9)\n"
    )


def subscription_cancelled_message(cancellation_date: str, plan_price: str) -> str:
    period = "month" if plan_price == settings.SUBSCRIPTION_PRICES_MARKDOWN["monthly"] else "year"
    return (
        f"Your subscription has been cancelled 😔\n\n"
        f"Cancellation date: {cancellation_date}\n"
        f"Plan price: {plan_price}\\$ / {period}\n\n"
        "[How can I continue using the service?](https://telegra.ph/FAQ-07-18-9)"
    )


def tariffs() -> str:
    return "Tariffs:"


def subscription_management() -> str:
    return "⚙️ Subscription Management"


def view_payments() -> str:
    return "View Payments"


def subscription_will_be_cancelled_message(remaining_messages: int, end_date: str) -> str:
    return (
        f"Your subscription will be cancelled\\.\n\n"
        f"*Remaining messages \\({remaining_messages} messages\\) can be used until {end_date},*"
        f"after which access to AI features will be terminated, but access to tasks will remain forever\\.\n\n"
        "Continue\\?"
    )


def i_like_efi() -> str:
    return "No, I like Efi 💚"


def confirmation_of_cancel_subscription() -> str:
    return "Yes, cancel the subscription"


def mutual_love() -> str:
    return "It's mutual! 💚"


def subscription_cancelled_message_heartbreak() -> str:
    return "Your subscription has been cancelled 💔"


def free_trial_activated_message() -> str:
    return (
        "🎉 Your free trial period has been activated\\! Enjoy\\! 😉\n\n"
        "You can find more about it [at this link](https://telegra.ph/Trial-Period-Usage-07-08-2)\\, or in the settings ⚙️"
    )


def free_trial_ended() -> str:
    return (
        "Your free trial period has ended. To continue using the service, please create a subscription.\n\n"
        "This will allow you to keep using 🤖 Efi's AI features and support the project 💚\n\n"
        "You can always view tasks created earlier. Everything remains as it was."
    )


def free_messages_credited(message_count: int) -> str:
    return f"{message_count} free messages credited\\! _Enjoy 💚\n\nWith care\\, the Efi team\\!_"


def payment_failed_retry() -> str:
    return "Your subscription payment failed. Please try again."


def retry_payment_button() -> str:
    return "Retry Payment"
