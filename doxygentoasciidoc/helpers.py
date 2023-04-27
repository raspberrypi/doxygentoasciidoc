import re


def escape_text(text):
    """Escape text so it is safe for use in AsciiDoc."""
    return (
        re.sub(r"\b(__\w+)", r"++\1++", str(text))
        .replace("*", "++*++")
        .replace(" \\\n", " ")
        .replace("((", "\\((")
    )


def sanitize(identifier):
    """Escape a Doxygen ID so it is safe to use in AsciiDoc."""
    return re.sub(r"__+", r"_", identifier)


def title(text, level):
    """Return text formatted as a title with the given level."""
    if level > 5:
        return f"*{escape_text(text)}*"

    marker = "=" * (level + 1)
    return f"{marker} {escape_text(text)}"
