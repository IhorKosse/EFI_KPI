import settings
from core import log

try:
    import hyperscan  # type: ignore
except ImportError as e:
    if settings.DEBUG:
        log.warning(-1, "Hyperscan is not available. The module will not work.")

    else:
        raise e
