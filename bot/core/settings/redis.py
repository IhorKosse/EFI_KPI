

def redis_key_settings_message_id(user_id: int) -> str:
    return f"settings:message_id:{user_id}"

def redis_key_subscription_continue_id(user_id: int) -> str:
    return f"subscription:continue_id:{user_id}"

def redis_key_subscription_details_id(user_id: int) -> str:
    return f"subscription:details_id:{user_id}"