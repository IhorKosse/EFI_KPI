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
            # "<0-2 words> видал <0-1> words" (UA keyboard layout)
            # Видали, видалена, видалено
            # Цю вже видалено, видалено цю, видалено це...
            b"^\\W*\\w*\\W*\\w*\\W*\\xd0\\xb2\\xd0\\xb8\\xd0\\xb4\\xd0\\xb0\\xd0\\xbb\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # "<0-2 words> удал <0-1> words" (UA keyboard layout)
            # Удали, удалила, удалив, ...
            b"^\\W*\\w*\\W*\\w*\\W*\\xd1\\x83\\xd0\\xb4\\xd0\\xb0\\xd0\\xbb\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # "<0-2 words> закр <0-1> words" (UA keyboard layout)
            # Закрий, закрита, закрито
            # Цю вже закрито, закрито цю, закрий це...
            b"^\\W*\\w*\\W*\\w*\\W*\\xd0\\xb7\\xd0\\xb0\\xd0\\xba\\xd1\\x80\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # "<0-2 words> заверш <0-1> words" (UA keyboard layout)
            b"^\\W*\\w*\\W*\\w*\\W*\\xd0\\xb7\\xd0\\xb0\\xd0\\xb2\\xd0\\xb5\\xd1\\x80\\xd1\\x88\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # "<0-2 words> виконан (крім закінчення "я") <0-1> words" (UA keyboard layout)
            # This regular expression represents the words "виконана", "виконано", "виконав", "виконала", and "виконай" encoded in UTF-8
            # Не реагувати на слово "виконання".
            b"\W*\w*\W*\w*\W*\xd0\xb2\xd0\xb8\xd0\xba\xd0\xbe\xd0\xbd\xd0\xb0\xd0\xbd\xd0\xb0|\xd0\xb2\xd0\xb8\xd0\xba\xd0\xbe\xd0\xbd\xd0\xb0\xd0\xbd\xd0\xbe|\xd0\xb2\xd0\xb8\xd0\xba\xd0\xbe\xd0\xbd\xd0\xb0\xd0\xb2|\xd0\xb2\xd0\xb8\xd0\xba\xd0\xbe\xd0\xbd\xd0\xb0\xd0\xbb\xd0\xb0|\xd0\xb2\xd0\xb8\xd0\xba\xd0\xbe\xd0\xbd\xd0\xb0\xd0\xb9\W*\w*\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # "<0-2 words> все <0-1> words" (UA keyboard layout)
            b"^\\W*\\w*\\W*\\w*\\W*\\xd0\\xb2\\xd1\\x81\\xd0\\xb5\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # "не важливо" і варіації.
            # "<0-2 words> не <word> важлив <0-1> words" (UA keyboard layout)
            b"^\\W*\\w*\\W*\\w*\\xd0\\xbd\\xd0\\xb5\\W*\\w*\\W*\\xd0\\xb2\\xd0\\xb0\\xd0\\xb6\\xd0\\xbb\\xd0\\xb8\\xd0\\xb2\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # "<0-2 words> забудь <0-1> words" (UA keyboard layout)
            b"^\\W*\\w*\\W*\\w*\\xd0\\xb7\\xd0\\xb0\\xd0\\xb1\\xd1\\x83\\xd0\\xb4\\xd1\\x8c\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # "не суттєво" і варіації.
            # "<0-2 words> не <word> суттєв <0-1> words" (UA keyboard layout)
            b"^\\W*\\w*\\W*\\w*\\xd0\\xbd\\xd0\\xb5\\W*\\w*\\W*\\xd1\\x81\\xd1\\x83\\xd1\\x82\\xd1\\x82\\xd1\\x94\\xd0\\xb2\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # "не потрібно" і варіації.
            # "<0-2 words> не <word> потріб <0-1> words" (UA keyboard layout)
            b"^\\W*\\w*\\W*\\w*\\xd0\\xbd\\xd0\\xb5\\W*\\w*\\W*\\xd0\\xbf\\xd0\\xbe\\xd1\\x82\\xd1\\x80\\xd1\\x96\\xd0\\xb1\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # "не треба"
            # "<0-2 words> не <word> треба <0-1> words" (UA keyboard layout)
            b"^\\W*\\w*\\W*\\w*\\xd0\\xbd\\xd0\\xb5\\W*\\w*\\W*\\xd1\\x82\\xd1\\x80\\xd0\\xb5\\xd0\\xb1\\xd0\\xb0\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # Скасуй, скасувати, скасувала, ...
            # "<0-2 words> скасу <0-1> words" (UA keyboard layout)
            b"^\\W*\\w*\\W*\\w*\\W*\\xd1\\x81\\xd0\\xba\\xd0\\xb0\\xd1\\x81\\xd1\\x83\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # Скасована, скасований (дзвінок), скасовано
            # "<0-2 words> скасо <0-1> words" (UA keyboard layout)
            b"^\\W*\\w*\\W*\\w*\\W*\\xd1\\x81\\xd0\\xba\\xd0\\xb0\\xd1\\x81\\xd0\\xbe\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # Відмінено, відмінити, відміни, відмінена, відмінений
            # "<0-2 words> відмін <0-1> words" (UA keyboard layout)
            b"^\\W*\\w*\\W*\\w*\\W*\\xd0\\xb2\\xd1\\x96\\xd0\\xb4\\xd0\\xbc\\xd1\\x96\\xd0\\xbd\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # Не актуально, не актуальна (задача), не актуальні (дані), не актуальний (дзвінок)
            # "<0-2 words> не <word> актуальн <0-1> words" (UA keyboard layout)
            b"^\\W*\\w*\\W*\\w*\\xd0\\xbd\\xd0\\xb5\\W*\\w*\\W*\\xd0\\xb0\\xd0\\xba\\xd1\\x82\\xd1\\x83\\xd0\\xb0\\xd0\\xbb\\xd1\\x8c\\xd0\\xbd\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # Немає сенсу, не має сенсу
            # "<0-2 words> не <word> має <non word> сенс <0-1 words>" (UA keyboard layout)
            b"^\\W*\\w*\\W*\\w*\\xd0\\xbd\\xd0\\xb5\\W*\\w*\\W*\\xd0\\xbc\\xd0\\xb0\\xd1\\x94\\W*\\xd1\\x81\\xd0\\xb5\\xd0\\xbd\\xd1\\x81\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # втратила сенс, втратив (дзвінок) сенс
            # "<0-2 words> втрат <word> сенс <0-1 words>" (UA keyboard layout)
            b"^\\W*\\w*\\W*\\w*\\xd0\\xb2\\xd1\\x82\\xd1\\x80\\xd0\\xb0\\xd1\\x82\\W*\\w*\\W*\\xd1\\x81\\xd0\\xb5\\xd0\\xbd\\xd1\\x81\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # Дропни, дропнув, дропнула...
            # "<0-2 words> дропн  <0-1 words>" (UA keyboard layout)
            b"^\\W*\\w*\\W*\\w*\\xd0\\xb4\\xd1\\x80\\xd0\\xbe\\xd0\\xbf\\xd0\\xbd\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # скасована, скасований (дзвінок), ...
            # "<0-2 words> скасован  <0-1 words>" (UA keyboard layout)
            b"^\\W*\\w*\\W*\\w*\\xd1\\x81\\xd0\\xba\\xd0\\xb0\\xd1\\x81\\xd0\\xbe\\xd0\\xb2\\xd0\\xb0\\xd0\\xbd\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # Скасував, скасувала, скасували, ...
            # "<0-2 words> скасув <0-1 words>" (UA keyboard layout)
            b"^\\W*\\w*\\W*\\w*\\xd1\\x81\\xd0\\xba\\xd0\\xb0\\xd1\\x81\\xd1\\x83\\xd0\\xb2\\xd0\\xb0\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
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
