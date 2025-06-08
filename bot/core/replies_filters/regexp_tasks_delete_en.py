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
            # "delete" and variations
            #
            # <0-2 words> delete <0-2 words>
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*delete\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(0),
        ),
        (
            # "deleted" and variations
            #
            # <0-2 words> deleted <0-2 words>
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*deleted\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(0),
        ),
        (
            # "del" and variations
            #
            # <0-2 words> del <0-3 words>
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*del\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(0),
        ),
        (
            # "dell" (casual usage) and variations
            #
            # <0-2 words> dell <0-2 words>
            b"^\\W*\\w*\\W*\\w*(is|has|was|must)?\\W*(be|been)?\\W*dell\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(0),
        ),
        (
            # "remove" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*remove\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "removed" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*removed\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "no need" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(no|not)\\W*(need|needed)\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "not required" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(no|not)\\W*(require|required)\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "not essential" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(no|not)\\W*essential\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "not necessary" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(no|not)\\W*necessary\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "cancel" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*cancel\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "canceled" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*(canceled|cancelled)\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "discontinue" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*discontinue\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "discontinued" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*discontinued\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "erase" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*erase\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "erased" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*erased\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "changed mind", "changed my mind" and variations
            # Only word is allowed after "mind", like "sorry"
            b"^\\W*\\w*\\W*\\w*\\W*changed\\W*\\w*\\W*mind\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "abandon" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*abandon\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "abandoned" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*abandoned\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "not necessary" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*(no|not)\\W*necessary\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "unnecessary" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*unnecessary\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "retract" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*retract\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "retracted" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*retracted\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "deactivate" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*deactivate\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "deactivated" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*deactivated\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "deactiv" -> short form of "deactivate"
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*deactiv\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "revoke" and variations
            # WARN: "revok" is not a word, but it's a common typo.
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*(revok|revoke)\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "revoked" and variations
            # WARN: "revok" is not a word, but it's a common typo.
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*(revoked|revokd)\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "expunge" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*expunge\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "expunged" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*expunged\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "terminate" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*terminate\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "terminated" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*terminated\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "drop" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*drop\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
            hyperscan.HS_FLAG_SOM_LEFTMOST,
            __next_rule_id(),
        ),
        (
            # "dropped" and variations
            b"^\\W*\\w*\\W*\\w*\\W*(is|has|was|must)?\\W*(be|been)?\\W*dropped\\W*(this one|this)?\\W*\\w*\\W*\\w*\\W*$",
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
