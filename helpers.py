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
    """Return text formatted as a title with the given level and attributes."""
    if attributes is None:
        attributes = {}

    attrlist = []

    if "id" in attributes:
        attrlist.append(f"#{sanitize(attributes.pop('id'))}")

    roles = []

    if level > 5:
        roles.append("h6")
    if "role" in attributes:
        roles.append(attributes.pop("role"))

    if roles:
        attrlist.append(f"role={' '.join(roles)}")

    if "tag" in attributes:
        attrlist.append(f"tag={escape_text(attributes.pop('tag'))}")
    if "type" in attributes:
        attrlist.append(f"type={escape_text(attributes.pop('type'))}")
    for key, value in attributes.items():
        attrlist.append(f'{escape_text(key)}="{escape_text(value)}"')

    output = []

    if attrlist:
        output.append(f"[{','.join(attrlist)}]")

    if level > 5:
        output.append(f"*{escape_text(text)}*")
    else:
        marker = "=" * (level + 1)
        output.append(f"{marker} {escape_text(text)}")

    return "\n".join(output)
