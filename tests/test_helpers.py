from doxygentoasciidoc.helpers import escape_text, sanitize, title


def test_escape_text_escapes_words_starting_with_double_underscore():
    assert escape_text("foo __bar baz") == "foo ++__bar++ baz"


def test_escape_text_escapes_literal_asterisks():
    assert escape_text("* foo * bar") == "++*++ foo ++*++ bar"


def test_escape_text_strips_line_continuation_characters():
    assert escape_text(" \\\n") == " "


def test_escape_text_accepts_non_strings():
    assert escape_text(123) == "123"


def test_escape_text_escapes_double_parentheses():
    assert escape_text("((hello))") == "\\((hello))"


def test_sanitize_replaces_multiple_leading_underscores():
    assert sanitize("___foo__bar") == "_foo_bar"


def test_title_with_level_1():
    assert title("Level 1 Section Title", 1) == "== Level 1 Section Title"


def test_title_with_level_5():
    assert title("Level 5 Section Title", 5) == "====== Level 5 Section Title"


def test_title_with_level_6():
    assert title("Level 6 Section Title", 6) == "*Level 6 Section Title*"


def test_title_escapes_text():
    assert title("3 * 2 = 6", 1) == "== 3 ++*++ 2 = 6"


def test_title_escapes_text_with_level_6():
    assert title("3 * 2 = 6", 6) == "*3 ++*++ 2 = 6*"
