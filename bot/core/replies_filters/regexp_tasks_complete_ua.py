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


if __hyperscan_available:
    database = hyperscan.Database()
    patterns = [
        (
            # "ок", "ок.", "ок ", " ок", "ОК", "Ок" (UA keyboard layout)
            b"^\\W*\\xD0\\xBE\\xD0\\xBA\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "к", "к.", "к ", " к", "К", "к" (UA keyboard layout)
            b"^\\W*\\xD0\\xBEW*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "Окей", "ОКЕЙ", (UA keyboard layout)
            b"^\\W*\\xD0\\xBE\\xD0\\xBA\\xD0\\xB5\\xD0\\xB9\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "Зроблено", "Зроблено!", "Зроблено.", "Зроблена", "зробив!", "зробила!" (UA keyboard layout)
            b"^\\W*\\xD0\\xB7\\xD1\\x80\\xD0\\xBE\\xD0\\xB1\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "Готов" (UA keyboard layout)
            # "готово", "готова", ...
            b"^\\W*\\xD0\\xB3\\xD0\\xBE\\xD1\\x82\\xD0\\xBE\\xD0\\xB2\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "Дан" (UA keyboard layout)
            b"^\\W*\\xD0\\xB4\\xD0\\xB0\\xD0\\xBD\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        #
        # Phrases
        #
        (
            # "<0-2 words> зроб <0-1> words" (UA keyboard layout)
            # Познач як зроблено
            # Ця зроблена
            # Ця вже зроблена
            # Цю вже зробив колись
            # Ця насправді зроблена
            # Цю задачу зроблено
            # Зроблена вже
            b"^\\W*\\w*\\W*\\w*\\W*\\xD0\\xB7\\xD1\\x80\\xD0\\xBE\\xD0\\xB1\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # "<0-2 words> готов <0-1> words" (UA keyboard layout)
            # Познач як готову
            # Ця готова
            # Ця вже готова
            # Ця насправді готова
            # Готова вже
            b"^\\W*\\w*\\W*\\w*\\W*\\xD0\\xB3\\xD0\\xBE\\xD1\\x82\\xD0\\xBE\\xD0\\xB2\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # Чекнута, чекнутий, і т.д.
            # "<0-2 words> чекн <0-1> words" (UA keyboard layout)
            b"^\\W*\\w*\\W*\\w*\\W*\\xd1\\x87\\xd0\\xb5\\xd0\\xba\\xd0\\xbd\\xd0\\xb8\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # Закрита, закритий, закрито
            # "<0-2 words> закр <0-1> words" (UA keyboard layout)
            b"^\\W*\\w*\\W*\\w*\\W*\\xd0\\xb7\\xd0\\xb0\\xd0\\xba\\xd1\\x80\\W*\\w*\\W*$",
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
