def redis_key_monthly_listing_message_id(user_id: int) -> str:
    return f"listing:monthly:message_id:{user_id}"


def redis_key_weekly_listing_message_id(user_id: int) -> str:
    return f"listing:weekly:message_id:{user_id}"


def redis_key_sequential_listing_offset(user_id: int) -> str:
    return f"listing:sequential:offset:{user_id}"


def redis_key_sequential_listing_last_header_date(user_id: int) -> str:
    return f"listing:sequential:last_header_date:{user_id}"


def redis_key_sequential_listing_load_more_message_id(user_id: int) -> str:
    return f"listing:sequential:load_more_message_id:{user_id}"


def redis_key_sequential_listing_load_more_message_content(user_id: int) -> str:
    return f"listing:sequential:load_more_message_content:{user_id}"


def redis_key_sequential_listing_task_context(user_id: int, message_id: int) -> str:
    return f"listing:sequential:task:{user_id}:{message_id}"

