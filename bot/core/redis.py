
def redis_key_payments_optional(user_id: int) -> str:
    return f"payments_optional:message_id:{user_id}"

def redis_key_payments_invoice(user_id: int) -> str:
    return f"payments_invoice:message_id:{user_id}"

def redis_key_requests_optional(user_id: int) -> str:
    return f"requests_optional:message_id:{user_id}"
