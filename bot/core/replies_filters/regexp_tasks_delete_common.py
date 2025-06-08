from core import log

try:
    import hyperscan  # type: ignore

    __hyperscan_available = True
except ImportError:
    __hyperscan_available = False



__rule_id = 0


def __next_rule_id(start_from: int | None = None) -> int:
    global __rule_id
    if start_from:
        __rule_id = start_from

    __rule_id += 1
    return __rule_id


__cross_mark = "\\xE2\\x9D\\x8C"
__prohibited = "\\xF0\\x9F\\x9A\\xAB"
__wastebasket = "\\xF0\\x9F\\x97\\x91"
__heavy_multiplication_x = "\\xE2\\x9C\\x96"
__minus_sign = "\\xE2\\x9E\\x96"


if __hyperscan_available:
    database = hyperscan.Database()
    patterns = [
        (
            # "-", "--", "---", ...
            b"^\\-+$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(0),
        ),
        (
            # ❌
            f"^\\W*{__cross_mark}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # 🚫
            f"^\\W*{__prohibited}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # 🗑️
            f"^\\W*{__wastebasket}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # ✖️
            f"^\\W*{__heavy_multiplication_x}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # ➖
            f"^\\W*{__minus_sign}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
    ]
    expressions, flags, ids = zip(*patterns)
    database.compile(expressions=expressions, ids=ids, elements=len(patterns), flags=flags)


__pattern_found: bool


def match(ray: int, message_content: str) -> bool:
    if not __hyperscan_available:
        log.warning(ray, "Hyperscan is not available. The function will always return False.")
        return False
    
    global __pattern_found
    __pattern_found = False
    message = message_content.encode("utf-8")

    try:
        database.scan(message, __match_event_handler)
    except hyperscan.ScanTerminated as e:
        if "error code -3" in str(e):
            # Scan was intentionally terminated by the callback function.
            pass

        else:
            log.error(ray, f"Scan was terminated due to an unexpected error: {e}")
            raise e

    return __pattern_found


def __match_event_handler(id, start, end, flags, context):
    global __pattern_found
    __pattern_found = True

    # Return a non-zero value to tell Hyperscan to stop scanning.
    return 1
