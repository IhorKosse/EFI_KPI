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


__thumb_up = "\\xF0\\x9F\\x91\\x8D"
__thumb_up_light = f"{__thumb_up}\\xF0\\x9F\\x8F\\xBB"
__thumb_up_medium_light = f"{__thumb_up}\\xF0\\x9F\\x8F\\xBC"
__thumb_up_medium = f"{__thumb_up}\\xF0\\x9F\\x8F\\xBD"
__thumb_up_medium_dark = f"{__thumb_up}\\xF0\\x9F\\x8F\\xBE"
__thumb_up_dark = f"{__thumb_up}\\xF0\\x9F\\x8F\\xBF"

__ok_hand = "\\xF0\\x9F\\x91\\x8C"
__ok_hand_light = f"{__ok_hand}\\xF0\\x9F\\x8F\\xBB"
__ok_hand_medium_light = f"{__ok_hand}\\xF0\\x9F\\x8F\\xBC"
__ok_hand_medium = f"{__ok_hand}\\xF0\\x9F\\x8F\\xBD"
__ok_hand_medium_dark = f"{__ok_hand}\\xF0\\x9F\\x8F\\xBE"
__ok_hand_dark = f"{__ok_hand}\\xF0\\x9F\\x8F\\xBF"

# "🆗" emoji (There are no skin tone variations for this emoji)
__ok_button = "\\xF0\\x9F\\x86\\x97"

# "✅" emoji (There are no skin tone variations for this emoji)
__check_mark_button = "\\xE2\\x9C\\x85"

# "☑️" emoji (There are no skin tone variations for this emoji)
__ballot_box_with_check = "\\xE2\\x98\\x91\\xEF\\xB8\\x8F"


if __hyperscan_available:
    database = hyperscan.Database()
    patterns = [
        (
            # "+", "++", "+++", ...
            b"^\\++$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(0),
        ),
        (
            # "👍", ".👍", "👍." and other variations
            f"^\\W*{__thumb_up}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "👍🏻", ".👍🏻", "👍🏻." and other variations
            f"^\\W*{__thumb_up_light}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "👍🏼", ".👍🏼", "👍🏼." and other variations
            f"^\\W*{__thumb_up_medium_light}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "👍🏽", ".👍🏽", "👍🏽." and other variations
            f"^\\W*{__thumb_up_medium}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "👍🏾", ".👍🏾", "👍🏾." and other variations
            f"^\\W*{__thumb_up_medium_dark}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "👍🏿", ".👍🏿", "👍🏿." and other variations
            f"^\\W*{__thumb_up_dark}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "👌", ".👌", "👌." and other variations
            f"^\\W*{__ok_hand}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "👌🏻", ".👌🏻", "👌🏻." and other variations
            f"^\\W*{__ok_hand_light}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "👌🏼", ".👌🏼", "👌🏼." and other variations
            f"^\\W*{__ok_hand_medium_light}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "👌🏽", ".👌🏽", "👌🏽." and other variations
            f"^\\W*{__ok_hand_medium}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "👌🏾", ".👌🏾", "👌🏾." and other variations
            f"^\\W*{__ok_hand_medium_dark}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "👌🏾", ".👌🏾", "👌🏾." and other variations
            f"^\\W*{__ok_hand_dark}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "🆗" emoji (There are no skin tone variations for this emoji)
            f"^\\W*{__ok_button}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "✅" emoji (There are no skin tone variations for this emoji)
            f"^\\W*{__check_mark_button}\\W*$".encode("utf-8"),
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "☑️" emoji (There are no skin tone variations for this emoji)
            f"^\\W*{__ballot_box_with_check}\\W*$".encode("utf-8"),
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
