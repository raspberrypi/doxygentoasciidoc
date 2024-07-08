import re


def escape_text(text):
    """Escape text so it is safe for use in AsciiDoc."""
    return re.sub(
        r"\(\((.+)\)\)",
        r"\((\1))",
        re.sub(r"\b(__\w+)", r"++\1++", str(text))
        .replace("*", "++*++")
        .replace(" \\\n", " ")
        .replace("->", "\\->"),
    )


def sanitize(identifier):
    """Escape a Doxygen ID so it is safe to use in AsciiDoc."""
    return re.sub(r"__+", r"_", identifier)


def title(text, level, attributes=None):
    """Return text formatted as a title with the given level."""
    if level > 5:
        if attributes is not None:
            if re.search(r'([,\s]role=)', attributes) is not None:
                attributes = re.sub(r'([,\s]role=)(.*?[,\s]?$)', "\\1h6 \\2", attributes)
            else:
                attributes += ",role=h6"
            return f"[{attributes}]\n*{escape_text(text)}*"
        else:
            return f"[.h6]\n*{escape_text(text)}*"

    marker = "=" * (level + 1)
    if attributes is not None:
        return f"[{attributes}]\n{marker} {escape_text(text)}"
    else:
        return f"{marker} {escape_text(text)}"
