import re


def escape_markdown_v2(text):
    """
    Escape special characters for Markdown V2 compatibility, avoiding double escaping.
    """
    # Characters that need to be escaped in Markdown V2
    escape_chars = "_*[]()~`<>#+-=|{}.!"

    # Regular expression to match characters that need escaping, avoiding already escaped ones
    # We use a negative lookbehind assertion to ensure the character is not already escaped
    pattern = rf'(?<!\\)([{re.escape("".join(escape_chars))}])'

    # Replace matches with escaped version
    escaped_text = re.sub(pattern, r"\\\1", text)

    return escaped_text


def matches_one_line_tasks_list_pattern(text):
    # Pattern:
    # #1 #2 #3 #4 ...

    # Pattern explanation:
    # ^: Start of string
    # (#\d+): '#' followed by one or more digits (first hashtag entry)
    # ( \#\d+)+: One or more occurrences of a space followed by '#', and digits
    # $: End of string
    pattern = r"^(#\d+)(( |, |,)#\d+)+$"

    return bool(re.match(pattern, text))


def format_text(text):
    """
    Escapes special characters for Markdown V2, except for the first and last asterisks.
    """
    result = re.sub(r"\\\*\\\*(.*?)\\\*\\\*", r"*\1*", text)
    return result
