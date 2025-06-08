from core.i10n.common import gen_response
from core.i10n import support__en as en
from core.i10n import support__ua as ua
from core.i10n import support__it as it


def link_to_support(link: str) -> str:
    return gen_response(en.link_to_support, ua.link_to_support, it.link_to_support, link)


def write_to_support() -> str:
    return gen_response(en.write_to_support, ua.write_to_support, it.write_to_support)
