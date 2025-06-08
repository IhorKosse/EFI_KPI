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
            # "ok", "ok.", "ok ", " ok", "OK", "Ok"
            b"^\\W*ok\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(0),
        ),
        (
            # "okay", "okay.", "okay ", " okay", "OKAY", "Okay"
            b"^\\W*okay\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "k", "k.", "k ", " k", "K", "k"
            # (some time users are making a typo and type "k" instead of "ok")
            b"^\\W*k\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "done", "done.", "done ", " done", "DONE", "Done"
            b"^\\W*done\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "complete", "Complete.", "complete ", " complete", "COMPLETE", etc
            # "completed", "completed.", "completed ", " completed", "COMPLETED", etc
            b"^\\W*compl[\\w+]*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        #
        # Phrases
        #
        (
            # "<0-3 words> ok <0-2> words
            # "this is ok", "this one is ok", "ok already", "ok, done", "ok, closed", "ok close"
            b"^\\W*\\w*\\W*\\w*\\W*\\w*\\W*ok\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(100),
        ),
        (
            # "<0-4 words> done <0-2> words
            # "this is done", "this one is done", "done already", "done, ok", "done, closed", "done close", etc
            b"^\\W*\\w*\\W*\\w*\\W*\\w*\\W*\\w*\\W*done\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "<0-3 words> close <0-2> words
            # "this is close", "this one is close", "close already", "close, ok", "close, done", "close done", etc
            b"^\\W*\\w*\\W*\\w*\\W*\\w*\\W*close\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "<0-3 words> check <0-2> words
            b"^\\W*\\w*\\W*\\w*\\W*\\w*\\W*check\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "<0-3 words> checked <0-2> words
            b"^\\W*\\w*\\W*\\w*\\W*\\w*\\W*checked\\W*\\w*\\W*\\w*\\W*$",
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
